"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore
from SpecClient import SpecScan, SpecCommand, SpecConnectionsManager, \
    SpecEventsDispatcher, SpecWaitObject

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import configutils

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class QtSpecScan(QtCore.QObject):

    def __init__(self, *args, **kwargs):
        QtCore.QObject.__init__(self)

        self._datafile = None
        self._scantype = None
        self._command = None
        self._scanAxes = []
        self._scanExtent = []
        self._scanShape = ()

        self._peaks = []
        self._elementMaps = {"Peak Area": {},
                            "Mass Fraction": {},
                            "Sigma Area": {}}

        self._currentElement = None
        self._currentDataType = "Peak Area"
        self._pymcaConfig = None

        self.dataQue = []
        self.dirty = False

        self.setPymcaConfig(kwargs.get('pymcaConfig', None))

    def getAxisName(self, index=0):
        return self._scanAxes[index]

    def getDatafile(self):
        return self._datafile

    def getElementMap(self, peak=None, datatype=None):
        if peak is None: peak = self._currentElement
        if datatype is None: datatype = self._currentDataType
        return self._elementMaps[datatype][peak]

    def getExtent(self):
        return self._scanExtent

    def getPeaks(self):
        return self._peaks

    def getScanType(self):
        return self._scantype

    def initElementMaps(self):
        for datatype in self._elementMaps:
            for peak in self._peaks:
                if not peak in self._elementMaps[datatype]:
                    self._elementMaps[datatype][peak] = \
                        numpy.zeros(self._scanShape, dtype=numpy.float_)

    def newScan(self, scanParameters):
        pass

    def dispatch(self):
        if len(self.threads) > 0 and len(self.dataQue) > 0:
            thread = self.threads.pop(0)
            data = self.dataQue.pop()
            thread.process(data)

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
        # update progressBars:
        self.emit(QtCore.SIGNAL("newScanIndex(int)"), i)


        skipmodeStatus=self.settings.value('skipmode/enabled').toBool()
        counter="%s"%self.settings.value('skipmode/counter').toString()
        threshold=self.settings.value('skipmode/threshold').toFloat()
        scanData['pointSkipped'] = skipmodeStatus and \
                (scanData[counter ] <= threshold)

        deadtimeCorrection=self.settings.value('DeadTimeCorrection').toBool()

        pointSkipped = skipmodeStatus and \
                (scanData[counter ] <= threshold)

        if not pointSkipped:
            if deadtimeCorrection:
                try:
                    scanData['mcaCounts'][1] *= 100./(100-float(scanData['dead']))
                except KeyError:
                    if DEBUG: print 'deadtime not corrected. A counter reporting '\
                        'the percent dead time, called "Dead", must be created in '\
                        'Spec for this feature to work.'

        self.dataQue.append(scanData)
        self.dispatch()
            # thread = self.threads.pop(0)
            # processed = thread.process(scanData)

    def updateProcessedData(self, processedData):
        # TODO: This method is basically pseudocode at the moment
        for group in result['groups']:
            self.elementMaps["Peak Area"][group].flat[index] = \
                result[group]['fitarea']
            area = numpy.where(result[group]['fitarea']==0,
                               numpy.nan,
                               result[group]['fitarea'])
            self.elementMaps["Sigma Area"][group].flat[index] = \
                result[group]['sigmaarea']/area

        if 'concentrations' in self._pymcaConfig:
            for group in concentrations['mass fraction'].keys():
                self.elementMaps["Mass Fraction"][group].flat[index] = \
                    concentrations['mass fraction'][group]
        self.dirty = True
        self.threads.append(thread)
        # emit a signal so we can dispatch
        self.emit(QtCore.SIGNAL('dataProcessed'))

#    def scanFinished(self):
#        self.emit(QtCore.SIGNAL("scanFinished()"))

