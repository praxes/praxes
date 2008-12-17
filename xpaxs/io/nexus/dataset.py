"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Dataset(h5py.Dataset):

    """
    """

    def __init__(self, parent_object, name, *args, **kwargs):
        with parent_object._lock:
            attrs = kwargs.pop('attrs', {})
            super(Dataset, self).__init__(parent_object, name, *args, **kwargs)

            for key, val in attrs.iteritems():
                self.attrs[key] = val

    @property
    def name(self):
        return super(Dataset, self).name.split('/')[-1]

    @property
    def path(self):
        return super(Dataset, self).name

registry.register(Dataset)

class Axis(Dataset):

    """
    """

    def __cmp__(self, other):
        with self._lock:
            try:
                assert isinstance(other, Axis)
                return cmp(self.priority, other.priority)
            except AssertionError:
                raise AssertionError(
                    'Cannot compare Axis and %s'%other.__class__.__name__
                )

    @property
    def axis(self):
        with self._lock:
            try:
                return self.attrs['axis']
            except h5py.H5Error:
                return 999

    @property
    def priority(self):
        with self._lock:
            try:
                return self.attrs['priority']
            except h5py.H5Error:
                return 999

registry.register(Axis)

class Signal(Dataset):

    """
    """

    def __cmp__(self, other):
        with self._lock:
            try:
                assert isinstance(other, Signal)
                return cmp(self.signal, other.signal)
            except AssertionError:
                raise AssertionError(
                    'Cannot compare Signal and %s'%other.__class__.__name__
                )

    @property
    def signal(self):
        with self._lock:
            try:
                return self.attrs['signal']
            except h5py.H5Error:
                return 999

registry.register(Signal)
