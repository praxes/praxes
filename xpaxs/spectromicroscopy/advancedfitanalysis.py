"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import Queue
import tempfile

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyMca import ClassMcaTheory, EdfFile
from PyMca.ConcentrationsTool import ConcentrationsTool
from PyQt4 import QtCore
import numpy
numpy.seterr(all='ignore')
#import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import configutils

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


DEBUG = False

if DEBUG:
    import time

def flat_to_nd(index, shape):
    res = []
    for i in xrange(1, len(shape)):
        p = numpy.product(shape[i:])
        res.append(index//p)
        index = index % p
    res.append(index)
    return tuple(res)


class AdvancedFitRunner(QtCore.QObject):

    def __init__(self, config, parent):
        super(AdvancedFitRunner, self).__init__(parent)

        self.config = config

        self.advancedFit = ClassMcaTheory.McaTheory(config=config)
        self.advancedFit.enableOptimizedLinearFit()

        self.concentrationsTool = None
        if 'concentrations' in config:
            self.concentrationsTool = ConcentrationsTool(config)
            self.tconf = self.concentrationsTool.configure()

    def processData(self, index, scanData):
        if DEBUG: t0 = time.time()
        self.advancedFit.config['fit']['use_limit'] = 1
        # TODO: get the channels from the controller
        self.advancedFit.setdata(y=scanData['MCA'])
        self.advancedFit.estimate()
        if ('concentrations' in self.advancedFit.config) and \
            (self.advancedFit._fluoRates is None):
            fitresult, result = self.advancedFit.startfit(digest=1)
        else:
            fitresult = self.advancedFit.startfit(digest=0)
            result = self.advancedFit.imagingDigestResult()
        result['index'] = index



        fitData = {}
        fitData['index'] = index
        fitData['xdata'] = self.advancedFit.xdata
        zero, gain = self.advancedFit.fittedpar[:2]
        fitData['energy'] = zero + gain*self.advancedFit.xdata
        fitData['ydata'] = self.advancedFit.ydata
        fitData['yfit'] = \
                self.advancedFit.mcatheory(self.advancedFit.fittedpar,
                                           self.advancedFit.xdata)
#        fitData['yfit'] += self.advancedFit.continuum(self.advancedFit.fittedpar, self.advancedFit.xdata)
        fitData['yfit'] += self.advancedFit.zz
        fitData['residuals'] = fitData['ydata']-fitData['yfit']
        logres = numpy.log10(fitData['ydata'])-\
                 numpy.log10(fitData['yfit'])
        logres[numpy.isinf(logres)]=numpy.nan
        fitData['logresiduals'] = logres

        result['mcaFit'] = fitData

        if DEBUG:
            t1 = time.time()
            print "fit: %s"%(t1-t0)

        # prepare for concentrations:
        # is this step always necessary?
        config = self.advancedFit.configure()

        if self.concentrationsTool:
            temp = {}
            temp['fitresult'] = fitresult
            temp['result'] = result
            temp['result']['config'] = self.advancedFit.config
            self.tconf.update(config['concentrations'])
            conc = self.concentrationsTool.processFitResult(config=self.tconf,
                                fitresult=temp,
                                elementsfrommatrix=False,
                                fluorates=self.advancedFit._fluoRates)
            result['concentrations'] = conc

            if DEBUG:
                t2 = time.time()
                print "conc.: %s"%(t2-t1)

        self.emit(QtCore.SIGNAL("dataProcessed"),
                  result)


class AdvancedFitThread(QtCore.QThread):

    def __init__(self, lock, parent):
        super(AdvancedFitThread, self).__init__(parent)
        self.lock = lock
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.completed = False

    def estimateMassFractions(self):
        # prepare for concentrations:
        # is this step always necessary?
        config = self.advancedFit.configure()

        if self.concentrationsTool:
            temp = {}
            temp['fitresult'] = self._fitresult
            temp['result'] = self._result
            temp['result']['config'] = self.advancedFit.config
            self.tconf.update(config['concentrations'])
            conc = self.concentrationsTool.processFitResult(config=self.tconf,
                                fitresult=temp,
                                elementsfrommatrix=False,
                                fluorates=self.advancedFit._fluoRates)
            self._result['concentrations'] = conc

    def fitSpectrum(self):
        self.advancedFit.config['fit']['use_limit'] = 1
        # TODO: get the channels from the controller
        self.advancedFit.setdata(y=self._spectrum)
        self.advancedFit.estimate()
        if ('concentrations' in self.advancedFit.config) and \
            (self.advancedFit._fluoRates is None):
            fitresult, result = self.advancedFit.startfit(digest=1)
        else:
            fitresult = self.advancedFit.startfit(digest=0)
            result = self.advancedFit.imagingDigestResult()
        result['index'] = self._index
        self._result = result
        self._fitresult = fitresult

    def findNextPoint(self):
        self._index = self.queue.get()
        try:
            self.lock.lockForRead()
            self._spectrum = self.scan.data[self._index]['MCA']
        finally:
            self.lock.unlock()

    def getSpectrumFit(self):
        fitData = {}
        fitData['index'] = self._index
        fitData['xdata'] = self.advancedFit.xdata
        zero, gain = self.advancedFit.fittedpar[:2]
        fitData['energy'] = zero + gain*self.advancedFit.xdata
        fitData['ydata'] = self.advancedFit.ydata
        fitData['yfit'] = \
                self.advancedFit.mcatheory(self.advancedFit.fittedpar,
                                           self.advancedFit.xdata)
        fitData['yfit'] += self.advancedFit.zz
        fitData['residuals'] = fitData['ydata']-fitData['yfit']
        logres = numpy.log10(fitData['ydata'])-\
                 numpy.log10(fitData['yfit'])
        logres[numpy.isinf(logres)]=numpy.nan
        fitData['logresiduals'] = logres

        return fitData

    def initialize(self, config, scan, queue):

        # TODO: enable skipmode, needs moved from analysisController

        self.config = config
        self.scan = scan
        self.queue = queue

        self.advancedFit = ClassMcaTheory.McaTheory(config=config)
        self.advancedFit.enableOptimizedLinearFit()

        self.concentrationsTool = None
        if 'concentrations' in config:
            self.concentrationsTool = ConcentrationsTool(config)
            self.tconf = self.concentrationsTool.configure()

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()

    def processData(self):
        while 1:
            if self.isStopped(): return

            try:
                self.findNextPoint()

                if DEBUG: t0 = time.time()
                self.fitSpectrum()
                if DEBUG:
                    t1 = time.time()
                    print "fit: %s"%(t1-t0)
                self.estimateMassFractions()
                if DEBUG:
                    t2 = time.time()
                    print "conc.: %s"%(t2-t1)
                self.updateRecords()
                self.queue.task_done()

                self.emit(QtCore.SIGNAL("dataProcessed"))
            except Queue.Empty:
                pass

    def run(self):
        self.processData()
        self.stop()
        self.emit(QtCore.SIGNAL('finished(bool)'), self.completed)

    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def updateRecords(self):
        try:
            self.lock.lockForRead()
            shape = self.scan.attrs.scanShape
        finally:
            self.lock.unlock()

        index = flat_to_nd(self._index, shape)

        for group in self._result['groups']:
            g = group.replace(' ', '')

            fitArea = self._result[group]['fitarea']
            if fitArea: sigmaArea = self._result[group]['sigmaarea']/fitArea
            else: sigmaArea = numpy.nan

            try:
                self.lock.lockForWrite()
                getattr(self.scan.elementMaps.PeakArea, g)[index] = fitArea
                getattr(self.scan.elementMaps.SigmaArea, g)[index] = sigmaArea
            finally:
                self.lock.unlock()

        if 'concentrations' in self._result:
            massFractions = self._result['concentrations']['mass fraction']
            for key, val in massFractions.iteritems():
                k = key.replace(' ', '')
                try:
                    self.lock.lockForWrite()
                    mf = getattr(self.scan.elementMaps.MassFraction, k)
                    mf[index] = val
                finally:
                    self.lock.unlock()


# TODO: this module should be eliminated
class AdvancedFitAnalysis(QtCore.QObject):

    def __init__(self, *args):
        """Processes the Information from Spec

        """
        QtCore.QObject.__init__(self)

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
        self.elementMaps = {"Peak Area": {},
                            "Mass Fraction": {},
                            "Sigma Area": {}}

        self._currentElement = None
        self._currentDataType = "Peak Area"

        self.concentrationTool = None

        self._specFilename = 'smp.dat'
        self.settings=QtCore.QSettings()
        # TODO: this should be configurable
        self.monitor="%s"%self.settings.value('Monitor').toString()#        self.monitor = 'Icol'
    def setMonitor(self):
        pass
        self.settings.setValue( )
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

    def loadPymcaConfig(self, config=None):
        if not config:
            config = configutils.getPymcaConfig()
        self.pymcaConfig = config
        self.peaks = []
        for el, edges in self.pymcaConfig['peaks'].iteritems():
            for edge in edges:
                self.peaks.append(' '.join([el, edge]))
        self.peaks.sort()
        if self._currentElement is None:
            self._currentElement = self.peaks[0]
        for datatype in self.elementMaps:
            for peak in self.peaks:
                if not peak in self.elementMaps[datatype]:
                    self.elementMaps[datatype][peak] = \
                        numpy.zeros(self.imageSize, dtype=numpy.float_)
        self.emit(QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                  self.peaks)
        self.advancedFit = ClassMcaTheory.McaTheory(config=config)
        self.advancedFit.enableOptimizedLinearFit()

        if 'concentrations' in config:
            self.concentrationTool = ConcentrationsTool.ConcentrationsTool(config)
            self.emit(QtCore.SIGNAL('viewConcentrations(PyQt_PyObject)'),
                      'concentrations' in config)

    def setCurrentElement(self, element):
        if not self._currentElement == str(element):
            self._currentElement = str(element)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.elementMaps[self._currentDataType][self._currentElement])

    def setCurrentDataType(self, datatype):
        if not self._currentDataType == str(datatype):
            self._currentDataType = str(datatype)
            self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                      self.elementMaps[self._currentDataType][self._currentElement])

    def newDataPoint(self, scanData):
        self.index = scanData['i']
        if self.index == 0: self.previousIndex = -1
        if self.index != self.previousIndex+1:
            if DEBUG: print 'index problem: ', self.previousIndex, self.index, len(self.dataQue)

        skipmodeStatus=self.settings.value('skipmode/enabled').toBool()
        counter="%s"%self.settings.value('skipmode/counter').toString()
        threshold=self.settings.value('skipmode/threshold').toFloat()
        scanData['pointSkipped'] = skipmodeStatus and \
                (scanData[counter ] <= threshold)

        deadtimeCorrection=self.settings.value('DeadTimeCorrection').toBool()
        if deadtimeCorrection:
            try:
                scanData['mcaCounts'][1] *= 100./(100-float(scanData['dead']))
            except KeyError:
                if DEBUG: print 'deadtime not corrected. A counter reporting '\
                    'the percent dead time, called "Dead", must be created in '\
                    'Spec for this feature to work.'
        self.dataQue.append(scanData)
        #TODO: probably needs a separate thread at some point
        self.processNextPoint()

    def processNextPoint(self):
        try:
            scanData = self.dataQue.pop(0)