#    def scanStarted(self):
#        if DEBUG: print 'scan started'
#        self.emit(QtCore.SIGNAL("scanStarted()"))

    def saveData(self):
        # TODO
        pass

    def setCurrentElement(self, element):
        if not self._currentElement == str(element):
            self._currentElement = str(element)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.getElementMap())

    def setCurrentDataType(self, datatype):
        if not self._currentDataType == str(datatype):
            self._currentDataType = str(datatype)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.getElementMap())

    def setPymcaConfig(self, config=None):
        if not config:
            config = configutils.getPymcaConfig()
        self._pymcaConfig = config
        self._peaks = []
        for el, edges in self._pymcaConfig['peaks'].iteritems():
            for edge in edges:
                self._peaks.append(' '.join([el, edge]))
        self._peaks.sort()
        if self._currentElement is None:
            self._currentElement = self._peaks[0]
        self.emit(QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                  self._peaks)

    def checkConcentrations(self):
        if 'concentrations' in self._pymcaConfig: return True
        else: return False

    def timeout(self):
        if self.dirty:
            self.emit(QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"), fitData)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.getElementMap())
            self.dirty = False


class QtSpecFileScan(QtSpecScan):

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


class QtSpecScanAcqusition(SpecScan.SpecScanA, QtCore.QObject):

    def __init__(self, *args, **kwargs):
        QtCore.QObject.__init__(self)
        SpecScan.SpecScanA.__init__(self, kwargs.get('specVersion', None))
        self._resumeScan = SpecCommand.SpecCommandA('scan_on', specVersion)
        # TODO: this is no longer necessary, get it from scanParams
#        self._datafile = qtspecvariable.QtSpecVariableA("DATAFILE",
#                                                        specVersion)
# TODO: all of these should go in the SpecScanAcquisition constructor
#        self.connect(self.specRunner.scan,
#                     QtCore.SIGNAL("newMesh(PyQt_PyObject)"),
#                     self.newScanAnalysis2D)
#        self.connect(self.specRunner.scan,
#                     QtCore.SIGNAL("newTseries(PyQt_PyObject)"),
#                     self.newScanAnalysis1D)
#        self.connect(self.specRunner.scan,
#                     QtCore.SIGNAL("newAscan(PyQt_PyObject)"),
#                     self.newScanAnalysis1D)
#        self.connect(self.specRunner.scan,
#                     QtCore.SIGNAL("newA2scan(PyQt_PyObject)"),
#                     self.newScanAnalysis1D)
#        self.connect(self.specRunner.scan,
#                     QtCore.SIGNAL("newA3scan(PyQt_PyObject)"),
#                     self.newScanAnalysis1D)
#        self.connect(self.specRunner.scan,
#                     QtCore.SIGNAL("newScan(PyQt_PyObject)"),
#                     self.setTabLabel)

    def connected(self):
        pass

    def disconnected(self):
        pass

    def newScan(self, scanParameters):
        scanParameters['datafile'] = os.path.split(self._datafile.getValue())[1]
        if DEBUG: print scanParameters
        self.emit(QtCore.SIGNAL("newScan(PyQt_PyObject)"), scanParameters)

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
        if DEBUG: print i
        self.emit(QtCore.SIGNAL("newScanIndex(int)"), i)
        self.emit(QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"), scanData)

    def resumeScan(self):
        self._resumeScan()

    def scanAborted(self):
        self.emit(QtCore.SIGNAL("scanAborted()"))

    def scanFinished(self):
        if DEBUG: print 'scan finished'
        # TODO: save data!
        self.emit(QtCore.SIGNAL("scanFinished()"))

    def scanStarted(self):
        if DEBUG: print 'scan started'
        self.emit(QtCore.SIGNAL("scanStarted()"))

    def _startScan(self, cmd):
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd(cmd)
            return True
        else:
            return False

    def ascan(self, *args):
        cmd = "ascan %s %f %f %d %f"%args
        self.emit(QtCore.SIGNAL("newAscan(PyQt_PyObject)"), args[:-1])
        self._startScan(cmd)

    def a2scan(self, *args):
        cmd = "a2scan %s %f %f \
                      %s %f %f \
                      %d %f"%args
        self.emit(QtCore.SIGNAL("newA2scan(PyQt_PyObject)"), args[:-1])
        self._startScan(cmd)

    def a3scan(self, *args):
        cmd = "a3scan %s %f %f \
                      %s %f %f \
                      %s %f %f \
                      %d %f"%args
        self.emit(QtCore.SIGNAL("newA3scan(PyQt_PyObject)"), args[:-1])
        self._startScan(cmd)

    def mesh(self, *args):
        cmd = "mesh %s %f %f %d \
                    %s %f %f %d \
                    %f"%args
        self.emit(QtCore.SIGNAL("newMesh(PyQt_PyObject)"), args[:-1])
        self.emit(QtCore.SIGNAL("xAxisLabel(PyQt_PyObject)"), args[0])
        self.emit(QtCore.SIGNAL("xAxisLims(PyQt_PyObject)"), args[1:3])
        self.emit(QtCore.SIGNAL("yAxisLabel(PyQt_PyObject)"), args[4])
        self.emit(QtCore.SIGNAL("yAxisLims(PyQt_PyObject)"), args[5:7])
        self._startScan(cmd)

