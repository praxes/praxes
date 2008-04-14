"""Helper module for managing scans"""
from SpecClient.SpecConnectionsManager import SpecConnectionsManager
from SpecClient import SpecCommand
from SpecClient import SpecEventsDispatcher
from SpecClient import SpecWaitObject
import logging
import types
import time
import numpy

import copy

__author__ = 'Matias Guijarro'
__version__ = 1


(TIMESCAN) = (16)

DEBUG = False


class SpecScanA:
    def __init__(self, specVersion = None):
        self.scanParams = {}
        self.scanCounterMne = None
        self.__scanning = False

        if specVersion is not None:
            self.connectToSpec(specVersion)
        else:
            self.connection = None

    def connectToSpec(self, specVersion):
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

    def __newScan(self, newscan):
        if DEBUG: print "SpecScanA.__newScan", newscan
        if not newscan:
            if self.__scanning:
                self.scanFinished()
                self.__scanning = False
            return

        self.__scanning = False

        self.scanParams = SpecWaitObject.waitReply(self.connection,
                                                   'send_msg_chan_read',
                                                   ('var/_SC_SCANENV', ))

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
        try:
            return self.scanParams['scantype']
        except:
            return -1

    def newScan(self, scanParameters):
        if DEBUG: print "SpecScanA.newScan", scanParameters
        pass

    def __newScanData(self, newScanData):
        if DEBUG: print "SpecScanA.__newScanData", newScanData
        if self.__scanning:
            scanData = SpecWaitObject.waitReply(self.connection,
                                                'send_msg_chan_read',
                                                ('var/_SC_SCANDATA', ))

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

    def __newScanPoint(self, newScanPoint):
        if DEBUG: print "SpecScanA.__newScanPoint", newScanPoint
        if self.__scanning:
            scanData = SpecWaitObject.waitReply(self.connection,
                                                'send_msg_chan_read',
                                                ('var/_SC_PLOTDATA', ))

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

    def newScanPoint(self, i, x, y, counters_value):
        if DEBUG: print "SpecScanA.newScanPoint", i, x, y, counters_value
        pass

    def scanFinished(self):
        pass

    def scanStarted(self): # A.B
        pass # A.B

    def ascan(self, motorMne, startPos, endPos, nbPoints, countTime):
        if self.connection.isSpecConnected():
            cmd = "ascan %s %f %f %d %f" % (motorMne, startPos, endPos,
                                            nbPoints, countTime)
            self.connection.send_msg_cmd(cmd)
            return True
        else:
            return False
