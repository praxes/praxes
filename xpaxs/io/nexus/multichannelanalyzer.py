"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



# TODO: fix this import:
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
                old = self.attrs['calibration']
                new = self.attrs['calibration']
                if len(old) < order:
                    new = numpy.zeros(order+1)
                    new[:len(old)] = old
                new[order] = cal
                self.attrs['calibration'] = new
            else:
                try:
                    assert len(cal) > 1
                except AssertionError:
                    raise AssertionError(
                        'Expecting a numerical sequence, received %s'%str(cal))
                self.attrs['calibration'] = cal

    @property
    def calibration(self):
        with self._lock:
            try:
                return self.attrs['calibration']
            except h5py.H5Error:
                return numpy.array([0, 1], 'f')

    @property
    def channels(self):
        with self._lock:
            try:
                return self['channels']
            except h5py.H5Error:
                return arange(self['counts'].shape[-1])

    @property
    def energy(self):
        with self._lock:
            return numpy.polyval(self.calibration, self.channels)

registry.register(MultiChannelAnalyzer)
