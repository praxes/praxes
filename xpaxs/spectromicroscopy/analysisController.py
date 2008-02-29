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

def flat_to_nd(index, shape):
    res = []
    for i in xrange(1, len(shape)):
        p = numpy.product(shape[i:])
        res.append(index//p)
        index = index % p
    res.append(index)
    return tuple(res)


class AnalysisController(QtCore.QObject):

    def __init__(self, scan, *args, **kwargs):
        QtCore.QObject.__init__(self)

        self.lock = QtCore.QReadWriteLock()
        self.lastUpdate = time.time()

        self.scan = scan
        self.queue = Queue.Queue()
        for i in range(len(self.scan.data)):
            self.queue.put(i)

        # TODO: add a new group to store this information
        self._elementMaps = {"Peak Area": {},
                            "Mass Fraction": {},
                            "Sigma Area": {}}

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

        self.dataQue = []
        self.dirty = False

        self.fitParamDlg = FitParamDialog()

        try:
            self._pymcaConfig = scan.attrs.pymcaConfig
            self.resetPeaks()
        except AttributeError:
            self.getPymcaConfig()

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
            self.lock.lockForRead()
            elementMap = self.scan._v_file.getNode(self.scan, dataPath)[:]
        finally:
            self.lock.unlock()
        if self._normalizationChannel:
            if self._normalizationChannel == 'Dead time %': temp = 'Dead'
            else: temp = self._normalizationChannel
            try:
                self.lock.lockForRead()
                norm = getattr(self.scan.data.cols, temp)[:]
            finally:
                self.lock.unlock()
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

    def dispatch(self):
        while self.threads:
            thread = self.threads.pop(0)
            try:
                index = self.queue.pop(0)
                row = self.scan.data[index]
                thread.initialize(index, row)
                if self._skipmodeEnabled:
                    if row[self._skipmodeMonitor] > self._skipmodeThresh:
                        thread.start(QtCore.QThread.HighestPriority)
                else:
                    thread.start(QtCore.QThread.HighestPriority)
            except IndexError:
                pass

    def processData(self):
        config = copy.deepcopy(self._pymcaConfig)
        thread = AdvancedFitThread(self.lock, self)
        thread.initialize(config, self.scan, self.queue)
        self.threads.append(thread)
        self.connect(thread,
                     QtCore.SIGNAL('dataProcessed'),
                     self.dataUpdated)
        thread.start(QtCore.QThread.NormalPriority)
#        QtGui.qApp.processEvents()
#        self.dispatch()

    def dataUpdated(self):
        self.dirty = True
        self.update()

    def update(self):
        # TODO: wire this to a QTimer
        now = time.time()
        elapsed = now-self.lastUpdate
        print elapsed
        if elapsed > 1:
            elementMap = self.getElementMap()
            self.emit(QtCore.SIGNAL("elementDataChanged"), elementMap)
            self.lastUpdate = time.time()

#    def newScanPoint(self, i, x, y, scanData):
#        scanData['i'] = i
#        scanData['x'] = x
#        scanData['y'] = y
#        # update progressBars:
#        self.emit(QtCore.SIGNAL("newScanIndex(int)"), i)
#
#
#        skipmodeStatus=self.settings.value('skipmode/enabled').toBool()
#        counter="%s"%self.settings.value('skipmode/counter').toString()
#        threshold=self.settings.value('skipmode/threshold').toFloat()
#        scanData['pointSkipped'] = skipmodeStatus and \
#                (scanData[counter ] <= threshold)
#
#        deadtimeCorrection=self.settings.value('DeadTimeCorrection').toBool()
#
#        pointSkipped = skipmodeStatus and \
#                (scanData[counter ] <= threshold)
#
#        if not pointSkipped:
#            if deadtimeCorrection:
#                try:
#                    scanData['mcaCounts'][1] *= 100./(100-float(scanData['dead']))
#                except KeyError:
#                    if DEBUG: print 'deadtime not corrected. A counter reporting '\
#                        'the percent dead time, called "Dead", must be created in '\
#                        'Spec for this feature to work.'
#
#        self.dataQue.append(scanData)
#        self.dispatch()
            # thread = self.threads.pop(0)
            # processed = thread.process(scanData)

    def updateProcessedData(self, processedData):
        thread = self.sender()
        self.threads.append(thread)
        # TODO: This method is basically pseudocode at the moment
        index = flat_to_nd(processedData['index'], self.getScanShape())
        for group in processedData['groups']:
            peakArea = self.scan._v_file.getNode(self.scan.elementMaps.PeakArea,
                                                 group.replace(' ', ''))
            peakArea[index] = processedData[group]['fitarea']
            area = processedData[group]['fitarea']
            if not area: area = numpy.nan
            sigmaArea = self.scan._v_file.getNode(self.scan.elementMaps.SigmaArea,
                                                  group.replace(' ', ''))
            sigmaArea[index] = processedData[group]['sigmaarea']/area

        if 'concentrations' in processedData:
            for key, val in processedData['concentrations']['mass fraction'].iteritems():
                mf = self.scan._v_file.getNode(self.scan.elementMaps.MassFraction,
                                               key.replace(' ', ''))
                mf[index] = val

        now = time.time()
        elapsed = now-self.lastUpdate
#        print elapsed
        if elapsed > 0:
            elementMap = self.getElementMap()
            self.emit(QtCore.SIGNAL("elementDataChanged"), elementMap)
            self.emit(QtCore.SIGNAL("newMcaFit"), processedData['mcaFit'])
            self.lastUpdate = time.time()

#        self.threads.append(thread)
        self.dispatch()

#    def scanFinished(self):
#        self.emit(QtCore.SIGNAL("scanFinished()"))

#    def scanStarted(self):
#        if DEBUG: print 'scan started'
#        self.emit(QtCore.SIGNAL("scanStarted()"))

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


class AcquisitionAnalysisController(AnalysisController):

    def __init__(self, scan, **kwargs):
        QtSpecScan.__init__(self)

        self.initScanData(scan)

    def initScanData(self, scan):
        self._specscan = scan
        self._datafile = scan.fileheader('F')[0].split()[1]
        self._scannum = scan.number()
        self._command = scan.command()
        if self._command.split()[0] == 'mesh':
            self._scantype = '2D'
            self._scanAxes = (scan.alllabels()[0], scan.alllabels()[1])
            self._scanExtent = (scan.datacol(1)[0], scan.datacol(1)[-1],
                                scan.datacol(2)[0], scan.datacol(2)[-1])
            self._scanShape = (len(scan.datacol(1)), len(scan.datacol(2)))
        else:
            self._scantype = '1D'
            self._scanAxes = (scan.alllabels()[0], )
            self._scanExtent = (scan.datacol(1)[0], scan.datacol(1)[-1])
            self.scanShape = (len(scan.datacol(1)), )

        self.initElementMaps()
