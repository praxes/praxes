"""
"""






#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys
import logging
import types
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.external.SpecClient import SpecScan, \
    SpecConnectionsManager, SpecEventsDispatcher, SpecWaitObject
from spectromicroscopy.smpcore import getPymcaConfig, getPymcaConfigFile

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


#                self._S = XrfSpecVar("S", self._specHost+":"+self._specPort)
#                self._Detector = XrfSpecVar("MCA_NAME",
#                                            self._specHost+":"+self._specPort)
#                self.mca_data = XrfSpecVar("MCA_DATA", 
#                                           self._specHost+":"+self._specPort,
#                                           500)
#
#    def get_values(self):
#        values = []
#        prev = self._last_index
#        curr = self._index.getValue()
#        if curr != prev:
#            if curr > prev+1:
#                print "missed point %s v %s"%(prev,curr)
#                self._last_index = curr
#                return ([''],curr,'')
#            else:
#                if self._Detector.getValue() == "vortex":
#                    a = self.compensate()
#                    print 'dead time correction: %.3f'% a
#                else:
#                    a = 1.0
##                time.sleep(TIMEOUT)
#                counts = self.mca_data.getValue()
#                values.append(a*counts)
#                self._last_index = curr
##                    print "*****************Got Point***************"
#                if 1 <= a:
#                    return (values, curr, True)
#                else:
#                    return (values, curr, False)
#        else:
#            return ([''], curr, '')
#
#    def compensate(self):
#        S = self._S.getValue()
#        icr = float(S["5"])
#        ocr = float(S["7"])
#        real = float(S["8"])
#        live = float(S["9"])
#        return icr/ocr*real/live

#        # TODO: break this into a new method
#        self.pymcaConfigFile = getPymcaConfigFile()
#        reader = getPymcaConfig()
#        self.__peaks = []
#        try:
#            elements = reader["peaks"]
#            for key in elements.keys():
#                self.__peaks.append("%s %s"%(key,elements[key]))
#        except KeyError:
#            pass

(TIMESCAN) = (16)

class QtSpecScanA(SpecScan.SpecScanA):
    def __init__(self, specVersion = None):
        self.scanParams = {}
        self.scanCounterMne = None
        self.__scanning = False

        if specVersion is not None:
            self.connectToSpec(specVersion)
        else:
            self.connection = None
        

    def connectToSpec(self, specVersion):
        self.connection = SpecConnectionsManager.SpecConnectionsManager().getConnection(specVersion)
        SpecEventsDispatcher.connect(self.connection, 'connected', self.connected)
        SpecEventsDispatcher.connect(self.connection, 'disconnected', self.__disconnected)

        self.connection.registerChannel('var/_SC_NEWSCAN', self.__newScan)
        self.connection.registerChannel('var/_SC_SCANDATALINE', self.__newScanPoint, dispatchMode=SpecEventsDispatcher.FIREEVENT)
                    
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
                

    def getScanType(self):
        try:
            return self.scanParams['scantype']
        except:
            return -1
        
                       
    def newScan(self, scanParameters):
        print scanParameters


    def __newScanPoint(self, scanDataString):
        if self.__scanning:
            print scanDataString
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
            self.connection.send_msg_cmd("ascan %s %f %f %d %f" % (motorMne, startPos, endPos, nbPoints, countTime))
            return True
        else:
            return False
