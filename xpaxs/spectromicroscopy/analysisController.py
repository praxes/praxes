"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy
import os
import Queue
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore, QtGui # gui for testing only
from PyMca.FitParam import FitParamDialog
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import configutils
from xpaxs.spectromicroscopy.advancedfitanalysis import AdvancedFitThread

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False

filters = tables.Filters(complib='zlib', complevel=0)


class AnalysisController(QtCore.QObject):

    def __init__(self, scan, mutex, *args, **kwargs):
        QtCore.QObject.__init__(self)

        self.lock = QtCore.QReadWriteLock()
        self.mutex = mutex
        self.lastUpdate = time.time()

        self.scan = scan
        self.queue = Queue.Queue()

        self.h5file = scan._v_file
        try:
            elementMaps = self.h5file.getNode(scan, 'elementMaps')
        except tables.NoSuchNodeError:
            elementMaps = self.h5file.createGroup(scan, 'elementMaps')
            for i in ['PeakArea', 'MassFraction', 'SigmaArea']:
                self.h5file.createGroup(elementMaps, i)
            self.h5file.flush()

        if 'skipmodeMonitor' in scan.attrs:
            self._skipmodeEnabled = True
            self._skipmodeMonitor = scan.attrs.skipmodeMonitor
            self._skipmodeThresh = scan.attrs.skipmodeThresh
        else:
            self._skipmodeEnabled = False
            self._skipmodeMonitor = None
            self._skipmodeThresh = 0

        self._currentElement = None
        self._currentDataType = "PeakArea"
        self._pymcaConfig = None
        self._peaks = []
        self._normalizationChannel = None

        self.threads = []

        self.dirty = False

        self.fitParamDlg = FitParamDialog()

        try:
            self._pymcaConfig = scan.attrs.pymcaConfig
            self.resetPeaks()
        except AttributeError:
            pass

    def getScanAxis(self, axis=0, index=0):
        """some scans have multiple axes, some axes have multiple components"""
        try:
            return self.scan.attrs.scanAxes[axis][index]
        except IndexError, KeyError:
            return ''

    def appendDataPoint(self):
        raise NotImplementedError
        # TODO: use this for acquisition

    def getScanAxes(self):
        return self.scan.attrs.scanAxes

    def getDatafile(self):
        return self.scan.attrs.fileName

    def getNumScanLines(self):
        return len(self.scan.data)

    def getExpectedScanLines(self):
        return self.scan.attrs.scanLines

    def getElementMap(self, peak=None, datatype=None):
        if peak is None: peak = self._currentElement
        if datatype is None: datatype = self._currentDataType
        dataPath = '/'.join(['elementMaps', self._currentDataType,
                             self._currentElement])
        try:
            self.mutex.lock()
            try:
                elementMap = self.scan._v_file.getNode(self.scan, dataPath)[:]
            except NoSuchNodeError:
                return numpy.zeros(self.getScanShape())
        finally:
            self.mutex.unlock()
        if self._normalizationChannel:
            if self._normalizationChannel == 'Dead time %': temp = 'Dead'
            else: temp = self._normalizationChannel
            try:
                self.mutex.lock()
                norm = getattr(self.scan.data.cols, temp)[:]
            finally:
                self.mutex.unlock()
            if self._normalizationChannel == 'Dead time %': norm = 1-norm/100
            elementMap.flat[:len(norm)] /= norm
        return elementMap

    def getScanRange(self, axis):
        return self.scan.attrs.scanRange[axis]

    def getScanShape(self):
        return self.scan.attrs.scanShape

    def getNormalizationChannels(self):
        channels = [i for i in self.scan.data.colnames if not i in self.scan.attrs]
        channels.insert(0, 'Dead time %')
        return channels

    def setNormalizationChannel(self, channel):
        channel = str(channel)
        if channel == 'None': channel = None
        if not self._normalizationChannel == channel:
            self._normalizationChannel = channel
            elementMap = self.getElementMap()
            self.emit(QtCore.SIGNAL("elementDataChanged"), elementMap)


    def getPeaks(self):
        return self._peaks

    def getScanType(self):
        return self.scan.attrs.scanType

    def getScanDimensions(self):
        return len(self.scan.attrs.scanAxes)

    def processData(self):
        # TODO: This needs to be improved
        if self._pymcaConfig is None:
            self.getPymcaConfig()

        try:
            self.mutex.lock()
            l = len(self.scan.data)
        finally:
            self.mutex.unlock()

        for i in xrange(l):
            self.queue.put(i)

        config = copy.deepcopy(self._pymcaConfig)
#        thread = AdvancedFitThread(self.lock, self)
        thread = AdvancedFitThread(self.mutex, self)
        thread.initialize(config, self.scan, self.queue)
        self.threads.append(thread)
        self.connect(thread,
                     QtCore.SIGNAL('dataProcessed'),
                     self.dataUpdated)
        self.connect(thread,
                     QtCore.SIGNAL('finished()'),
                     self.finished)
        thread.start(QtCore.QThread.NormalPriority)

    def finished(self):
        self.emit(QtCore.SIGNAL('finished()'))

    def dataUpdated(self):
        self.dirty = True
        self.update()

    def update(self):
        elementMap = self.getElementMap()
        self.emit(QtCore.SIGNAL("elementDataChanged"), elementMap)

    def saveData(self):
        # TODO
        pass

    def setCurrentElement(self, element):
        element = str(element).replace(' ', '')
        if not self._currentElement == element:
            self._currentElement = element
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.getElementMap())

    def setCurrentDataType(self, datatype):
        datatype = str(datatype).replace(' ', '')
        if not self._currentDataType == datatype:
            self._currentDataType = datatype
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.getElementMap())

    def getPymcaConfig(self):
        self.fitParamDlg.exec_()
        self._pymcaConfig = self.fitParamDlg.getParameters()
        self.scan.attrs.pymcaConfig = self._pymcaConfig
        self.resetPeaks()
        self.emit(QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                  self._peaks)

    def resetPeaks(self):
        self._peaks = []
        for el, edges in self._pymcaConfig['peaks'].iteritems():
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

    def checkConcentrations(self):
        if 'concentrations' in self._pymcaConfig: return True
        else: return False

    def timeout(self):
        if self.dirty:
            self.emit(QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"), fitData)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.getElementMap())
            self.dirty = False
