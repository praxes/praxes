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

from xpaxs.instrumentation.spec import TEST_SPEC

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.instrumentation.spec.client.scan')



class QtSpecScanBase(SpecScan.SpecScanA, QtCore.QObject):

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
        logger.debug('newScan: %s', scanParameters)

    def newScanData(self, scanData):
        logger.debug( 'scanData: %s', scanData)
        self.emit(QtCore.SIGNAL("newScanIndex(int)"), i)

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
        logger.debug( "newScanPoint: %s", scanData)
        self.emit(QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"), scanData)

    def resumeScan(self):
        logger.info('Scan Resumed')
        self._resumeScan()

    def scanAborted(self):
        logger.info('Scan Aborted')
        self.emit(QtCore.SIGNAL("scanAborted()"))
        self.scanFinished()

    def scanFinished(self):
        logger.info( 'scan finished')
        # TODO: save data!
        self.emit(QtCore.SIGNAL("scanFinished()"))

    def scanStarted(self):
        logger.info( 'scan started')
        self.emit(QtCore.SIGNAL("scanStarted()"))

    def _startScan(self, cmd):
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd(cmd)
            return True
        else:
            return False

    def ascan(self, *args):
        cmd = "ascan %s %f %f %d %f"%args
        logger.debug(cmd)
        self.emit(QtCore.SIGNAL("newAscan(PyQt_PyObject)"), args[:-1])
        self._startScan(cmd)

    def a2scan(self, *args):
        cmd = "a2scan %s %f %f \
                      %s %f %f \
                      %d %f"%args
        logger.debug(cmd)
        self.emit(QtCore.SIGNAL("newA2scan(PyQt_PyObject)"), args[:-1])
        self._startScan(cmd)

    def a3scan(self, *args):
        cmd = "a3scan %s %f %f \
                      %s %f %f \
                      %s %f %f \
                      %d %f"%args
        logger.debug(cmd)
        self.emit(QtCore.SIGNAL("newA3scan(PyQt_PyObject)"), args[:-1])
        self._startScan(cmd)

    def mesh(self, *args):
        cmd = "mesh %s %f %f %d \
                    %s %f %f %d \
                    %f"%args
        logger.debug(cmd)
        self.emit(QtCore.SIGNAL("newMesh(PyQt_PyObject)"), args[:-1])
        self.emit(QtCore.SIGNAL("xAxisLabel(PyQt_PyObject)"), args[0])
        self.emit(QtCore.SIGNAL("xAxisLims(PyQt_PyObject)"), args[1:3])
        self.emit(QtCore.SIGNAL("yAxisLabel(PyQt_PyObject)"), args[4])
        self.emit(QtCore.SIGNAL("yAxisLims(PyQt_PyObject)"), args[5:7])
        self._startScan(cmd)



class TestQtSpecScanA(QtSpecScanBase):

    def __init__(self, specVersion, parent=None):
        pass
        #QtCore.QObject.__init__(self, parent)
        #SpecScan.SpecScanA.__init__(self)#, specVersion)

    def newScan(self, scanParameters):
        pass
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
        logger.debug('newScan: %s', scanParameters)


    def _startScan(self, cmd):
        return True
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd(cmd)
            return True
        else:
            return False

    def __newScanPoint(self, scanData):
        return
        if DEBUG: print "SpecScanA.__newScanPoint", scanData
        if self.__scanning and scanData:
            scanData = dict([i.split("=", 1)
                             for i in scanData.rstrip("\t").split("\t")])

            for key, value in scanData.iteritems():
                if ',' in value:
                    if '.' in value:
                        value = numpy.fromstring(value, sep=',', dtype='f')
                    else:
                        value = numpy.fromstring(value, sep=',', dtype='i')
                else:
                    value = float(value)
                scanData[key] = value

                if key == "i": i = value
                elif key == "x": x = value
                elif key == self.scanCounterMne: y = value

            # hack to know if we should call newScanPoint with
            # scanData or not (for backward compatiblity)
            if len(self.newScanPoint.im_func.func_code.co_varnames) > 4:
              self.newScanPoint(i, x, y, scanData)
            else:
              self.newScanPoint(i, x, y)

    def connectToSpec(self, specVersion):
        return
        self.connection = SpecConnectionsManager().getConnection(specVersion)

        SpecEventsDispatcher.connect(self.connection, 'connected',
                                     self.connected)
        SpecEventsDispatcher.connect(self.connection, 'disconnected',
                                     self.__disconnected)

        self.connection.registerChannel('var/_SC_NEWSCAN', self.__newScan,
                                    dispatchMode=SpecEventsDispatcher.FIREEVENT)
        self.connection.registerChannel('var/_SC_NEWPLOTDATA',
                                    self.__newScanPoint,
                                    dispatchMode=SpecEventsDispatcher.FIREEVENT)
        self.connection.registerChannel('var/_SC_NEWSCANDATA',
                                    self.__newScanData,
                                    dispatchMode=SpecEventsDispatcher.FIREEVENT)

        if self.connection.isSpecConnected():
            self.connected()

    def isConnected(self):
        return QtCore.QObject() and True
        return self.connection and self.connection.isSpecConnected()

    def connected(self):
        pass

    def __disconnected(self):
        self.scanCounterMne = None
        self.__scanning = False
        self.scanParams = {}

        self.disconnected()

    def disconnected(self):
        pass

    def __newScan(self, scanParams):
        return

        if DEBUG: print "SpecScanA.__newScan", scanParams
        if not scanParams:
            if self.__scanning:
                self.scanFinished()
                self.__scanning = False
            return

        self.__scanning = False

        self.scanParams = dict([i.split("=", 1)
                                for i in scanParams.rstrip("\t").split("\t")])

        if type(self.scanParams) != types.DictType:
            return

        self.newScan(self.scanParams)

        self.scanCounterMne = self.scanParams.get('counter')
        if (not self.scanCounterMne) or self.scanCounterMne == '?':
            logging.getLogger("SpecClient").error(
                                "No counter selected for scan.")
            self.scanCounterMne = None
            return

        self.__scanning = True
        self.scanStarted() # A.B

    def getScanType(self):
        return 'mesh'
        try:
            return self.scanParams['scantype']
        except:
            return -1

    def newScan(self, scanParameters):
        if DEBUG: print "SpecScanA.newScan", scanParameters
        pass

    def __newScanData(self, scanData):
        if DEBUG: print "SpecScanA.__newScanData", scanData
        return
        if self.__scanning and scanData:
            scanData = dict([i.split("=", 1)
                             for i in scanData.rstrip("\t").split("\t")])

            for key, value in scanData.iteritems():
                if ',' in value:
                    if '.' in value:
                        value = numpy.fromstring(value, sep=',', dtype='f')
                    else:
                        value = numpy.fromstring(value, sep=',', dtype='i')
                else:
                    value = float(value)
                scanData[key] = value

            self.newScanData(copy.deepcopy(scanData))

    def newScanData(self, scanData):
        if DEBUG: print "SpecScanA.newScanData", scanData
        pass


if TEST_SPEC:
    class QtSpecScanA(TestQtSpecScanA):
        pass
else:
    class QtSpecScanA(QtSpecScanBase):
        pass

