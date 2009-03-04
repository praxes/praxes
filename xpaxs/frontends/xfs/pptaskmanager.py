"""
"""

import logging
import time

import pp
from PyMca import ClassMcaTheory
from PyMca.ConcentrationsTool import ConcentrationsTool
from PyQt4 import QtCore
import numpy as np
np.seterr(all='ignore')

from xpaxs.dispatch.pptaskmanager import PPTaskManager


logger = logging.getLogger(__file__)
DEBUG = False

def flat_to_nd(index, shape):
    res = []
    for i in xrange(1, len(shape)):
        p = np.product(shape[i:])
        res.append(index//p)
        index = index % p
    res.append(index)
    return tuple(res)

def analyzeSpectrum(index, spectrum, tconf, advancedFit, mfTool):
    start = time.time()
    advancedFit.config['fit']['use_limit'] = 1
    # TODO: get the channels from the controller
    advancedFit.setdata(y=spectrum)
    advancedFit.estimate()
    estimate = time.time()
    if ('concentrations' in advancedFit.config) and \
            (advancedFit._fluoRates is None):
        fitresult, result = advancedFit.startfit(digest=1)
    else:
        fitresult = advancedFit.startfit(digest=0)
        result = advancedFit.imagingDigestResult()
    result['index'] = index
    fit = time.time()

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
    fitconc = time.time()
    report = {'estimate':estimate-start,
              'fit': fit-estimate,
              'fitconc': fitconc-fit}

    return {
        'index': index,
        'result': result,
        'advancedFit': advancedFit,
        'report': report
    }


class XfsPPTaskManager(PPTaskManager):

    def _submitJobs(self, numJobs):
        try:
            self.mutex.lock()
            for i in range(numJobs):
                try:
                    index, data = self.iterData.next()
                    args = (
                        index, data, self.tconf, self.advancedFit, self.mfTool
                    )
                    self.jobServer.submit(
                        analyzeSpectrum,
                        args,
                        modules=("time", ),
                        callback=self.updateRecords
                    )
                except IndexError:
                    break
        finally:
            self.mutex.unlock()

    def setData(self, scan, config):
        self.scan = scan
        self.iterData = scan.mcas.values()[0]['counts'].corrected.iteritems()
        self._totalProcessed = 0

        self.config = config

        self.advancedFit = ClassMcaTheory.McaTheory(config=config)
        self.advancedFit.enableOptimizedLinearFit()
        self.mfTool = None
        if 'concentrations' in config:
            self.mfTool = ConcentrationsTool(config)
            self.tconf = self.mfTool.configure()

    def updateElementMap(self, element, mapType, index, val):
        try:
            entry = '%s_%s'%(element, mapType)
            self.scan['element_maps'][entry][index] = val
        except ValueError:
            print index, node

    def updateRecords(self, data):
        if data:
            try:
                self.mutex.lock()
                if DEBUG: print 'Updating records'

                self.advancedFit = data['advancedFit']
                shape = self.scan.acquisition_shape
                index = data['index']

                self._totalProcessed += 1

                result = data['result']
                for group in result['groups']:
                    g = group.replace(' ', '_')

                    fitArea = result[group]['fitarea']
                    if fitArea: sigmaArea = result[group]['sigmaarea']/fitArea
                    else: sigmaArea = np.nan

                    self.updateElementMap(g, 'fit', index, fitArea)
                    self.updateElementMap(g, 'fit_error', index, sigmaArea)

                if 'concentrations' in result:
                    massFractions = result['concentrations']['mass fraction']
                    for key, val in massFractions.iteritems():
                        k = key.replace(' ', '_')
                        self.updateElementMap(k, 'mass_fraction', index, val)
                self.dirty = True
                track = self._totalProcessed + self.iterData.total_skipped
                self.emit(
                    QtCore.SIGNAL('percentComplete'),
                    (100.0 * track) / self.scan.npoints
                )
                if DEBUG: print 'records updated'
            finally:
                self.mutex.unlock()
