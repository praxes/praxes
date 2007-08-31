"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import tempfile

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyMca import ClassMcaTheory, EdfFile,ConcentrationsTool
from PyQt4 import QtCore
import numpy
numpy.seterr(all='ignore')
#import tables

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
        
        self.threshold=0
        self.detector="Icol"
        self.skipmode=0
        
        self.dataQue = []
        self.previousIndex = -1
        self.index = 0
        
#        self.hdf5file = tempfile.NamedTemporaryFile()
#        self.hdf5 = tables.openFile(self.hdf5file.name, mode='w')
#        self.hdf5.createGroup('/', 'spec', 'spec raw data')
#        self.hdf5.createGroup('/', 'pymca', 'pymca processed data')
#        self.hdf5.createGroup('/pymca', 'elements', 'pymca elements data')
#        self.hdf5.createGroup('/pymca/elements', 'fitarea', 'peak areas')
#        self.hdf5.createGroup('/pymca/elements', 'concentrations', 'concentrations')
#        self.hdf5.createGroup('/pymca/elements', 'sigmaarea', 'error')
        
        self.mcaDataFit = []
        self.mcaConData=[]
        self.elements = {}
        self.sigma={}
        self.concentrates={}
        self.alldata={}
        self._currentElement = None
        self._currentDataType = "Peak Areas"
        
        self._suggested_filename = 'smp.dat'
        
        # TODO: this should be configurable
        self.monitor = 'Icol'
    
#    def configureSpecTable(self, scanData):
#        desc = dict([(key, tables.Float32Col()) for key in scanData])
#        if 'mcaData' in desc:
#            s = scanData['mcaData'].shape
#            desc['mcaData'] = tables.Float32Col(shape=s)
#        self.hdf5.createTable('/spec', 'rawData', desc, 'raw data')
#    
#    def archiveSpecData(self, scanData):
#        try:
#            obs = self.hdf5.root.spec.rawData.row
#        except:
#            self.configureSpecTable(scanData)
#            obs = self.hdf5.root.spec.rawData.row
#        for key in scanData:
#            obs[key] = scanData[key]
#        obs.append()
#        self.hdf5.root.spec.rawData.flush()
#
#    def configurePymcaSpectraTable(self, fitData):
#        
#        desc = dict([(key, tables.Float32Col(shape=val.shape)) 
#                     for (key, val) in fitData.iteritems()])
#        
#        self.hdf5.createTable('/pymca', 'spectra', desc, 'pymca fits')
#    
#    def archivePymcaSpectra(self, fitData):
#        try:
#            row = self.hdf5.root.pymca.spectra.row
#        except:
#            self.configurePymcaSpectraTable(fitData)
#            row = self.hdf5.root.pymca.spectra.row
#        for key in fitData:
#            row[key] = fitData[key]
#        row.append()
#        self.hdf5.root.pymca.spectra.flush()
#    
#    def createElementArray(self, element, type):
#        self.hdf5.createArray('/pymca/elements/%s'%type, 
#                              element, 
#                              numpy.zeros(self.imageSize, dtype=numpy.float32), 
#                              ' '.join([element, type]) )
#    
#    def archiveElementData(self, element, type, index, val):
#        try:
#            group = getattr(self.hdf5.root.pymca.elements, type)
#            data = getattr(group, element)
#        except tables.exceptions.NoSuchNodeError:
#            self.createElementArray(element, type)
#            group = getattr(self.hdf5.root.pymca.elements, type)
#            data = getattr(group, element)
#        # This doesnt work, no flat attribute unless we read() the data
#        # Thats not good!
#        data.flat[index] = val

    def setThreshold(self,value):
        self.threshold=double(value)
    def setDetector(self,name):
        self.detector=str(name)
    def setSkipMode(self,bool):
        self.skipmode=bool

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
            if not peak in self.sigma:
                    self.sigma[peak] = numpy.zeros(self.imageSize,
                                                      dtype=numpy.float_)
            if not peak in self.concentrates:
                    self.concentrates[peak] = numpy.zeros(self.imageSize,
                                                      dtype=numpy.float_)
        self.emit(QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                  self.peaks)
        self.advancedFit = ClassMcaTheory.McaTheory(configFile)
        self.advancedFit.enableOptimizedLinearFit()
        self.concentrationTool=ConcentrationsTool.ConcentrationsTool(configFile)
    
    def setCurrentElement(self, element):
        if not self._currentElement == str(element):
            self._currentElement = str(element)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"), 
                      self.alldata[self._currentDataType][self._currentElement])
    def setCurrentDataType(self,datatype):
        if not self._currentDataType == str(datatype):
            self._currentDataType = str(datatype)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"), 
                      self.alldata[self._currentDataType][self._currentElement])
    
    def newDataPoint(self, scanData):
        self.previousIndex = self.index
        self.index = scanData['i']
        if self.index != self.previousIndex+1 and self.index != 0:
            print 'index problem: ', self.previousIndex, self.index
        
        
        
        if self.threshold>=scanData[self.detector] and self.skipmode:
            print "THRESHOLD TRIPED"
            scanData["mcaData"]=0
            self.dataQue.append(scanData)
        else:
            #TODO: preprocess data here: deadtime correction, etc.
            self.dataQue.append(scanData)
        #TODO: probably needs a separate thread at some point
        self.processNextPoint()
    
    def processNextPoint(self):
        try:
            scanData = self.dataQue.pop(0)
#            self.archiveSpecData(scanData)
            index = scanData['i']
            mcaData = scanData['mcaData']
            if type(mcaData)==type(0):
                print "SKIPPING"
                for key in self.elements.keys():
                    self.elements[key].flat[index] = 0
                    self.concentrates[key].flat[index] = 0
                    self.sigma[key].flat[index] = 0
                    self.emit(QtCore.SIGNAL("Skipped(PyQt_PyObject)"), index)
            else:
                self.advancedFit.setdata(mcaData[0], mcaData[1], None)
                self.advancedFit.estimate()
                fitresult, result = self.advancedFit.startfit(digest=1)
                
                dictresult={"result":result}
                concentrationresult=self.concentrationTool.processFitResult(fitresult=dictresult)
                self.mcaConData.append(concentrationresult)
                
                
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
                self.mcaDataFit.append(fitData)
    #            self.archivePymcaSpectra(fitData)
                
                for group in result['groups']:
    #                print result[group].keys()
                    self.elements[group].flat[index] = result[group]['fitarea']
    #                for t in ('fitarea', 'sigmaarea'):
    #                    self.archiveElementData(group, t, index, result[group][t])
                    self.sigma[group].flat[index]=concentrationresult['sigmaarea'][group]
                    self.concentrates[group].flat[index]=concentrationresult['mass fraction'][group]
                self.emit(QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"), fitData)
                
            self.alldata["Peak Areas"]=self.elements
            self.alldata["Concentrations"]=self.concentrates
            self.alldata["Error"]=self.sigma
            
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"), 
                      self.alldata[self._currentDataType][self._currentElement])
            
            
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
    
    def __init__(self, scanArgs):
        #TODO edit so that it can work with both Tseries and Ascans
        AdvancedFitAnalysis.__init__(self)
        
        xsteps = scanArgs[-1]
        if len(scanArgs) > 3:
            self.x = scanArgs[0]
            self.xRange = scanArgs[1:3]
        else:
            self.x = 'time'
            self.xRange = (0, xsteps+1)
        self.xPoints = xsteps + 1
        self.imageSize = (self.xPoints)


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
