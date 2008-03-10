"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy
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

from xpaxs.datalib.hdf5.xpaxsdatainterface import XpaxsScanInterface

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class SmpScanInterface(XpaxsScanInterface):

    def __init__(self, scan, mutex, *args, **kwargs):
        super(SmpScanInterface, self).__init__(self, scan, mutex,
                                               *args, **kwargs)

        try:
            self.mutex.lock()
            elementMaps = self.h5file.getNode(scan, 'elementMaps')
        except tables.NoSuchNodeError:
            elementMaps = self.h5file.createGroup(scan, 'elementMaps')
            for i in ['PeakArea', 'MassFraction', 'SigmaArea']:
                self.h5file.createGroup(elementMaps, i)
            self.h5file.flush()
        finally:
            self.mutex.unlock()

        if 'skipmodeMonitor' in self.scan._v_attrs:
            self.skipmodeEnabled = True
            self.skipmodeMonitor = scan.attrs.skipmodeMonitor
            self.skipmodeThresh = scan.attrs.skipmodeThresh
        else:
            self.skipmodeEnabled = False

        self._currentElement = None
        self._currentDataType = "PeakArea"
        self._pymcaConfig = None
        self._peaks = []
        self._normalizationChannel = None

    def getScanAxis(self, axis=0, index=0):
        """some scans have multiple axes, some axes have multiple components"""
        try:
            return self.scan._v_attrs.scanAxes[axis][index]
        except IndexError, KeyError:
            return ''

    def appendDataPoint(self):
        raise NotImplementedError
        # TODO: use this for acquisition

    def getScanAxes(self):
        return self.scan._v_attrs.scanAxes

    def getDatafile(self):
        return self.scan._v_attrs.fileName

    def getNumScanLines(self):
        return len(self.scan.data)

    def getExpectedScanLines(self):
        return self.scan._v_attrs.scanLines

    def getElementMap(self, element, datatype, normalization=None):
        dataPath = '/'.join(['elementMaps', datatype, element])
        try:
            self.mutex.lock()
            try:
                elementMap = self.scan._v_file.getNode(self.scan, dataPath)[:]
            except NoSuchNodeError:
                return numpy.zeros(self.getScanShape())
        finally:
            self.mutex.unlock()
        if normalization:
            # TODO: this if is a wart:
            if normalization == 'Dead time %':
                try:
                    self.mutex.lock()
                    norm = getattr(self.scan.data.cols, 'Dead')[:]
                finally:
                    self.mutex.unlock()
                norm = 1-norm/100
            else:
                try:
                    self.mutex.lock()
                    norm = getattr(self.scan.data.cols, normalization)[:]
                finally:
                    self.mutex.unlock()
            elementMap.flat[:len(norm)] /= norm
        return elementMap

    def getScanRange(self, axis):
        return self.scan._v_attrs.scanRange[axis]

    def getScanShape(self):
        return self.scan._v_attrs.scanShape

    def getNormalizationChannels(self):
        channels = [i for i in self.scan.data.colnames if not i in self.scan._v_attrs]
        channels.insert(0, 'Dead time %')
        return channels

    def getPeaks(self):
        return self._peaks

    def getScanType(self):
        return self.scan._v_attrs.scanType

    def getScanDimensions(self):
        return len(self.scan._v_attrs.scanAxes)

    def setSkipmode(self, monitor, thresh):
        try:
            self.mutex.lock()
            scan._v_attrs.skipmodeMonitor = monitor
            scan._v_attrs.skipmodeThresh = thresh
        finally:
            self.mutex.unlock()

    def dataUpdated(self):
        self.dirty = True
        self.update()

    def updateElementMap(self, mapType, element, index, val):
        node = '/'.join([mapType, element])
        try:
            self.mutex.lock()
            try:
                self.h5file.getNode(self.scan, node)[index] = val
            except ValueError:
                print index, node
        finally:
            self.mutex.unlock()


    def resetPeaks(self, pymcaConfig):
        # TODO: this needs to be thread safe!
        self._peaks = []
        for el, edges in pymcaConfig['peaks'].iteritems():
            for edge in edges:
                name = ' '.join([el, edge])
                self._peaks.append(name)
                for i in ['PeakArea', 'MassFraction', 'SigmaArea']:
                    node = self.h5file.getNode(self.scan.elementMaps, i)
                    h5Name = name.replace(' ', '')
                    if not h5Name in node:
                        self.h5file.createCArray(node, h5Name,
                                                 tables.Float32Atom(),
                                                 self.getScanShape(),
                                                 filters=filters)
        self._peaks.sort()
        if self._currentElement is None:
            self._currentElement = self._peaks[0].replace(' ', '')

        self.emit(QtCore.SIGNAL("availablePeaks"), self._peaks)


