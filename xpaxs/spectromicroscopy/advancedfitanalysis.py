"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import Queue
import tempfile
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import pp
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

def flat_to_nd(index, shape):
    res = []
    for i in xrange(1, len(shape)):
        p = numpy.product(shape[i:])
        res.append(index//p)
        index = index % p
    res.append(index)
    return tuple(res)


def analyzeSpectrum(index, spectrum, tconf, advancedFit, mfTool):
    DEBUG = 0
    if DEBUG:
        t0 = time.time()

    advancedFit.config['fit']['use_limit'] = 1
    # TODO: get the channels from the controller
    advancedFit.setdata(y=spectrum)
    advancedFit.estimate()
    if ('concentrations' in advancedFit.config) and \
            (advancedFit._fluoRates is None):
        fitresult, result = advancedFit.startfit(digest=1)
    else:
        fitresult = advancedFit.startfit(digest=0)
        result = advancedFit.imagingDigestResult()
    result['index'] = index

    if DEBUG:
        t1 = time.time()
        print "fit: %s"%(t1-t0)

    if mfTool:
        temp = {}
        temp['fitresult'] = fitresult
        temp['result'] = result
        temp['result']['config'] = advancedFit.config
        tconf.update(advancedFit.configure()['concentrations'])
        conc = mfTool.processFitResult(config=tconf, fitresult=temp,
                                       elementsfrommatrix=False,
                                       fluorates=advancedFit._fluoRates)
        result['concentrations'] = conc

        if DEBUG:
            t2 = time.time()
            print "conc.: %s"%(t2-t1)

    return {'index': index, 'result': result, 'advancedFit': advancedFit}


class AdvancedFitThread(QtCore.QThread):

    def __init__(self, lock, parent):
        super(AdvancedFitThread, self).__init__(parent)
#        self.lock = lock
        self.lock = None
        self.stopped = False
        self.mutex = lock

        self.lastUpdate = time.time()

        self.completed = False

        self.jobServer = pp.Server()
#        self.jobServer.set_ncpus(1)

        self.connect(self,
                     QtCore.SIGNAL("processed"),
                     self.updateRecords)

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
        index = self.queue.get()
        try:
            self.mutex.lock()
#            self.lock.lockForRead()
            spectrum = self.scan.data[index]['MCA']
        finally:
            self.mutex.unlock()
#            self.lock.unlock()
        return index, spectrum

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

            d0 = time.time()
            for i in xrange(100):
                try: self.queueNext()
                except Queue.Empty: break

            d1 = time.time()
            print 'initialization:', d1-d0

            self.jobServer.wait()

            print 'completion:', time.time()-d1

    def queueNext(self):
        index, spectrum = self.findNextPoint()
        args = (index, spectrum, self.tconf, self.advancedFit,
                self.concentrationsTool)
        self.jobServer.submit(analyzeSpectrum, args,
                              callback=self.updateRecords)
#        self.jobServer.submit(analyzeSpectrum, args,
#                              callback=self.emit,
#                              callbackargs=(QtCore.SIGNAL("processed"), ))

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

    def updateRecords(self, data):
        result = data['result']
        try:
            self.mutex.lock()
#            self.lock.lockForWrite()
            self.advancedFit = data['advancedFit']
        finally:
            self.mutex.unlock()
#            self.lock.unlock()

        try:
            self.mutex.lock()
#            self.lock.lockForRead()
            shape = self.scan.attrs.scanShape
        finally:
            self.mutex.unlock()
#            self.lock.unlock()

        index = flat_to_nd(data['index'], shape)

        for group in result['groups']:
            g = group.replace(' ', '')

            fitArea = result[group]['fitarea']
            if fitArea: sigmaArea = result[group]['sigmaarea']/fitArea
            else: sigmaArea = numpy.nan

            try:
                self.mutex.lock()
#                self.lock.lockForWrite()
                try:
                    getattr(self.scan.elementMaps.PeakArea, g)[index] = fitArea
                    getattr(self.scan.elementMaps.SigmaArea, g)[index] = sigmaArea
                except ValueError:
                    print index, g
            finally:
                self.mutex.unlock()
#                self.lock.unlock()

        if 'concentrations' in result:
            massFractions = result['concentrations']['mass fraction']
            for key, val in massFractions.iteritems():
                k = key.replace(' ', '')
                try:
                    self.mutex.lock()
#                    self.lock.lockForWrite()
                    try:
                        getattr(self.scan.elementMaps.MassFraction, k)[index] = val
                    except ValueError:
                        print index, k
                finally:
                    self.mutex.unlock()
#                    self.lock.unlock()

        # TODO: wire this to a QTimer?
        now = time.time()
        elapsed = now-self.lastUpdate
#        print elapsed
        if elapsed > 1:
            self.emit(QtCore.SIGNAL("dataProcessed"))
            self.lastUpdate = time.time()

        try: self.queueNext()
        except Queue.Empty: pass
