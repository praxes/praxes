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

def analyze_spectrum(index, spectrum, tconf, advanced_fit, mass_fraction_tool):
    start = time.time()
    advanced_fit.config['fit']['use_limit'] = 1
    # TODO: get the channels from the controller
    advanced_fit.setdata(y=spectrum)
    advanced_fit.estimate()
    estimate = time.time()
    if ('concentrations' in advanced_fit.config) and \
            (advanced_fit._fluoRates is None):
        fitresult, result = advanced_fit.startfit(digest=1)
    else:
        fitresult = advanced_fit.startfit(digest=0)
        result = advanced_fit.imagingDigestResult()
    result['index'] = index
    fit = time.time()

    if mass_fraction_tool:
        temp = {}
        temp['fitresult'] = fitresult
        temp['result'] = result
        temp['result']['config'] = advanced_fit.config
        tconf.update(advanced_fit.configure()['concentrations'])
        conc = mass_fraction_tool.processFitResult(
            config=tconf,
            fitresult=temp,
            elementsfrommatrix=False,
            fluorates=advanced_fit._fluoRates
            )
        result['concentrations'] = conc
    fitconc = time.time()
    report = {'estimate':estimate-start,
              'fit': fit-estimate,
              'fitconc': fitconc-fit}

    return {
        'index': index,
        'result': result,
        'advanced_fit': advanced_fit,
        'report': report
    }


class MultiMcaAcquisitionEnumerator(object):

    """
    A class for iterating over datasets, even during data acquisition.

    If a datapoint is marked as masked or invalid, it is skipped and not
    included in the enumeration.

    If the current index is out of range, but smaller than the number of points
    expected for the acquisition (npoints), an IndexError is raised instead of
    StopIteration. This allows the code doing the iteration to assume the
    acquisition is ongoing and continue attempts to iterate until StopIteration
    is encountered. If a scan is aborted, the number of expected points must be
    updated or AcquisitionEnumerator will never raise StopIteration.

    The enumerator yields an index, item_list tuple.
    """

    def __init__(self, measurement):
        self._measurement = measurement
        self._mcas = measurement.mcas.values()
        self._next_index = 0

    def __iter__(self):
        return self

    def next(self):
        i = self._next_index
        if i >= self._measurement.npoints:
            raise StopIteration()
        elif i + 1 > self._measurement.acquired:
            # expected the datapoint, but not yet acquired
            return None

        self._next_index = i + 1

        if self._measurement.masked[i]:
            return i, None

        return i, np.sum([mca.corrected_value[i] for mca in self._mcas], 0)


class XfsPPTaskManager(PPTaskManager):

    @property
    def advanced_fit(self):
        with self.lock:
            return self._advanced_fit
    @advanced_fit.setter
    def advanced_fit(self, val):
        with self.lock:
            self._advanced_fit = val

    @property
    def mass_fraction_tool(self):
        with self.lock:
            return self._mass_fraction_tool
    @mass_fraction_tool.setter
    def mass_fraction_tool(self, val):
        with self.lock:
            self._mass_fraction_tool = val

    @property
    def tconf(self):
        with self.lock:
            return self._tconf
    @tconf.setter
    def tconf(self, val):
        with self.lock:
            self._tconf = val

    def __init__(self, scan, config, parent=None):
        super(XfsPPTaskManager, self).__init__(scan, parent)

        self.advanced_fit = ClassMcaTheory.McaTheory(config=config)
        self.advanced_fit.enableOptimizedLinearFit()
        self.mass_fraction_tool = None
        if 'concentrations' in config:
            self.mass_fraction_tool = ConcentrationsTool(config)
            self.tconf = self.mass_fraction_tool.configure()

    def __iter__(self):
        return MultiMcaAcquisitionEnumerator(self.scan)

    def submit_job(self, index, data):
        args = (
            index, data, self.tconf, self.advanced_fit,
            self.mass_fraction_tool
        )
        self.job_server.submit(
            analyze_spectrum,
            args,
            modules=("time", ),
            callback=self.update_records
        )

    def update_element_map(self, element, map_type, index, val):
        try:
            entry = '%s_%s'%(element, map_type)
            self.scan['element_maps'][entry][index] = val
        except ValueError:
            print "index %d out of range for %s", index, entry
        except KeyError:
            print "%s not found in element_maps", entry

    def update_records(self, data):
        with self.lock:
            index = data['index']
            self.advanced_fit = data['advanced_fit']

            result = data['result']
            for group in result['groups']:
                g = group.replace(' ', '_')

                fit_area = result[group]['fitarea']
                if fit_area:
                    sigma_area = result[group]['sigmaarea']/fit_area
                else:
                    sigma_area = np.nan

                self.update_element_map(g, 'fit', index, fit_area)
                self.update_element_map(g, 'fit_error', index, sigma_area)

            try:
                mass_fractions = result['concentrations']['mass fraction']
                for key, val in mass_fractions.iteritems():
                    k = key.replace(' ', '_')
                    self.update_element_map(k, 'mass_fraction', index, val)
            except KeyError:
                pass

            self.dirty = True
            self.report_stats()
