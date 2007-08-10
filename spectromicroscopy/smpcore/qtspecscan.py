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
from spectromicroscopy.smpcore import configutils

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
#
#    def set_element(self):
#        self.Image_Element = "%s"%self.ElementSelect.currentText()
#        self.change_limits()
#
#    def auto_set(self):
#        self.MinValSpin.setValue(0)
#        self.MaxValSpin.setValue(0)
#        self.change_limits()
#
#    def change_limits(self):
#        if self.setup != 0:
#            parent = self.ImageFrame.widget(0)
#            self.Range_Max = self.MaxValSpin.value()
#            self.Range_Min = self.MinValSpin.value()
#            scale = "%s"%self.ScaleBox.currentText()
#            self.image = MyCanvas(self.ScanBox.currentText(),
#                                  self.__images[self.Image_Element],
#                                  self.x_index,
#                                  self.y_index,
#                                  self.Range_Min,
#                                  self.Range_Max,
#                                  parent,
#                                  self.energy,
#                                  self.__totaled,
#                                  scale)
#            self.image.setGeometry( QtCore.QRect(169, -1, 771, 900) )
#            self.image.setMinimumSize(100, 100)
#            self.image.setObjectName("Graph")
#            self.image.show()
#
#    def run_scan(self):
#        """
#        sets up scans
#        Pauses scan if running
#        resumes scan if paused
#        
#        Inorder to run a scan it:
#       1) establishes required values
#       2)connects MCA_DATAas spec variable
#       3)begins a timmer to gather data
#        """
#        if "%s"%self.Run.text() == "Scan":
#            self.setup = 0
#            self.processed = []
#            indexs=[[1,1,1],[1,1,1],[1,1,1]]
#            for i in range(len(self.Spin_Slide_Motor)):
#                for j in range(3):
#                    indexs[i][j] = self.Spin_Slide_Motor[i].get_settings()[j]
#            count_time = self.Counter.value()
#            self.Range_Max = self.MaxValSpin.value()
#            self.Range_Min = self.MinValSpin.value()
#            if "%s"%self.ScanBox.currentText() == "tseries":
#                self.max = indexs[0][2]*indexs[1][2]
#                self.xprun.set_cmd("tseries %s %s"%(self.max,count_time))
#                self.x_index = indexs[0][2]
#                self.y_index = 1
#            else:
#                self.x_index = indexs[0][2]+1
#                self.y_index = indexs[1][2]+1
#                self.max = self.x_index*self.y_index
#                x = self.X.get_motor_name()
#                y = self.Y.get_motor_name()
#                (xmin, xmax, xstep) = indexs[0]
#                (ymin, ymax, ystep) = indexs[1]
#                part_one = " %s %s %s %s"%(x,xmin,xmax,xstep)
#                part_two = " %s %s %s %s"%(y,ymin, ymax, ystep)
#                self.xprun.set_cmd("mesh"+part_one+part_two+" %s"%(count_time))
#            self.xprun.exc("NPTS=0")
#            self.processed = []
#            self.theory = ClassMcaTheory.McaTheory(self.pymcaConfigFile)
#            self.theory.enableOptimizedLinearFit()
#            self.data = numpy.memmap(self.buffer.name,
#                                     dtype=float,
#                                     mode='w+',
#                                     shape=(self.max,2048))
##            self.xprun.exc("MCA_DATA=0")
##            self.xprun.set_var('MCA_DATA',"Sync")
#            self.__images = {}
#            self.__sigmas = {}
#            config = getPymcaConfig()
#            gain = float(config["detector"]["gain"])
#            offset = float(config["detector"]["zero"])
#            self.__totaled = numpy.zeros(2048, numpy.float_)
#            converstion = 0.01##TODO: read this value from config files
#            self.energy = gain*numpy.arange(2048, dtype=numpy.float_)+offset
#            self.timer = QtCore.QTimer(self)
#            QtCore.QObject.connect(self.timer,
#                                   QtCore.SIGNAL("timeout()"),
#                                   self.data_collect)
#            self.timer.start(20)
#            self.xprun.run_cmd()
#            self.Run.setText("Pause")
#        elif "%s"%self.Run.text() == "Pause":
#            print "Pause command"
#            self.xprun.exc("")
#            self.Run.setText("Resume")
#        elif "%s"%self.Run.text() == "Resume":
#            self.xprun.exc("scan_on")
#            self.Run.setText("Pause")
#    
#    def data_collect(self):
#        """gathers data from spec and processes it """
#        max_index = self.max
#        self.xprun.update()
#        (value,index,actual) = self.xprun.get_values()
#        if actual:
#            typed = type(value[0])
##            print "<<%s>> %s"%(index,typed)
#            if len(value[0])>1:
#                self.data[index-1] = value[0][:,1]
#            else:
#                self.data[index-1] = value[0]
#            self.theory.setdata(range(2048),self.data[index-1],None)
#            self.theory.estimate()
#            fitresult, result = self.theory.startfit(digest=1)
#            self.processed.append((fitresult,result))
#            self.__peaks = []
#            self.__nrows = len(range(0,max_index))
#            for group in result['groups']:
#                self.__peaks.append(group)
#                if not self.setup:
#                    self.__images[group] = numpy.zeros((self.__nrows,1),
#                                                       dtype=numpy.float_)
#                    self.__sigmas[group] = numpy.zeros((self.__nrows,1),
#                                                       dtype=numpy.float_)
#            self.__images['chisq'] = numpy.zeros((self.__nrows,1),
#                                                 dtype=numpy.float_) - 1.
#            self.__images['chisq'][index-1, 0] = result['chisq']
#            for peak in self.__peaks:
#                if not self.setup:
#                    self.__images[peak][index-1, 0] = result[peak]['fitarea']
#                    self.__sigmas[peak][index-1,0] = result[peak]['sigmaarea']
#                else:
#                    self.__images[peak][index-1, 0] += result[peak]['fitarea']
#                    self.__sigmas[peak][index-1,0] += result[peak]['sigmaarea']
#            if self.Image_Element not in self.__peaks:
#                self.Image_Element=self.__peaks[0]
##            print self.__images[self.Image_Element]
#            scale = "%s"%self.ScaleBox.currentText()
#            self.__totaled += self.data[index-1]
#            parent = self.ImageFrame.widget(0)
#            self.image = MyCanvas(self.ScanBox.currentText(),
#                                  self.__images[self.Image_Element],
#                                  self.x_index,
#                                  self.y_index,
#                                  self.Range_Min,
#                                  self.Range_Max,
#                                  parent,
#                                  self.energy,
#                                  self.__totaled,
#                                  scale)
#            self.image.setGeometry( QtCore.QRect(169, -1, 771, 800) )
#            self.image.setMinimumSize(100,100)
#            self.image.setObjectName("Graph")
#            self.image.show()
#            self.ToolBar = NavigationToolbar2QTAgg(self.image, parent)
#            self.ToolBar.setGeometry( QtCore.QRect(169, 800, 771, 50) )
#            self.ToolBar.show()
#            self.ToolBar.draw()
#            self.ToolBar.update()
#            self.setup = 1
##            print self.Image_Element
#        if index == self.max:
#            self.timer.stop()
#            self.setup = 2
##            self.xprun.exc("MCA_DATA=0")
#            self.Run.setText("Scan")

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
