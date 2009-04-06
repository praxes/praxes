"""
"""
from __future__ import with_statement

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

    def __init__(self, enumerator, config, scan, parent=None):
        super(XfsPPTaskManager, self).__init__(enumerator, parent)

        with self.lock:
            self.scan = scan

            self.config = config

            self.advancedFit = ClassMcaTheory.McaTheory(config=config)
            self.advancedFit.enableOptimizedLinearFit()
            self.mfTool = None
            if 'concentrations' in config:
                self.mfTool = ConcentrationsTool(config)
                self.tconf = self.mfTool.configure()

    def submitJob(self, index, data):
        with self.lock:
            args = (
                index, data, self.tconf, self.advancedFit,
                self.mfTool
            )
            self._jobServer.submit(
                analyzeSpectrum,
                args,
                modules=("time", ),
                callback=self.updateRecords
            )

    def updateElementMap(self, element, mapType, index, val):
        with self.lock:
            try:
                entry = '%s_%s'%(element, mapType)
                self.scan['element_maps'][entry][index] = val
            except ValueError:
                print index, node

    def updateRecords(self, data):
        if data:
            with self.lock:
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
                if DEBUG: print 'records updated'
            self.report()
