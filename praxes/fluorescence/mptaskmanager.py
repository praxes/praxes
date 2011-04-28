"""
"""
from __future__ import with_statement

import copy
#import logging
import multiprocessing
import sys
import time

import numpy as np
from PyMca import ClassMcaTheory
from PyMca.ConcentrationsTool import ConcentrationsTool
import numpy as np
np.seterr(all='ignore')

from praxes.dispatch.mptaskmanager import TaskManager


#logger = logging.getLogger(__file__)
DEBUG = False


def init(config):
    global advanced_fit, mass_fraction_tool
    from PyMca.ClassMcaTheory import McaTheory
    config['fit']['use_limit'] = 1
    advanced_fit = McaTheory(config=config)
    advanced_fit.enableOptimizedLinearFit()
    if 'concentrations' in config:
        mass_fraction_tool = ConcentrationsTool(config['concentrations'])
        mass_fraction_tool.config['time'] = 1
    else:
        mass_fraction_tool = None


def analyze_spectrum(index, spectrum, monitor):
    start = time.time()
    advanced_fit.setdata(y=spectrum)
    advanced_fit.estimate()
    estimate = time.time()
    if (mass_fraction_tool is not None) and (advanced_fit._fluoRates is None):
        fitresult, result = advanced_fit.startfit(digest=1)
    else:
        fitresult = advanced_fit.startfit(digest=0)
        result = advanced_fit.imagingDigestResult()
    result['index'] = index
    fit = time.time()

    if mass_fraction_tool is not None:
        temp = {}
        temp['fitresult'] = fitresult
        temp['result'] = result
        temp['result']['config'] = advanced_fit.config
        mass_fraction_tool.config['time'] = 1
        mass_fraction_tool.config['flux'] = monitor
        conc = mass_fraction_tool.processFitResult(
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
        'report': report
    }


class XfsTaskManager(TaskManager):

    @property
    def advanced_fit(self):
        with self.lock:
            return copy.deepcopy(self._advanced_fit)
    @advanced_fit.setter
    def advanced_fit(self, val):
        with self.lock:
            self._advanced_fit = val

    @property
    def mass_fraction_tool(self):
        with self.lock:
            return copy.copy(self._mass_fraction_tool)
    @mass_fraction_tool.setter
    def mass_fraction_tool(self, val):
        with self.lock:
            self._mass_fraction_tool = val

    def __init__(self, scan, config, progress_queue, **kwargs):
        # needs to be set before the super call:
        self._config = config
        super(XfsTaskManager, self).__init__(scan, progress_queue, **kwargs)

        with scan:
            self._measurement = scan.entry.measurement
            self._indices = self._measurement.scalar_data['i']
            self._masked = self._measurement.masked
            try:
                # are we processing a group of mca elements...
                mcas = scan.mcas.values()
                self._counts = [mca['counts'] for mca in mcas]
                self._monitor = getattr(
                    mcas[0].monitor, 'corrected_value', None
                    )
            except AttributeError:
                # or a single element?
                self._counts = [scan['counts']]
                self._monitor = getattr(scan.monitor, 'corrected_value', None)

    def create_pool(self):

        return multiprocessing.Pool(
            self.n_cpus, init, (self._config,)
            )

    def next(self):
        i = self._next_index
        if i >= self.n_points:
            raise StopIteration()

        with self.scan:
            try:
                suspect = i != self._indices[i]
            except IndexError:
                suspect = True
            if suspect:
                if i >= self._measurement.entry.npoints:
                    # entry.npoints has changed, scan was aborted
                    raise StopIteration()
                # expected the datapoint, but not yet acquired
                return None

            self._next_index = i + 1

            if self._masked[i]:
                return 0

            cts = [counts.corrected_value[i] for counts in self._counts]
            spectrum = np.sum(cts, 0)

            monitor = None
            if self._monitor is not None:
                monitor = self._monitor[i]

        return analyze_spectrum, (i, spectrum, monitor)

    def update_element_map(self, element, map_type, index, val):
        with self.scan:
            try:
                entry = '%s_%s'%(element, map_type)
                self.scan['element_maps'][entry][index] = val
            except ValueError:
                print "index %d out of range for %s" % (index, entry)
            except KeyError:
                print "%s not found in element_maps" % entry
            except TypeError:
                print entry, index, val

    def update_records(self, data):
        if data is None:
            return

        index = data['index']

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
            for key, val in mass_fractions.items():
                k = key.replace(' ', '_')
                self.update_element_map(k, 'mass_fraction', index, val)
        except KeyError:
            pass
