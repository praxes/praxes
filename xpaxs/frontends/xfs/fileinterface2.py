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
import h5py
from PyMca.ConfigDict import ConfigDict

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.io.h5file import XpaxsH5File, XpaxsH5Scan
from xpaxs.frontends.base.fileinterface2 import H5FileInterface, H5FileModel

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


logger = logging.getLogger('XPaXS.frontends.xfs.fileinterface')
DEBUG = False

#filters = tables.Filters(complib='zlib', complevel=9)


def getSpecScanInfo(commandList):
    scanType, args = commandList[0], commandList[1:]
    scanAxes = []
    scanRange = {}
    scanShape = []
    if scanType in ('mesh', ):
        while len(args) > 4:
            (axis, start, stop, step), args = args[:4], args[4:]
            scanAxes.append((axis, ))
            scanRange[axis] = [float(start), float(stop)]
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


class XfsH5File(XpaxsH5File):

    def createEntry(self, scanParams):
        try:
            self.mutex.lock()

            scanEntry = XfsH5Scan(self, scanParams)

        finally:
            self.mutex.unlock()

        self.emit(QtCore.SIGNAL('newEntry'), scanEntry)
        return scanEntry

    def iterobjects(self):
        for group in self.h5File.iterobjects():
            yield XfsH5Scan(self, group)

#    def getNode(self, where, name=None):
#        node = self.h5File.getNode(where, name)
#        # TODO: these checks should eventually look for nexus classes
#        # for now just use the pytables classes
#        if isinstance(node, tables.Group):
#            return XfsH5Scan(self, node)


class McaSpectraIterator(object):

    def __init__(self, scanData):
        self._currentIndex = 0
        self._scanData = scanData
        self._mutex = QtCore.QMutex(QtCore.QMutex.Recursive)

    def __iter__(self):
        return self

    @property
    def currentIndex(self):
        try:
            self.mutex.lock()
            return copy.copy(self._currentIndex)
        finally:
            self.mutex.unlock()

    @property
    def mutex(self):
        return self._mutex

    @property
    def numExpectedPoints(self):
        return self._scanData.numExpectedPoints

    def next(self):
        try:
            self.mutex.lock()
            if self._currentIndex >= self.numExpectedPoints:
                raise StopIteration

            else:
                try:
                    if self._scanData.isValidDataPoint(self._currentIndex):
                        i = self._currentIndex
                        spectrum = self._scanData.getMcaSpectrum(i)
                        self._currentIndex += 1

                        return i, spectrum

                    else:
                        self._currentIndex += 1
                        return self.next()
                except h5py.h5.ArgsError:
                    raise IndexError
        finally:
            self.mutex.unlock()


class XfsH5Scan(XpaxsH5Scan):

    def __init__(self, xpaxsFile, scanParams):
        XpaxsH5Scan.__init__(self, xpaxsFile, scanParams)
        self._numSkippedPoints = len(self.getInvalidDataPoints())

    def _initializeEntry(self, scanParams):
        try:
            self.mutex.lock()

            self._columnNames = scanParams['scan_desc']['column names']

            data = self.h5Node.create_group('data')

            attrs = self.h5Node.attrs

            attrs['scan number'] = scanParams['scan_desc']['scan number']
            attrs['scan command'] = scanParams['scan_desc']['command']
            attrs['scan points'] = scanParams['scan_desc']['scan points']
            attrs['filename'] = scanParams['scan_desc']['filename'].split('/')[-1]

            info = getSpecScanInfo(scanParams['scan_desc']['command'].split())

            attrs['scan type'] = info[0]
            attrs['scan axes'] = str(info[1])
            attrs['scan range'] = str(info[2])
            attrs['scan shape'] = str(info[3])

            skipmode = scanParams.get('skipmode', None)
            if skipmode:
                skipmode = self.h5Node.create_group('skipmode')
                try:
                    skipmode.attrs['monitor'] = scanParams['skipmode']['monitor']
                    skipmode.attrs['threshold'] = scanParams['skipmode']['threshold']
                except KeyError:
                    pass

            for key, val in scanParams['motor_positions'].iteritems():
                setattr(attrs, key, val)

            for key, val in scanParams.iteritems():
                try:
                    if val['type'] == 'MCA':
                        # yuck, we'll use the key as the entry name when we
                        # move to the new file format, instead of defaulting
                        # to "MCA"
                        mcaEntry = self.h5Node.create_group('MCA')

                        channelsEntry = mcaEntry.create_dataset(
                            'channels', data=val['channels']
                        )

                        energyEntry = mcaEntry.create_dataset(
                            'energy', data=val['energy']
                        )

                except (KeyError, TypeError):
                    pass

        finally:
            self.mutex.unlock()
        self.flush()

    @property
    def iterMcaSpectra(self):
        return McaSpectraIterator(self)

    def _initializeData(self, key, val):
        # TODO: This should also go inside the datasets
        try:
            self.mutex.lock()

            if key == 'epoch':
                val = numpy.array([val], 'd')
            elif key == 'i':
                val = numpy.array([val], 'uint32')
            else:
                val = numpy.array([val], 'f')

            maxshape = [self.numExpectedPoints]
            maxshape.extend(val.shape[1:])

            self.h5Node['data'].create_dataset(key, data=val, maxshape=maxshape)

            self.flush()

            # TODO: Is this the best way to get this information?
            if key == 'i':
                self.emit(QtCore.SIGNAL('dataInitialized'))

        finally:
            self.mutex.unlock()

    def _updateDataset(self, key, i, val):
        try:
            self.mutex.lock()

            # TODO: This should be refactored into the dataset subclasses
            if key not in self.h5Node['data']:
                self._initializeData(key, val)
            else:
                shape = list(self.h5Node['data'][key].shape)
                shape[0] = i+1
                self.h5Node['data'][key].extend(tuple(shape))
                self.h5Node['data'][key][i] = val
