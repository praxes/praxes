"""
"""

from __future__ import absolute_import, with_statement

import copy
import threading

import numpy as np

from .dataset import CorrectedDataProxy, DeadTime, Signal
from .detector import Detector
from .registry import registry
from .utils import simple_eval, sync


class MultiChannelAnalyzer(Detector):

    """
    """

    @property
    def calibration(self):
        cal = simple_eval(self.attrs.get('calibration', '(0,1)'))
        return np.array(cal, 'f')

    @property
    def channels(self):
        if 'channels' in self:
            return self['channels'].value
        return np.arange(self['counts'].shape[-1])

    @property
    def energy(self):
        return np.polyval(self.calibration[::-1], self.channels)

    def _get_pymca_config(self):
        from PyMca.ConfigDict import ConfigDict
        return ConfigDict(simple_eval(self.attrs.get('pymca_config', '{}')))
    def _set_pymca_config(self, config):
        self.attrs['pymca_config'] = str(config)
    pymca_config = property(_get_pymca_config, _set_pymca_config)

    def __init__(self, *args, **kwargs):
        # this whole __init__ is only needed to fix some badly formatted data
        # from early in development of phynx
        super(MultiChannelAnalyzer, self).__init__(*args, **kwargs)

        if 'counts' in self:
            if self['counts'].attrs['class'] != 'McaSpectrum':
                self['counts'].attrs['class'] = 'McaSpectrum'

        # TODO: this could eventually go away
        # old files did not identify dead time properly
        if 'dead_time' in self:
            dt = self['dead_time']
            if not isinstance(dt, DeadTime):
                dt.attrs['class'] = 'DeadTime'
        else:
            if 'dead' in self:
                self['dead_time'] = self['dead']
                self['dead_time'].attrs['class'] = 'DeadTime'
            elif 'dtn' in self:
                data = 100*(1-self['dtn'].value)
                self.create_dataset('dead_time', type='DeadTime', data=data)
            elif 'vtxdtn' in self:
                data = 100*(1-self['vtxdtn'].value)
                self.create_dataset('dead_time', type='DeadTime', data=data)
            else:
                return
            self['dead_time'].attrs['units'] = '%'
            self['dead_time'].attrs['dead_time_format'] = '%'

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

registry.register(MultiChannelAnalyzer)


class McaSpectrum(Signal):

    """
    """

    @property
    def corrected(self):
        try:
            return self._corrected_data_proxy
        except AttributeError:
            self._corrected_data_proxy = CorrectedDataProxy(self)
            return self._corrected_data_proxy

    @property
    def map(self):
        raise TypeError('can not produce a map of a 3-dimensional dataset')

registry.register(McaSpectrum)
