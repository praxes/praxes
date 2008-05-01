"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import hashlib
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

    def __init__(self, scan, config, parent=None):
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

        settings = QtCore.QSettings()
        settings.beginGroup('PPJobServers')
        ncpus, ok = settings.value('LocalProcesses',
                                 QtCore.QVariant(1)).toInt()
        self.jobServer = pp.Server(ncpus, ('*',))
        # TODO: make this configurable
        self.jobServer.set_ncpus(ncpus)
        self.numCpus = numpy.sum([i for i in
                        self.jobServer.get_active_nodes().itervalues()])
        self.numQueued = 0
        self.numProcessed = 0
        self.expectedLines = self.scan.getNumExpectedScanLines()

        self.queue = Queue.Queue()
        for i in self.scan.getValidDataPoints():
            self.queue.put(i)

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

            self.queueNext()

            self.jobServer.wait()

            time.sleep(0.01)
            self.expectedLines = self.scan.getNumExpectedScanLines()
            if self.expectedLines <= (self.numProcessed): return

    def queueNext(self):
        try:
            self.mutex.lock()
            while self.numQueued < self.numCpus*2:
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
        try:
            self.mutex.lock()
            self.numQueued -= 1
            self.numProcessed += 1
            self.emit(QtCore.SIGNAL('percentComplete'),
                      100*self.numProcessed/self.expectedLines)
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

        try:
            if not self.isStopped():
                self.queueNext()
        except Queue.Empty: pass

    def report(self):
        if self.dirty:
            self.emit(QtCore.SIGNAL("dataProcessed"))
            self.emit(QtCore.SIGNAL("ppJobStats"), self.jobServer.get_stats())
            self.dirty = False
