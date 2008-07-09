"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy
import logging
import Queue

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore, QtGui # gui for testing only
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.datalib.hdf5 import XpaxsFile, XpaxsScan

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


logger = logging.getLogger('XPaXS.spectromicroscopy.smpdatainterface')
DEBUG = False

filters = tables.Filters(complib='zlib', complevel=9)


def getSpecScanInfo(commandList):
    scanType, args = commandList[0], commandList[1:]
    scanAxes = []
    scanRange = {}
    scanShape = []
    if scanType in ('mesh', ):
        while len(args) > 4:
            (axis, start, stop, step), args = args[:4], args[4:]
            scanAxes.append((axis, ))
            scanRange[axis] = (float(start), float(stop))
            scanShape.append(int(step)+1)
    elif scanType in ('ascan', 'a2scan', 'a3scan',
                         'dscan', 'd2scan', 'd3scan'):
        temp = []
        while len(args) > 3:
            (axis, start, stop), args = args[:3], args[3:]
            temp.append(axis)
            scanRange[axis] = (float(start), float(stop))
        scanAxes.append(tuple(temp))
        scanShape.append(int(args[0])+1)
    else:
        raise RuntimeError('Scan %s not recognized!'%commandType)
    scanShape = tuple(scanShape[::-1])

    return (scanType, scanAxes, scanRange, scanShape)


class SmpFile(XpaxsFile):

    def createEntry(self, scanParams):
        scanParams = copy.deepcopy(scanParams)
        scanName = scanParams['title'].lower().replace(' ', '')
        try:
            self.mutex.lock()

            # It is possible for a scan number to appear multiple times in a
            # spec file. Booo!
            scanOrder = ''
            i = 0
            while (scanName + scanOrder) in self.h5File.root:
                i += 1
                scanOrder = '.%d'%i
            scanName = scanName + scanOrder

            h5Entry = self.h5File.createGroup('/', scanName, title=scanName,
                                              filters=filters)
            attrs = h5Entry._v_attrs
            attrs.scanNumber = scanParams['scanNumber']
            attrs.scanCommand = scanParams['scanCommand']
            attrs.scanLines = scanParams['scanLines']
            attrs.fileName = scanParams['fileName'].split('/')[-1]
            scanInfo = getSpecScanInfo(scanParams['scanCommand'].split())
            attrs.scanType = scanInfo[0]
            attrs.scanAxes = scanInfo[1]
            attrs.scanRange = scanInfo[2]
            attrs.scanShape = scanInfo[3]

            skipmode = scanParams.get('skipmode', None)
            if skipmode:
                mon, thresh = skipmode.split()
                attrs.skipmodeMonitor = mon
                attrs.skipmodeThresh = float(thresh)

            for entry in scanParams['motorPositions'].split():
                key, val = entry.split('=')
                setattr(attrs, key, float(val))

            Data = {}
            for label in scanParams['columnNames'].split():
                if label == 'epoch': Data[label] = tables.Float64Col()
                else: Data[label] = tables.Float32Col()

            mcas = scanParams.get('mcas', '').split()
            for mca in mcas:
                mcaEntry = self.h5File.createGroup(h5Entry, mca, title=mca,
                                                   filters=filters)

                channels = scanParams['mcaChannels_%s'%mca]
                channelsEntry = self.h5File.createCArray(mcaEntry, 'channels',
                                                         tables.UInt16Atom(),
                                                         channels.shape,
                                                         filters=filters)
                channelsEntry[:] = channels

                energy = scanParams['mcaEnergy_%s'%mca]
                energyEntry = self.h5File.createCArray(mcaEntry, 'energy',
                                                         tables.UInt16Atom(),
                                                         energy.shape,
                                                         filters=filters)
                energyEntry[:] = energy

                Data[mca] = tables.Float32Col(shape=channels.shape)

            dataTable = self.h5File.createTable(h5Entry, 'data', Data,
                                                filters=filters,
                                                expectedrows=attrs.scanLines)
        finally:
            self.mutex.unlock()
        self.flush()
        scanEntry = SmpScan(self, h5Entry)
        self.emit(QtCore.SIGNAL('newEntry'), scanEntry)
        return scanEntry

    def getNode(self, where, name=None):
        node = self.h5File.getNode(where, name)
        # TODO: these checks should eventually look for nexus classes
        # for now just use the pytables classes
        if isinstance(node, tables.Group):
            return SmpScan(self, node)


class SmpScan(XpaxsScan):

    def __init__(self, *args, **kwargs):
        super(SmpScan, self).__init__(*args, **kwargs)
        self._numSkippedPoints = len(self.getInvalidDataPoints())

    def appendDataPoint(self, data):
        data = copy.deepcopy(data)
        mon, thresh = self.getSkipmode()
        if DEBUG: print "appending data point:", data['i']
        try:
            self.mutex.lock()
            row = self.h5Node.data.row
            for key, val in data.iteritems():
                row[key] = val
            row.append()
            self.h5Node.data.flush()
            if data[mon] > thresh:
                self.queue.put(int(data['i']))
            else:
                self._numSkippedPoints += 1
        finally:
            self.mutex.unlock()
