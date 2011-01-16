"""Helper module for managing scans"""

import copy
import cStringIO
import logging
import time
import tokenize
import types

import numpy as np

from SpecClient.SpecConnectionsManager import SpecConnectionsManager
from SpecClient import SpecCommand
from SpecClient import SpecEventsDispatcher
from SpecClient import SpecWaitObject


__author__ = 'Matias Guijarro (ESRF) / Darren Dale (CHESS)'
__version__ = 1


(TIMESCAN) = (16)

DEBUG = False


def _iterable(next, terminator):
    out = []
    token = next()
    while token[1] != terminator:
        out.append(_atom(next, token))
        token = next()
        if token[1] == ",":
            token = next()
    return out

def _dictable(next):
    out = []
    token = next()
    while token[1] != '}':
        k = _atom(next, token)
        token = next()
        token = next()
        v = _atom(next, token)
        out.append((k, v))
        token = next()
        if token[1] == ",":
            token = next()
    return dict(out)

def _atom(next, token):
    if token[1] == "(":
        return tuple(_iterable(next, ')'))
    if token[1] == "[":
        return list(_iterable(next, ']'))
    if token[1] == "{":
        return _dictable(next)
    if token[1] == "array":
        token = next()
        return np.array(*_iterable(next, ')'))
    elif token[0] is tokenize.STRING:
        return token[1][1:-1].decode("string-escape")
    elif token[0] is tokenize.NUMBER:
        try:
            return int(token[1], 0)
        except ValueError:
            return float(token[1])
    elif token[1] == "-":
        token = list(next())
        token[1] = "-" + token[1]
        return _atom(next, token)
    elif token[0] is tokenize.NAME:
        if token[1] == 'None':
            return None
        raise ValueError('tokenize NAME: %s unrecognized' % token[1])
    elif not token[0]:
        return
    for i, v in tokenize.__dict__.iteritems():
        if v == token[0]:
            raise ValueError("tokenize.%s unrecognized: %s" % (i, token[1]))

def simple_eval(source):
    """a safe version of the builtin eval function, """
    src = cStringIO.StringIO(source).readline
    src = tokenize.generate_tokens(src)
    return _atom(src.next, src.next())


class SpecScanA:

    @property
    def paused(self):
        # False when a scan is running or has completed normally
        return self.__status == 'paused'

    @property
    def ready(self):
        # False when a scan starts, only True once a scan completes normally
        return self.__status == 'ready'

    @property
    def scanning(self):
        # True when a scan is running, False when scan completes or is paused
        return self.__status == 'scanning'

    @property
    def specVersion(self):
        return self.__specVersion

    def __init__(self, specVersion = None):
        self.scanParams = {}
        self.scanCounterMne = None
        self.__status = 'ready'
        self.__specVersion = None

        if specVersion is not None:
            self.connectToSpec(specVersion)
        else:
            self.connection = None


    def connectToSpec(self, specVersion):
        self.connection = SpecConnectionsManager().getConnection(specVersion)
        self.__specVersion = specVersion

        SpecEventsDispatcher.connect(self.connection, 'connected',
                                     self.connected)
        SpecEventsDispatcher.connect(self.connection, 'disconnected',
                                     self.__disconnected)

        self.connection.registerChannel('status/ready', self.__statusReady,
                                    dispatchMode=SpecEventsDispatcher.FIREEVENT)
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
        self.__status = 'ready'
        self.scanParams = {}

        self.disconnected()


    def disconnected(self):
        pass


    def getScanType(self):
        try:
            return self.scanParams['scantype']
        except:
            return -1


    def isScanning(self):
        return self.scanning


    def __newScan(self, scanParams):
        if DEBUG: print "SpecScanA.__newScan", scanParams

        if not scanParams:
            if self.scanning:
                # receive 0 when scan ends normally
                self.__status = 'ready'
                self.scanFinished()
            return

        if not self.ready:
            # a new scan was started before the old one completed
            # lets provide an opportunity to clean up
            self.scanAborted()

        self.__status = 'scanning'

        self.scanParams = simple_eval(scanParams)

        if type(self.scanParams) != types.DictType:
            return

        self.newScan(self.scanParams)

        self.scanCounterMne = self.scanParams.get('counter')
        if (not self.scanCounterMne) or self.scanCounterMne == '?':
            logging.getLogger("SpecClient").error(
                                "No counter selected for scan.")
            self.scanCounterMne = None
            return

        self.scanStarted() # A.B


    def newScan(self, scanParameters):
        if DEBUG: print "SpecScanA.newScan", scanParameters
        pass


    def __newScanData(self, scanData):
        if DEBUG: print "SpecScanA.__newScanData", scanData
        if self.paused and scanData:
            self.__status = 'scanning'
            self.scanResumed()
        if self.scanning and scanData:
            scanData = simple_eval(scanData)

            self.newScanData(scanData)


    def newScanData(self, scanData):
        if DEBUG: print "SpecScanA.newScanData", scanData
        pass


    def __newScanPoint(self, scanData):
        if DEBUG: print "SpecScanA.__newScanPoint", scanData
        if self.paused and scanData:
            self.__status = 'scanning'
            self.scanResumed()
        if self.scanning and scanData:
            scanData = simple_eval(scanData)

            i = scanData['i']
            x = scanData['x']
            y = scanData[self.scanCounterMne]

            # hack to know if we should call newScanPoint with
            # scanData or not (for backward compatiblity)
            if len(self.newScanPoint.im_func.func_code.co_varnames) > 4:
              self.newScanPoint(i, x, y, scanData)
            else:
              self.newScanPoint(i, x, y)


    def newScanPoint(self, i, x, y, counters_value):
        if DEBUG: print "SpecScanA.newScanPoint", i, x, y, counters_value
        pass


    def abort(self):
        if self.isConnected and (self.scanning or self.paused):
            if self.scanning:
                self.connection.abort()
            self.__status = 'ready'
            self.scanAborted()


    def pause(self):
        if self.isConnected() and self.scanning:
            self.connection.abort()


    def resume(self):
        if self.isConnected() and self.paused:
            SpecCommand.SpecCommandA('scan_on', self.specVersion)()


    def scanAborted(self):
        pass


    def scanFinished(self):
        pass


    def scanPaused(self):
        pass


    def scanResumed(self):
        pass


    def scanStarted(self): # A.B
        pass # A.B


    def __statusReady(self, status):
        if status and self.scanning:
            self.__status = 'paused'
            self.scanPaused()


    def ascan(self, motorMne, startPos, endPos, nbPoints, countTime):
        if self.connection.isSpecConnected():
            cmd = "ascan %s %f %f %d %f" % (motorMne, startPos, endPos,
                                            nbPoints, countTime)
            self.connection.send_msg_cmd(cmd)
            return True
        else:
            return False
