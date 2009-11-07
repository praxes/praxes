"""
"""
from __future__ import with_statement

import logging
import time

import numpy as np
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

    def _get_advancedFit(self):
        with self.lock:
            return self._advancedFit
    def _set_advancedFit(self, val):
        with self.lock:
            self._advancedFit = val
    advancedFit = property(_get_advancedFit, _set_advancedFit)

    def _get_mfTool(self):
        with self.lock:
            return self._mfTool
    def _set_mfTool(self, val):
        with self.lock:
            self._mfTool = val
    mfTool = property(_get_mfTool, _set_mfTool)

    def _get_tconf(self):
        with self.lock:
            return self._tconf
    def _set_tconf(self, val):
        with self.lock:
            self._tconf = val
    tconf = property(_get_tconf, _set_tconf)

    def __init__(self, scan, enumerator, config, parent=None):
        super(XfsPPTaskManager, self).__init__(scan, enumerator, parent)

        self.advancedFit = ClassMcaTheory.McaTheory(config=config)
        self.advancedFit.enableOptimizedLinearFit()
        self.mfTool = None
        if 'concentrations' in config:
            self.mfTool = ConcentrationsTool(config)
            self.tconf = self.mfTool.configure()

    def submitJob(self, index, data):
        args = (
            index, data, self.tconf, self.advancedFit,
            self.mfTool
        )
        self.jobServer.submit(
            analyzeSpectrum,
            args,
            modules=("time", ),
            callback=self.updateRecords
        )

    def updateElementMap(self, element, mapType, index, val):
        try:
            entry = '%s_%s'%(element, mapType)
            self.scan['element_maps'][entry][index] = val
        except ValueError:
            print "index %d out of range for %s", index, entry
        except KeyError:
            print "%s not found in element_maps", entry

    def updateRecords(self, data):
        with self.lock:
            index = data['index']
            self.advancedFit = data['advancedFit']
            self._totalProcessed += 1

            result = data['result']
            for group in result['groups']:
                g = group.replace(' ', '_')

                fitArea = result[group]['fitarea']
                if fitArea:
                    sigmaArea = result[group]['sigmaarea']/fitArea
                else:
                    sigmaArea = np.nan

                self.updateElementMap(g, 'fit', index, fitArea)
                self.updateElementMap(g, 'fit_error', index, sigmaArea)

            try:
                massFractions = result['concentrations']['mass fraction']
                for key, val in massFractions.iteritems():
                    k = key.replace(' ', '_')
                    self.updateElementMap(k, 'mass_fraction', index, val)
            except KeyError:
                pass

            self.dirty = True
            self.reportStats()
