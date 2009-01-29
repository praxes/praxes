"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .detector import Detector
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
        return numpy.array(temp.split(','), 'f')

    @property
    def channels(self):
        try:
            return self['channels'].value
        except h5py.H5Error:
            return numpy.arange(self['counts'].shape[-1])

    @property
    def energy(self):
        return numpy.polyval(self.calibration[::-1], self.channels)

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
