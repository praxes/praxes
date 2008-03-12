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

def analyzeSpectrum(index, spectrum, tconf, advancedFit, mfTool):
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

    return {'index': index, 'result': result, 'advancedFit': advancedFit}


class AdvancedFitThread(QtCore.QThread):

    def __init__(self, scan, config, parent):
        super(AdvancedFitThread, self).__init__(parent)

        self.mutex = QtCore.QMutex()

        self.scan = scan

        self.config = config
        self.advancedFit = ClassMcaTheory.McaTheory(config=config)
        self.advancedFit.enableOptimizedLinearFit()
        self.concentrationsTool = None
        if 'concentrations' in config:
            self.concentrationsTool = ConcentrationsTool(config)
            self.tconf = self.concentrationsTool.configure()

        self.jobServer = pp.Server()
#        self.jobServer.set_ncpus(1)

        self.queue = Queue.Queue()
        for i in xrange(self.scan.getNumScanLines()):
            self.queue.put(i)
        self.previousIndex = None

        self.dirty = False
        self.stopped = False
        self.completed = False

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.report)
        self.timer.start(1000)

        self.connect(self,
                     QtCore.SIGNAL("processed"),
                     self.updateRecords)

    def findNextPoint(self):
        index = self.queue.get(False)
        # TODO: need to be able to select which mca
        spectrum = self.scan.getMcaSpectrum(index)
        try:
            self.mutex.lock()
            self.previousIndex = index
        finally:
            self.mutex.unlock()
        return index, spectrum

    def getQueue(self):
        return self.queue

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

            # TODO: report this progress in a progressBar
            for i in xrange(100):
                try: self.queueNext()
                except Queue.Empty: break

            self.jobServer.wait()

            expectedLines = self.scan.getNumExpectedScanLines()
            if expectedLines <= (self.previousIndex+1): return

    def queueNext(self):
        index, spectrum = self.findNextPoint()
        args = (index, spectrum, self.tconf, self.advancedFit,
                self.concentrationsTool)
        self.jobServer.submit(analyzeSpectrum, args,
                              callback=self.updateRecords)

    def run(self):
        self.processData()
        self.stop()
        self.emit(QtCore.SIGNAL('finished()'))

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
            self.advancedFit = data['advancedFit']
        finally:
            self.mutex.unlock()

        shape = self.scan.getScanShape()

        index = flat_to_nd(data['index'], shape)

        for group in result['groups']:
            g = group.replace(' ', '')

            fitArea = result[group]['fitarea']
            if fitArea: sigmaArea = result[group]['sigmaarea']/fitArea
            else: sigmaArea = numpy.nan

            self.scan.updateElementMap('fitArea', g, index, fitArea)
            self.scan.updateElementMap('sigmaArea', g, index, sigmaArea)

        if 'concentrations' in result:
            massFractions = result['concentrations']['mass fraction']
            for key, val in massFractions.iteritems():
                k = key.replace(' ', '')
                self.scan.updateElementMap('massFraction', k, index, val)
        self.dirty = True

        try: self.queueNext()
        except Queue.Empty: pass

    def report(self):
        if self.dirty:
            self.emit(QtCore.SIGNAL("dataProcessed"))
            self.dirty = False
