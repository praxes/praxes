"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.external.SpecClient import SpecScan

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class QtSpecScanA(SpecScan.SpecScanA, QtCore.QObject):

    def __init__(self, specVersion = None):
        QtCore.QObject.__init__(self)
        SpecScan.SpecScanA.__init__(self, specVersion)
        

    def connected(self):
        pass

    def disconnected(self):
        pass

    def getScanType(self):
        try:
            return self.scanParams['scantype']
        except:
            return -1

    def newScan(self, scanParameters):
        print scanParameters

    def __newScan(self, newscan):
#        print newscan
        if not newscan:
            if self.__scanning:
                self.scanFinished()
                self.__scanning = False
            return

        self.__scanning = False
            
        self.scanParams = SpecWaitObject.waitReply(self.connection, 'send_msg_chan_read', ('var/_SC_SCANENV', ))

        if type(self.scanParams) != types.DictType:
            return

        self.newScan(self.scanParams)

        self.scanCounterMne = self.scanParams['counter']
        if len(self.scanCounterMne) == 0 or self.scanCounterMne == '?':
            logging.getLogger("SpecClient").error("No counter selected for scan.")
            self.scanCounterMne = None
            return
                
        self.__scanning = True
        self.scanStarted() # A.B

    def __newScanPoint(self, scanDataString):
        if self.__scanning:
            scanData = {}

            for elt in scanDataString.split():
                key, value = elt.split('=')
                scanData[key]=float(value)

            i = scanData["i"]
            x = scanData["x"]
            y = scanData[self.scanCounterMne]
            
            self.newScanPoint(i, x, y)

    def newScanPoint(self, i, x, y):
        print i, (x, y)

    def scanFinished(self):
        pass

    def scanStarted(self): # A.B
        pass # A.B

    def ascan(self, motorMne, startPos, endPos, nbPoints, countTime):
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd("ascan %s %f %f %d %f" % (motorMne, startPos, endPos, nbPoints, countTime))
            return True
        else:
            return False

    def abort(self):
        if self.connection is None or not self.connection.isSpecConnected():
            return
        
        self.connection.abort()
