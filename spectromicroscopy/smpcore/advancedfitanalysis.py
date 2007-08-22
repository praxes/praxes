"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyMca import ClassMcaTheory, EdfFile
from PyQt4 import QtCore
import numpy
numpy.seterr(all='ignore')

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpcore import configutils

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class AdvancedFitAnalysis(QtCore.QObject):

    def __init__(self, *args):
        """Processes the Information from Spec
        
        """
        QtCore.QObject.__init__(self)

        self.dataQue = []
        self.previousIndex = -1
        self.index = 0
        
        self.mcaDataFit = []
        self.elements = {}
        self._currentElement = None
        
        self._suggested_filename = 'smp.dat'
        
        # TODO: this should be configurable
        self.monitor = 'Icol'
    
    def loadPymcaConfig(self, configFile=None):
        if not configFile:
            configFile = configutils.getDefaultPymcaConfigFile()
        self.pymcaConfig = configutils.getPymcaConfig(configFile)
        self.peaks = [' '.join([key, val]) 
                      for key, val in self.pymcaConfig['peaks'].iteritems()]
        self.peaks.sort()
        if self._currentElement is None:
            self._currentElement = self.peaks[0]
        for peak in self.peaks:
            if not peak in self.elements:
                    self.elements[peak] = numpy.zeros(self.imageSize,
                                                      dtype=numpy.float_)
        self.emit(QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                  self.peaks)
        self.advancedFit = ClassMcaTheory.McaTheory(configFile)
        self.advancedFit.enableOptimizedLinearFit()
    
    def setCurrentElement(self, element):
        if not self._currentElement == str(element):
            self._currentElement = str(element)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"), 
                      self.elements[self._currentElement])
    
    def newDataPoint(self, scanData):
        self.previousIndex = self.index
        self.index = scanData['i']
        if self.index != self.previousIndex+1 and self.index != 0:
            print 'index problem: ', self.previousIndex, self.index
        
        #TODO: preprocess data here: deadtime correction, etc.
        self.dataQue.append(scanData)
        
        #TODO: probably needs a separate thread at some point
        self.processNextPoint()
    
    def processNextPoint(self):
        try:
            scanData = self.dataQue.pop(0)
            index = scanData['i']
            mcaData = scanData['mcaData']
            self.advancedFit.setdata(mcaData[0], mcaData[1], None)
            self.advancedFit.estimate()
            fitresult, result = self.advancedFit.startfit(digest=1)
            
            fitData = {}
            fitData['xdata'] = result['xdata']
            fitData['energy'] = result['energy']
            fitData['ydata'] = result['ydata']
            fitData['yfit'] = result['yfit']
            fitData['residuals'] = result['ydata']-result['yfit']
            logres = numpy.log10(result['ydata'])-\
                            numpy.log10(result['yfit'])
            logres[numpy.isinf(logres)]=numpy.nan
            fitData['logresiduals'] = logres
            
            for group in result['groups']:
                self.elements[group].flat[index] = result[group]['fitarea']
            
            self.mcaDataFit.append(fitData)
            self.emit(QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"), fitData)
            
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"), 
                      self.elements[self._currentElement])
            if index <= 1:
                self.emit(QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                          True)
        except IndexError:
            pass # no data to process
    
    def getMcaSpectrum(self, index=None):
        if index is None:
            return self.mcaDataFit[-1]

    def setSuggestedFilename(self, scanParams):
        filename = '_'.join([scanParams['datafile'],
                             scanParams['title'].replace(' ', '')])
        self._suggested_filename = filename+'.edf'
    
    def getSuggestedFilename(self):
        return self._suggested_filename

    def saveData(self, filename):
        data = self.elements[self._currentElement]
        header = self.getFileHeader()
        
        format = os.path.splitext(filename)[-1]
        if format.lower() == '.edf':
            edf = EdfFile.EdfFile(filename)
            edf.WriteImage(header, data, Append=0)
        else:
            fd = open(filename, 'w')
            header = ['#%s : %s\n'% (i, v) for (i, v) in header.itervalues()]
            fd.writelines(header)
            s = data.shape
            if len(s) == 1:
                cols = s[0]
                fd.write('%s '*cols%tuple(data))
            else:
                cols = s[1]
                formatStr = '%f '*cols+'\n'
                strRep = [formatStr%tuple(line) for line in data]
                fd.writelines(strRep)
            fd.close()
    
    def getFileHeader(self):
        return {}


class AdvancedFitAnalysis1D(AdvancedFitAnalysis):
    
    def __init__(self, *args):
        AdvancedFitAnalysis.__init__(self)
        
        


class AdvancedFitAnalysis2D(AdvancedFitAnalysis):
    
    def __init__(self, scanArgs):
        AdvancedFitAnalysis.__init__(self)
        
        x, xmin, xmax, xsteps, y, ymin, ymax, ysteps = scanArgs
        
        self.x = x
        self.xRange = (xmin, xmax)
        self.xPoints = xsteps+1
        self.y = y
        self.yRange = (ymin, ymax)
        self.yPoints = ysteps+1
        self.imageSize = (self.yPoints, self.xPoints)


#        scanData['MCA_DATA'] = self.mcaData.getValue


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
#            self.connect(self.timer,
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
