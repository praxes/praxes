"""Helper module for managing scans"""
import SpecConnectionsManager
import SpecEventsDispatcher
import SpecWaitObject
import logging
import types
import time

__author__ = 'Matias Guijarro'
__version__ = 1


(TIMESCAN) = (16)


class SpecScanA:
    def __init__(self, specVersion = None):
        self.scanParams = {}
        self.scanCounterMne = None
        self._scanning = False

        if specVersion is not None:
            self.connectToSpec(specVersion)
        else:
            self.connection = None

    def connectToSpec(self, specVersion):
        connectionsManager = SpecConnectionsManager.SpecConnectionsManager()
        self.connection = connectionsManager.getConnection(specVersion)
        SpecEventsDispatcher.connect(self.connection,
                                     'connected',
                                     self.connected)
        SpecEventsDispatcher.connect(self.connection,
                                     'disconnected',
                                     self._disconnected)

        self.connection.registerChannel('var/_SC_NEWSCAN', self._newScan)
        self.connection.registerChannel('var/_SC_SCANDATALINE',
                                        self._newScanPoint,
                                        dispatchMode=\
                                            SpecEventsDispatcher.FIREEVENT)
                    
        if self.connection.isSpecConnected():
            self.connected()

    def isConnected(self):
        return self.connection and self.connection.isSpecConnected()

    def connected(self):
        pass

    def _disconnected(self):
        self.scanCounterMne = None
        self._scanning = False
        self.scanParams = {}
        
        self.disconnected()

    def disconnected(self):
        pass

    def _newScan(self, newscan):
        if not newscan:
            if self._scanning:
                self.scanFinished()
                self._scanning = False
            return

        self._scanning = False
            
        self.scanParams = SpecWaitObject.waitReply(self.connection,
                                                   'send_msg_chan_read',
                                                   ('var/_SC_SCANENV', ))

        if type(self.scanParams) != types.DictType:
            return

        self.newScan(self.scanParams)

        self.scanCounterMne = self.scanParams['counter']
        if len(self.scanCounterMne) == 0 or self.scanCounterMne == '?':
            logging.getLogger("SpecClient").error("No counter selected for scan.")
            self.scanCounterMne = None
            return
                
        self._scanning = True
        self.scanStarted() # A.B

    def getScanType(self):
        try:
            return self.scanParams['scantype']
        except:
            return -1

    def newScan(self, scanParameters):
        print scanParameters

    def _newScanPoint(self, scanDataString):
        if self._scanning:
            scanData = {}

            for elt in scanDataString.split():
                key, value = elt.split('=')
                scanData[key]=float(value)

            i = scanData["i"]
            x = scanData["x"]
            y = scanData[self.scanCounterMne]
            
            self.newScanPoint(i, x, y)

    def newScanPoint(self, i, x, y):
        pass #print i, (x, y)            

    def scanFinished(self):
        pass

    def scanStarted(self): # A.B
        pass # A.B

    def ascan(self, motorMne, startPos, endPos, nbPoints, countTime):
        if self.connection.isSpecConnected():
            cmd = "ascan %s %f %f %d %f"%(motorMne, startPos, endPos,
                                          nbPoints, countTime)
            self.connection.send_msg_cmd(cmd)
            return True
        else:
            return False
