"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
import Queue
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import pp
from PyMca import ClassMcaTheory
from PyMca.ConcentrationsTool import ConcentrationsTool
from PyQt4 import QtCore
import numpy
numpy.seterr(all='ignore')

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.dispatch.pptaskmanager import PPTaskManager

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


logger = logging.getLogger(__file__)
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


class XfsPPTaskManager(PPTaskManager):

    def findNextPoint(self):
        index = self.queue.get(False)
        # TODO: need to be able to select which mca
        spectrum = self.scan.getMcaSpectrum(index)
        return index, spectrum

    def queueNext(self):
        self.numExpected = self.scan.getNumExpectedScanLines()
        self.numSkipped = self.scan.getNumSkippedPoints()
        try:
            self.mutex.lock()
            while self.numQueued < self.numCpus*3:
                try:
                    index, spectrum = self.findNextPoint()
                    args = (index, spectrum, self.tconf, self.advancedFit,
                            self.concentrationsTool)
                    self.jobServer.submit(analyzeSpectrum, args,
                                          callback=self.updateRecords)
                    self.numQueued += 1
                except Queue.Empty:
                    break
        finally:
            self.mutex.unlock()

    def setData(self, scan, config):
        self.scan = scan
        self.scan.setQueue(self.queue)

        self.config = config

        self.advancedFit = ClassMcaTheory.McaTheory(config=config)
        self.advancedFit.enableOptimizedLinearFit()
        self.concentrationsTool = None
        if 'concentrations' in config:
            self.concentrationsTool = ConcentrationsTool(config)
            self.tconf = self.concentrationsTool.configure()

        self.numSkipped = self.scan.getNumSkippedPoints() # skipped by skipmode
        self.expectedLines = self.scan.getNumExpectedScanLines()

        for i in self.scan.getValidDataPoints():
            self.queue.put(i)

    def updateRecords(self, data):
        try:
            self.mutex.lock()
            self.numQueued -= 1
            self.numProcessed += 1
            self.emit(QtCore.SIGNAL('percentComplete'),
                      100*(self.numProcessed+self.numSkipped)/self.expectedLines)
            if data: self.advancedFit = data['advancedFit']
        finally:
            self.mutex.unlock()

        if data:
            shape = self.scan.getScanShape()
            index = flat_to_nd(data['index'], shape)

            result = data['result']
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

    def report(self):
        if DEBUG: print self
        if self.dirty:
            self.emit(QtCore.SIGNAL("dataProcessed"))
            self.emit(QtCore.SIGNAL("ppJobStats"), self.jobServer.get_stats())
            self.dirty = False