#            try:
#                self.h5Node['data'][key][i] = val
#            except IndexError:
#                shape = [dset.shape]
#                rows = shape[0]
#                if rows+100 < self.numExpectedPoints:
#                    shape[0] += 100
#                    self.h5Node['data'][key].extend(tuple(shape))
#                else:
#                    shape[0] = self.numExpectedPoints
#                    self.h5Node['data'][key].extend(tuple(shape))
#                self.h5Node['data'][key][i] = val
        finally:
            self.mutex.unlock()

    def appendDataPoint(self, data):
        if DEBUG: print "appending data point:", data['i']
        try:
            self.mutex.lock()

            maxshape = self.numExpectedPoints

            i = data['i']

            for key, val in data['positions'].iteritems():
                self._updateDataset(key, i, val)

            for key, val in data['scalars'].iteritems():
                # TODO: YUCK
                if key not in self.h5Node['data']:
                    if key not in ('epoch', 'i'):
                        self.appendNormalizationChannel(key)
                self._updateDataset(key, i, val)

            # TODO: YUCK
            try:
                for key, val in data['vortex'].iteritems():
                    if key == 'dtn':
                        key = 'vtxdtn'
                        if not key in self.h5Node['data']:
                            self.appendNormalizationChannel(key)
                    elif key == 'counts':
                        key = 'MCA'
                    else:
                        if not key in self.h5Node['data']:
                            self.appendNormalizationChannel(key)
                    self._updateDataset(key, i, val)
            except KeyError:
                pass

            # we do this last so we can emit a signal if this is the first point
            # TODO: YUCK
            self._updateDataset('i', i, i)

        finally:
            self.mutex.unlock()

    def getAvailableElements(self):
        try:
            self.mutex.lock()
            elements = self.h5Node['elementMaps']['fitArea'].listnames()
            elements.sort()
            return elements
        except h5py.h5.H5Error:
            return []
        finally:
            self.mutex.unlock()

    def getAverageMcaSpectrum(self, indices=[], id='MCA', normalization=None):
        if len(indices) > 0:
            try:
                self.mutex.lock()
                spectrum = self.h5Node['data'][id][indices[0], :]*0
                numIndices = len(indices)
                for index in indices:
                    result = self.h5Node['data'][id][index, :]
                    if normalization:
                        norm = self.h5Node['data'][normalization][index]
                        if normalization == 'Dead':
                            norm = (100-norm)/100
                        result /= numpy.where(norm==0, numpy.inf, norm)
                    spectrum += result
                return spectrum / len(indices)
            finally:
                self.mutex.unlock()

    def getElementMap(self, mapType, element, normalization=None):
        try:
            self.mutex.lock()
            try:
                elementMap = self.h5Node['elementMaps'][mapType][element].value
            except h5py.h5.H5Error:
                return numpy.zeros(self.scanShape)

            if normalization:
                norm = self.h5Node['data'][normalization].value
                if normalization == 'Dead':
                    norm = (100-norm)/100

                elementMap.flat[:len(norm)] /= numpy.where(norm==0, numpy.inf, norm)
            return elementMap
        finally:
            self.mutex.unlock()

    def getInvalidDataPoints(self, indices=None):
        mon, thresh = self.getSkipmode()
        try:
            self.mutex.lock()
            if mon and thresh:
                temp = self.h5Node['data'][mon][:]
                invalid = numpy.nonzero(temp < thresh)[0]
            else:
                invalid = []

            if indices is None: return invalid
            if len(indices): return [i for i in indices if i in invalid]
            else: return invalid
        finally:
            self.mutex.unlock()

    def getMcaSpectrum(self, index, id='MCA', normalization=None):
        try:
            self.mutex.lock()
            result = self.h5Node['data'][id][index]
            if normalization is not None:
                result /= self.h5Node['data'][normalization][index]
            return result
        finally:
            self.mutex.unlock()

    def getMcaChannels(self, id='MCA'):
        try:
            self.mutex.lock()
            return self.h5Node[id]['channels'].value
        finally:
            self.mutex.unlock()

    def _getNormalizationChannels(self):
        try:
            self.mutex.lock()
            channels = self.h5Node['data'].listnames()
            # TODO: This is a wart, to be fixed with better structuring of
            # files via nexus standard:
            try:
                channels.remove('MCA')
            except ValueError:
                pass

            return channels
        finally:
            self.mutex.unlock()

    def getPymcaConfig(self):
        try:
            self.mutex.lock()
            try:
                return ConfigDict(eval(self.h5Node.attrs['pymcaConfig']))
            except h5py.h5.AttrError:
                return None
        finally:
            self.mutex.unlock()

    def getValidDataPoints(self, indices=None):
        mon, thresh = self.getSkipmode()
        try:
            self.mutex.lock()
            if mon and thresh:
                temp = self.h5Node['data'][mon][:]
                valid = numpy.nonzero(temp > thresh)[0]
            else:
                valid = range(len(self.h5Node['data']['i']))

            if indices is None: return valid
            if len(indices): return [i for i in indices if i in valid]
            else: return valid
        finally:
            self.mutex.unlock()

    def isValidDataPoint(self, index):
        try:
            self.mutex.lock()
            mon, thresh = self.getSkipmode()
            if mon and thresh:
                return self.h5Node['data'][mon][index] > thresh
            else:
                return self.h5Node['data']['i'][index] == index
        finally:
            self.mutex.unlock()

    def initializeElementMaps(self, elements):
        try:
            self.mutex.lock()
            if 'elementMaps' in self.h5Node:
                del self.h5Node['elementMaps']

            elementMaps = self.h5Node.create_group('elementMaps')
            for mapType in ['fitArea', 'massFraction', 'sigmaArea']:
                mapGroup = elementMaps.create_group(mapType)
                for element in elements:
                    mapGroup.create_dataset(
                        element.replace(' ', ''),
                        data=numpy.zeros(self.scanShape, 'f')
                    )

            self.flush()
        finally:
            self.mutex.unlock()

    def setPymcaConfig(self, config):
        try:
            self.mutex.lock()
            self.h5Node.attrs['pymcaConfig'] = str(config)
        finally:
            self.mutex.unlock()

    def getSkipmode(self):
        try:
            self.mutex.lock()
            mon = self.h5Node['skipmode'].attrs['monitor']
            thresh = self.h5Node['skipmode'].attrs['threshold']
            return (mon, thresh)
        except h5py.h5.ArgsError:
            return (None, 0)
        finally:
            self.mutex.unlock()

#    def setSkipmode(self, monitor=None, thresh=0):
#        monitor = copy.copy(monitor)
#        thresh = copy.copy(thresh)
#        try:
#            self.mutex.lock()
#            self.h5Node._v_attrs.skipmodeMonitor = monitor
#            self.h5Node._v_attrs.skipmodeThresh = thresh
#        finally:
#            self.mutex.unlock()

    def updateElementMap(self, mapType, element, index, val):
        try:
            self.mutex.lock()
            try:
                self.h5Node['elementMaps'][mapType][element][tuple(index)] = val
            except ValueError:
                print index, node
        finally:
            self.mutex.unlock()


class XfsH5FileModel(H5FileModel):

    """
    """

    def _openFile(self, filename):
        return XfsH5File(filename, 'a', self)


class XfsH5FileInterface(H5FileInterface):

    def _setFileModel(self):
        self._fileModel = XfsH5FileModel(parent=self)