#            self.archiveSpecData(scanData)
            index = scanData['i']
            if scanData['pointSkipped']:
                for datatype in self.elementMaps:
                    for peak in self.peaks:
                        self.elementMaps[datatype][peak].flat[index] = 0
            else:
                if DEBUG: t0 = time.time()
                self.advancedFit.config['fit']['use_limit'] = 1
                self.advancedFit.setdata(scanData['mcaChannels'],
                                         scanData['mcaCounts'])
                self.advancedFit.estimate()
                if ('concentrations' in self.advancedFit.config) and \
                    (self.advancedFit._fluoRates is None):
                    fitresult, result = self.advancedFit.startfit(digest=1)
                else:
                    fitresult = self.advancedFit.startfit(digest=0)
                    result = self.advancedFit.imagingDigestResult()

                fitData = {}
                fitData['xdata'] = self.advancedFit.xdata
                zero, gain = self.advancedFit.fittedpar[:2]
                fitData['energy'] = zero + gain*self.advancedFit.xdata
                fitData['ydata'] = self.advancedFit.ydata
                fitData['yfit'] = self.advancedFit.\
                        mcatheory(self.advancedFit.fittedpar,
                                  self.advancedFit.xdata)
                fitData['residuals'] = fitData['ydata']-fitData['yfit']
                logres = numpy.log10(fitData['ydata'])-\
                         numpy.log10(fitData['yfit'])
                logres[numpy.isinf(logres)]=numpy.nan
                fitData['logresiduals'] = logres
                self.emit(QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"), fitData)

                for group in result['groups']:
                    self.elementMaps["Peak Area"][group].flat[index] = \
                        result[group]['fitarea']
                    area = numpy.where(result[group]['fitarea']==0,
                                       numpy.nan,
                                       result[group]['fitarea'])
                    self.elementMaps["Sigma Area"][group].flat[index] = \
                        result[group]['sigmaarea']/area

                if DEBUG:
                    t1 = time.time()
                    print "fit: %s"%(t1-t0)

                # prepare for concentrations:
                conf = self.advancedFit.configure()
                if conf.has_key('concentrations'):
                    temp = {}
                    temp['fitresult'] = fitresult
                    temp['result'] = result
                    temp['result']['config'] = self.advancedFit.config
                    tconf = self.concentrationTool.configure()
                    tconf.update(conf['concentrations'])
                    concentrations = self.concentrationTool.\
                       processFitResult(config=tconf,
                                        fitresult=temp,
                                        elementsfrommatrix=False,
                                        fluorates=self.advancedFit._fluoRates)
                    for group in concentrations['mass fraction'].keys():
                        self.elementMaps["Mass Fraction"][group].flat[index] = \
                            concentrations['mass fraction'][group]

                    if DEBUG:
                        t2 = time.time()
                        print "conc.: %s"%(t2-t1)

                self.emit(QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                          self.elementMaps[self._currentDataType][self._currentElement])

            if index <= 1:
                self.emit(QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                          True)
            self.previousIndex = index
        except IndexError:
            pass # no data to process

    def getMcaSpectrum(self, index=None):
        if index is None:
            return self.mcaDataFit[-1]

    def getSpecFilename(self):
        return self._specFilename

    def setSpecFilename(self, scanParams):
        temp = scanParams['datafile'].rstrip('.dat').rstrip('.txt').rstrip('.mca')
        filename = '_'.join([temp,
                             scanParams['title'].replace(' ', '')])
        self._specFilename = filename

    def getSuggestedFilename(self):
        return '%s_%s_%s.edf'%(self._specFilename,
                               self._currentElement.replace(' ', '-'),
                               self._currentDataType.replace(' ', ''))

    def _saveData(self, filename, el, datatype):
        data = self.elementMaps[datatype][el]
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

    def saveData(self, filename=None, filetype='edf'):
        if not filename: filename = self._specFilename
        for dtype, val in self.elementMaps.iteritems():
            for el, data in val.iteritems():
                self._saveData("%s_%s_%s.%s"%(filename,
                                              el.replace(' ', '-'),
                                              dtype.replace(' ', ''),
                                              filetype),
                               el, dtype)


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
