"""
"""

from __future__ import absolute_import, with_statement

import copy

import numpy as np

from .dataset import DataProxy, DeadTime, Signal
from .detector import Detector
from .exceptions import H5Error
from .utils import simple_eval, sync


class MultiChannelAnalyzer(Detector):

    """
    """

    @property
    def calibration(self):
        cal = simple_eval(self.attrs.get('calibration', '(0,1)'))
        return np.array(cal, 'f')

    @property
    @sync
    def channels(self):
        if 'channels' in self:
            return self['channels'].value
        return np.arange(self['counts'].shape[-1])

    @property
    @sync
    def energy(self):
        return np.polyval(self.calibration[::-1], self.channels)

    @property
    @sync
    def monitor(self):
        id = self.attrs.get('monitor', None)
        if id is not None:
            return self[id]

    @sync
    def _get_pymca_config(self):
        try:
            return self._pymca_config
        except AttributeError:
            from PyMca.ConfigDict import ConfigDict
            self._pymca_config = ConfigDict(
                simple_eval(self.attrs.get('pymca_config', '{}'))
            )
            return copy.deepcopy(self._pymca_config)
    @sync
    def _set_pymca_config(self, config):
        self._pymca_config = copy.deepcopy(config)
        self.attrs['pymca_config'] = str(config)
    pymca_config = property(_get_pymca_config, _set_pymca_config)

    @sync
    def set_calibration(self, cal, order=None):
        if order is not None:
            try:
                assert isinstance(order, int)
            except AssertionError:
                raise AssertionError('order must be an integer value')
            old = self.calibration
            new = self.calibration
            if len(old) < order:
                new = np.zeros(order+1)
                new[:len(old)] = old
            new[order] = cal
            self.attrs['calibration'] = str(tuple(new))
        else:
            try:
                assert len(cal) > 1
            except AssertionError:
                raise AssertionError(
                    'Expecting a numerical sequence, received %s'%str(cal)
                )
            self.attrs['calibration'] = str(tuple(cal))


class Spectrum(Signal):

    """
    """

    @property
    @sync
    def corrected_value(self):
        return CorrectedSpectrumProxy(self)

    @property
    def map(self):
        raise TypeError('can not produce a map of a 3-dimensional dataset')


class McaSpectrum(Spectrum):

    """
    This is just a compatibility class, Spectrum should be used instead
    """


class CorrectedSpectrumProxy(DataProxy):

    @sync
    def __getitem__(self, key):
        with self._dset.plock:
            data = self._dset.__getitem__(key)

            try:
                norm = self._dset.efficiency
                if norm is not None:
                    data /= norm
            except AttributeError:
                pass

            try:
                norm = (
                    self._dset.parent.pymca_config['concentrations']['time'] *
                    self._dset.parent.pymca_config['concentrations']['flux'] /
                    self._dset.parent.monitor.corrected_value.__getitem__(key)
                )
                if not np.isscalar(norm) and len(norm.shape) < len(data.shape):
                    newshape = [1]*len(data.shape)
                    newshape[:len(norm.shape)] = norm.shape
                    norm.shape = newshape
                data *= norm
            except (KeyError, TypeError, AttributeError):
                # fails if monitor is None or modeled intensity can not be found
                pass

            # detector deadtime correction
            try:
                dtc = self._dset.parent['dead_time'].correction.__getitem__(key)
                if isinstance(dtc, np.ndarray) \
                        and len(dtc.shape) < len(data.shape):
                    newshape = [1]*len(data.shape)
                    newshape[:len(dtc.shape)] = dtc.shape
                    dtn.shape = newshape
                data *= dtc
            except H5Error:
                # fails if dead_time_correction is not defined
                pass

            return data
