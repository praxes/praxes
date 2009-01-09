"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .detector import Detector
from .group import AcquisitionIterator
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class MultiChannelAnalyzer(Detector):

    """
    """

    def set_calibration(self, cal, order=None):
        with self._lock:
            if order is not None:
                try:
                    assert isinstance(order, int)
                except AssertionError:
                    raise AssertionError('order must be an integer value')
                old = self.calibration
                new = self.calibration
                if len(old) < order:
                    new = numpy.zeros(order+1)
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
        # TODO: use h5py get() when available
        try:
            temp = self.attrs['calibration'].lstrip('(').rstrip(')')
        except h5py.H5Error:
            temp = '0,1'
        return array(temp.split(','), 'f')

    @property
    def channels(self):
        try:
            return self['channels']
        except h5py.H5Error:
            return arange(self['counts'].shape[-1])

    @property
    def energy(self):
        return numpy.polyval(self.calibration[::-1], self.channels)

    @property
    def device_id(self):
        try:
            return self.attrs['id']
        except h5py.H5Error:
            return self.name

    @property
    def iter_mca_counts(self):
        return AcquisitionIterator(self, self['counts'], self.normalization)

    @property
    def normalization(self):
        try:
            norm = self.attrs['normalization']
            if norm in ('', 'None'):
                return 1
            return self[norm].value
        except h5py.H5Error:
            return 1

    def _get_normalization_channel(self):
        try:
            return self.attrs['normalization']
        except h5py.H5Error:
            return ''
    def _set_normalization_channel(self, norm):
        self.attrs['normalization'] = norm
    normalization_channel = property(
        _get_normalization_channel, _set_normalization_channel
    )

    def get_averaged_counts(self, indices=[]):
        if len(indices) > 0:
            spectrum = self['counts'][indices[0], :]*0
            numIndices = len(indices)
            for index in indices:
                if not self.is_valid_index(index):
                    continue
                result = self['counts'][index, :]
                if self.normalization is not None:
                    norm = self.normalization[index]
                    result /= numpy.where(norm==0, numpy.inf, norm)
                spectrum += result
            return spectrum / len(indices)

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
