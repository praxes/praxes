"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from SpecClient import SpecScan, SpecVariable, SpecConnectionsManager, \
    SpecEventsDispatcher, SpecWaitObject
from spectromicroscopy.smpcore import configutils, qtspeccommand, \
    qtspecvariable

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class QtSpecScanA(SpecScan.SpecScanA, QtCore.QObject):

    def __init__(self, specVersion = None):
        QtCore.QObject.__init__(self)
        SpecScan.SpecScanA.__init__(self, specVersion)
        self._resumeScan = qtspeccommand.QtSpecCommandA('scan_on', specVersion)
        self._datafile = qtspecvariable.QtSpecVariableA("DATAFILE",
                                                        specVersion)

    def connected(self):
        pass

    def disconnected(self):
        pass

    def newScan(self, scanParameters):
        scanParameters['datafile'] = os.path.split(self._datafile.getValue())[1]
        if DEBUG: print scanParameters
        self.emit(QtCore.SIGNAL("newScan(PyQt_PyObject)"), scanParameters)

    def newScanPoint(self, i, x, y, scanData):
        if DEBUG: print scanData
        self.emit(QtCore.SIGNAL("newScanIndex(int)"), i)
        self.emit(QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"), scanData)

    def resumeScan(self):
        self._resumeScan()

    def scanAborted(self):
        self.emit(QtCore.SIGNAL("scanAborted()"))

    def scanFinished(self):
        if DEBUG: print 'scan finished'
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

    def tseries(self, nbPoints, countTime):
        cmd = "tseries %d %f"%(nbPoints, countTime)
        self.emit(QtCore.SIGNAL("newTseries(PyQt_PyObject)"), [nbPoints])
        self._startScan(cmd)


class QtSpecScanMcaA(QtSpecScanA):

    def __init__(self, specVersion = None):
        QtSpecScanA.__init__(self, specVersion)
        self.mcaData = SpecVariable.SpecVariable("MCA_DATA",
                                                 specVersion, 
                                                 timeout=500)

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
        scanData['mcaData'] = self.mcaData.getValue().transpose()
        QtSpecScanA.newScanPoint(self, i, x, y, scanData)
