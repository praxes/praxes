"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from posixpath import basename

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

try:
    from enthought.traits.api import HasTraits
except ImportError:
    class HasTraits(object):
        pass
import h5py
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .base import _PhynxProperties
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class AcquisitionIterator(object):

    """A class for iterating over datasets, even during data acquisition. The
    dataset can either be a phynx dataset or a proxy to a phynx dataset.

    If a datapoint is marked as invalid, it is skipped.

    If the end of the current index is out of range, but smaller than the number
    of points expected for the acquisition (npoints), an IndexError is raised
    instead of StopIteration. This allows the code doing the iteration to assume
    the acquisition is ongoing and continue attempts to iterate until
    StopIteration is encountered. If a scan is aborted, the number of expected
    points must be updated or AcquisitionIterator will never raise
    StopIteration.

    The iterator yields an index, item tuple.
    """

    def __init__(self, dataset):
        self._dataset = dataset

        self._current_index = 0
        self._total_skipped = 0

    def __iter__(self):
        return self

    @property
    def current_index(self):
        return self._current_index

    @property
    def total_skipped(self):
        return self._total_skipped

    def next(self):
        if self._current_index >= self._dataset.npoints:
            raise StopIteration()

        else:
            try:
                try:
                    valid = not self._dataset.masked[self._current_index]
                except TypeError:
                    valid = True
                if valid:
                    i = self._current_index
                    data = self._dataset[i]
                    self._current_index += 1

                    return i, data

                else:
                    self._current_index += 1
                    self._total_skipped += 1
                    return self.next()

            except h5py.H5Error:
                raise IndexError


class Dataset(h5py.Dataset, _PhynxProperties, HasTraits):

    """
    """

    def __init__(self, parent_object, name, *args, **kwargs):
        with parent_object._lock:
            attrs = kwargs.pop('attrs', {})
            if name in parent_object:
                super(Dataset, self).__init__(
                    parent_object, name
                )
            else:
                try:
                    h5kwargs = {
                        'compression':4, 'shuffle':True, 'fletcher32':True
                    }
                    h5kwargs.update(kwargs)
                    super(Dataset, self).__init__(
                        parent_object, name, *args, **h5kwargs
                    )
                except (TypeError, ValueError):
                    # scalar datasets dont allow chunking
                    super(Dataset, self).__init__(
                        parent_object, name, *args, **kwargs
                    )
                self.attrs['class'] = self.__class__.__name__

                _PhynxProperties.__init__(self, parent_object)

                for key, val in attrs.iteritems():
                    self.attrs[key] = val

            self._parent = parent_object

    def __repr__(self):
        with self._lock:
            try:
                return '<%s dataset "%s": shape %s, type "%s" (%d attrs)>'%(
                    self.__class__.__name__,
                    self.name,
                    self.shape,
                    self.dtype.str,
                    len(self.attrs)
                )
            except Exception:
                return "<Closed %s dataset>" % self.__class__.__name__

    @property
    def map(self):
        res = numpy.zeros(self.acquisition_shape, 'f')
        res.flat[:len(self)] = self.value.flat[:]
        return res

    @property
    def masked(self):
        try:
            return self._parent['masked']
        except:
            return None

    @property
    def name(self):
        with self._lock:
            return basename(super(Dataset, self).name)

    @property
    def parent(self):
        return self._parent

    @property
    def path(self):
        with self._lock:
            return super(Dataset, self).name

    def iteritems(self):
        return AcquisitionIterator(self)

registry.register(Dataset)


class Axis(Dataset):

    """
    """

    def __cmp__(self, other):
        with self._lock:
            try:
                assert isinstance(other, Axis)
                return cmp(self.primary, other.primary)
            except AssertionError:
                raise AssertionError(
                    'Cannot compare Axis and %s'%other.__class__.__name__
                )

    @property
    def axis(self):
        try:
            return self.attrs['axis']
        except h5py.H5Error:
            return 0

    @property
    def primary(self):
        try:
            return self.attrs['primary']
        except h5py.H5Error:
            return 0

    @property
    def range(self):
        try:
            temp = self.attrs['range'].lstrip('(').rstrip(')')
            return tuple(float(i) for i in temp.split(','))
        except h5py.H5Error:
            try:
                return (self.value[[0, -1]])
            except IndexError:
                return (0, 0)

registry.register(Axis)


class Signal(Dataset):

    """
    """

    def __cmp__(self, other):
        with self._lock:
            try:
                assert isinstance(other, Signal)
                ss = self.signal if self.signal else 999
                os = other.signal if other.signal else 999
                return cmp(ss, os)
            except AssertionError:
                raise AssertionError(
                    'Cannot compare Signal and %s'%other.__class__.__name__
                )

    @property
    def signal(self):
        try:
            return self.attrs['signal']
        except h5py.H5Error:
            return 0

registry.register(Signal)