#        self.flush()

    def getAvailableElements(self):
        try:
            self.mutex.lock()
            elements = self.h5Node.elementMaps.fitArea._v_leaves.keys()
        except tables.NoSuchNodeError:
            return []
        finally:
            self.mutex.unlock()
        elements.sort()
        return elements

    def getAverageMcaSpectrum(self, indices=[], id='MCA', normalization=None):
        if len(indices) > 0:
            try:
                self.mutex.lock()
                spectrum = self.h5Node.data[indices[0]][id]*0
                numIndices = len(indices)
                for index in indices:
                    result = self.h5Node.data[index][id]
                    if normalization is not None:
                        result /= getattr(self.h5Node.data.cols,
                                          normalization)[index]
                    spectrum += result
                return spectrum / len(indices)
            finally:
                self.mutex.unlock()

    def getElementMap(self, mapType, element, normalization=None):
        dataPath = '/'.join(['elementMaps', mapType, element])
        try:
            self.mutex.lock()
            try:
                elementMap = self.h5Node._v_file.getNode(self.h5Node, dataPath)[:]
            except tables.NoSuchNodeError:
                print dataPath
                return numpy.zeros(self.getScanShape())
        finally:
            self.mutex.unlock()
        if normalization:
            try:
                self.mutex.lock()
                norm = getattr(self.h5Node.data.cols, normalization)[:]
            finally:
                self.mutex.unlock()
            elementMap.flat[:len(norm)] /= numpy.where(norm==0, numpy.inf, norm)
        return elementMap

    def getInvalidDataPoints(self, indices=None):
        mon, thresh = self.getSkipmode()
        try:
            self.mutex.lock()
            if mon and thresh:
                temp = getattr(self.h5Node.data.cols, mon)[:]
                invalid = numpy.nonzero(temp < thresh)[0]
            else:
                invalid = []
        finally:
            self.mutex.unlock()

        if indices is None: return invalid
        if len(indices): return [i for i in indices if i in invalid]
        else: return invalid

    def getMcaSpectrum(self, index, id='MCA', normalization=None):
        try:
            self.mutex.lock()
            result = self.h5Node.data[index][id][:]
            if normalization is not None:
                result /= getattr(self.h5Node.data.cols, normalization)[index]
            return result
        finally:
            self.mutex.unlock()

    def getMcaChannels(self, id='MCA'):
        try:
            self.mutex.lock()
            return getattr(self.h5Node, id).channels[:]
        finally:
            self.mutex.unlock()

    def getNormalizationChannels(self):
        try:
            self.mutex.lock()
            channels = [i for i in copy.deepcopy(self.h5Node.data.colnames)
                        if not i in self.h5Node._v_attrs]
            # TODO: This is a wart, to be fixed with better structuring of
            # files via nexus standard:
            channels.remove('MCA')
        finally:
            self.mutex.unlock()
        return channels

    def getNumSkippedPoints(self):
        try:
            self.mutex.lock()
            return copy.copy(self._numSkippedPoints)
        finally:
            self.mutex.unlock()

    def getPymcaConfig(self):
        try:
            self.mutex.lock()
            try:
                return copy.deepcopy(self.h5Node._v_attrs.pymcaConfig)
            except AttributeError:
                return None
        finally:
            self.mutex.unlock()

    def getValidDataPoints(self, indices=None):
        mon, thresh = self.getSkipmode()
        try:
            self.mutex.lock()
            if mon and thresh:
                temp = getattr(self.h5Node.data.cols, mon)[:]
                valid = numpy.nonzero(temp > thresh)[0]
            else:
                valid = range(len(self.h5Node.data))
        finally:
            self.mutex.unlock()

        if indices is None: return valid
        if len(indices): return [i for i in indices if i in valid]
        else: return valid

    def initializeElementMaps(self, elements):
        elements = copy.deepcopy(elements)
        shape = self.getScanShape()
        filters = self.getH5Filters()
        try:
            self.mutex.lock()
            try:
                self.h5Node._v_file.removeNode(self.h5Node, 'elementMaps',
                                       recursive=True)
            except tables.NoSuchNodeError:
                pass
            elementMaps = self.h5Node._v_file.createGroup(self.h5Node,
                                                          'elementMaps')
            for mapType in ['fitArea', 'massFraction', 'sigmaArea']:
                self.h5Node._v_file.createGroup(elementMaps, mapType)
                for element in elements:
                    node = self.h5Node._v_file.getNode(self.h5Node.elementMaps,
                                               mapType)
                    self.h5Node._v_file.createCArray(node,
                                             element.replace(' ', ''),
                                             tables.Float32Atom(),
                                             shape,
                                             filters=filters)
        finally:
            self.mutex.unlock()
        self.flush()

    def setPymcaConfig(self, config):
        try:
            self.mutex.lock()
            self.h5Node._v_attrs.pymcaConfig = copy.deepcopy(config)
        finally:
            self.mutex.unlock()

    def getSkipmode(self):
        try:
            self.mutex.lock()
            mon = self.h5Node._v_attrs.skipmodeMonitor[:]
            thresh = copy.copy(self.h5Node._v_attrs.skipmodeThresh)
            return (mon, thresh)
        except AttributeError:
            return (None, 0)
        finally:
            self.mutex.unlock()

    def setSkipmode(self, monitor=None, thresh=0):
        monitor = copy.copy(monitor)
        thresh = copy.copy(thresh)
        try:
            self.mutex.lock()
            self.h5Node._v_attrs.skipmodeMonitor = monitor
            self.h5Node._v_attrs.skipmodeThresh = thresh
        finally:
            self.mutex.unlock()

    def updateElementMap(self, mapType, element, index, val):
        val = copy.copy(val)
        node = '/'.join(['elementMaps', mapType, element])
        try:
            self.mutex.lock()
            try:
                self.h5Node._v_file.getNode(self.h5Node, node)[index] = val
            except ValueError:
                print index, node
        finally:
            self.mutex.unlock()
