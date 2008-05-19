"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
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

logger = logging.getLogger('XPaXS.spec.client.scan')
DEBUG = False


class QtSpecScanA(SpecScan.SpecScanA, QtCore.QObject):

    def __init__(self, specVersion, parent=None):
        QtCore.QObject.__init__(self, parent)
        SpecScan.SpecScanA.__init__(self, specVersion)
        self._resumeScan = SpecCommand.SpecCommandA('scan_on', specVersion)

    def connected(self):
        pass

    def disconnected(self):
        pass

    def newScan(self, scanParameters):
        for key, value in scanParameters.iteritems():
            if ',' in value:
                if '.' in value:
                    temp = numpy.fromstring(value, sep=',', dtype='f')
                else:
                    temp = numpy.fromstring(value, sep=',', dtype='i')
                if len(temp) == value.count(','): value = temp
            else:
                try:
                    if ('e' in value) or ('.' in value):
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
            scanParameters[key] = value
        if DEBUG: print 'newScan:', scanParameters

    def newScanData(self, scanData):
        if DEBUG: print 'scanData:', scanData
        self.emit(QtCore.SIGNAL("newScanIndex(int)"), i)

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
        if DEBUG: print "newScanPoint:", scanData
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

