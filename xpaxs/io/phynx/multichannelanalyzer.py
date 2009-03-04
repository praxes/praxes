"""
"""

from __future__ import absolute_import, with_statement

import copy
import threading

import h5py
import numpy as np

from .dataset import AcquisitionIterator, Signal
from .detector import Detector
from .registry import registry
from .utils import simple_eval, sync


class MultiChannelAnalyzer(Detector):

    """
    """
    def __init__(self, *args, **kwargs):
        # this whole __init__ is only needed to fix some badly formatted data
        # from early in development of phynx
        super(MultiChannelAnalyzer, self).__init__(*args, **kwargs)
        with self._lock:
            try:
                if self['counts'].attrs['class'] != 'McaSpectrum':
                    self['counts'].attrs['class'] = 'McaSpectrum'
            except h5py.H5Error:
                pass

            # TODO: this could eventually go away
            if 'dead_time' not in self:
                self._set_dead_time()

    def _set_dead_time(self):
        if 'dead' in self:
            self['dead_time'] = self['dead']
        elif 'dtn' in self:
            data = 100*(1-self['dtn'].value)
            self.create_dataset('dead_time', data=data)
        elif 'vtxdtn' in self:
            data = 100*(1-self['vtxdtn'].value)
            self.create_dataset('dead_time', data=data)
        else:
            return
        self['dead_time'].attrs['units'] = '%'

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

    @property
    def calibration(self):
        cal = simple_eval(self.attrs.get('calibration', '(0,1)'))
        return np.array(cal, 'f')

    @property
    def channels(self):
        try:
            return self['channels'].value
        except h5py.H5Error:
            return np.arange(self['counts'].shape[-1])

    @property
    def energy(self):
        return np.polyval(self.calibration[::-1], self.channels)

    def _get_pymca_config(self):
        try:
            from PyMca.ConfigDict import ConfigDict
            return ConfigDict(eval(self.attrs['pymca_config']))
        except h5py.H5Error:
            return None
    def _set_pymca_config(self, config):
        self.attrs['pymca_config'] = str(config)
    pymca_config = property(_get_pymca_config, _set_pymca_config)

registry.register(MultiChannelAnalyzer)


class CorrectedDataProxy(object):

    def __init__(self, dataset):
#        self._lock = threading.RLock()
        self._lock = dataset._lock
        self._dataset = dataset

    @property
    def masked(self):
        return self._dataset.masked

    @property
    def npoints(self):
        return self._dataset.npoints

    @sync
    def __getitem__(self, key):
        data = self._dataset[key]

        # normalization may be something like ring current or monitor counts
        try:
            norm = self._dataset.parent['normalization'][key]
            if norm.shape and len(norm.shape) < len(data.shape):
                newshape = [1]*len(data.shape)
                newshape[:len(norm.shape)] = norm.shape
                norm.shape = newshape
            data /= norm
        except h5py.H5Error:
            # fails if normalization is not defined
            pass

        # detector deadtime correction
        try:
            dtn = 1-self._dataset.parent['dead_time'][key]/100
            if isinstance(dtn, np.ndarray) \
                    and len(dtn.shape) < len(data.shape):
                newshape = [1]*len(data.shape)
                newshape[:len(dtn.shape)] = dtn.shape
                dtn.shape = newshape
            data /= dtn
        except h5py.H5Error:
            # fails if dead_time_correction is not defined
            pass

        return data

    def __len__(self):
        return len(self._dataset)

    def iteritems(self):
        return AcquisitionIterator(self)

    @sync
    def get_averaged_counts(self, indices=[]):
        if not len(indices):
            indices = range(len(self))
        if len(indices) == 0:
            return

        result = np.zeros(len(self[indices[0]]), 'f')
        numIndices = len(indices)
        total_valid = 0
        for index in indices:
            try:
                valid = not self._dataset.masked[index]
            except TypeError:
                valid = True
            if valid:
                temp = self[index]
                result += temp
                total_valid += 1

        return result / total_valid


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
