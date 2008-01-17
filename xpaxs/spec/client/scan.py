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


class QtSpecScanA(SpecScan.SpecScanA, QtCore.QObject):

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

