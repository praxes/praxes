"""
"""

from __future__ import absolute_import, with_statement

import posixpath

import h5py
import numpy as np

from .base import _PhynxProperties
from .registry import registry
from .utils import simple_eval, sync


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

    @property
    def current_index(self):
        return self._current_index

    @property
    def total_skipped(self):
        return self._total_skipped

    def __init__(self, dataset):
        self._dataset = dataset

        self._current_index = 0
        self._total_skipped = 0

    def __iter__(self):
        return self

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


class Dataset(h5py.Dataset, _PhynxProperties):

    """
    """

    @property
    def map(self):
        res = np.zeros(self.acquisition_shape, 'f')
        res.flat[:len(self)] = self.value.flat[:]
        return res

    @property
    def masked(self):
        return self.parent.get('masked', None)

    @property
    @sync
    def name(self):
        return posixpath.basename(super(Dataset, self).name)

    @property
    @sync
    def path(self):
        return super(Dataset, self).name

    @property
    @sync
    def parent(self):
        p = posixpath.split(self.path)[0]
        g = h5py.Group(self, p, create=False)
        t = g.attrs.get('class', 'Group')
        return registry[t](self, p)

    def __init__(
        self, parent_object, name, shape=None, dtype=None, data=None,
        chunks=None, compression='gzip', shuffle=None, fletcher32=None,
        maxshape=None, compression_opts=None, **kwargs
    ):
        """
        The following args and kwargs
        """
        with parent_object.plock:
            if name in parent_object:
                h5py.Dataset.__init__(self, parent_object, name)
                _PhynxProperties.__init__(self, parent_object)
            else:
                h5py.Dataset.__init__(
                    self, parent_object, name, shape=shape, dtype=dtype,
                    data=data, chunks=chunks, compression=compression,
                    shuffle=shuffle, fletcher32=fletcher32, maxshape=maxshape,
                    compression_opts=compression_opts
                )
                _PhynxProperties.__init__(self, parent_object)

                self.attrs['class'] = self.__class__.__name__

            for key, val in kwargs.iteritems():
                if not np.isscalar(val):
                    val = str(val)
                self.attrs[key] = val

    @sync
    def __repr__(self):
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

    def iteritems(self):
        return AcquisitionIterator(self)

registry.register(Dataset)


class Axis(Dataset):

    """
    """

    @property
    def axis(self):
        return self.attrs.get('axis', 0)

    @property
    def primary(self):
        return self.attrs.get('primary', 0)

    @property
    def range(self):
        try:
            return simple_eval(self.attrs['range'])
        except h5py.H5Error:
            try:
                return (self.value[[0, -1]])
            except IndexError:
                return (0, 0)

    @sync
    def __cmp__(self, other):
        try:
            assert isinstance(other, Axis)
            return cmp(self.primary, other.primary)
        except AssertionError:
            raise AssertionError(
                'Cannot compare Axis and %s'%other.__class__.__name__
            )

registry.register(Axis)


class Signal(Dataset):

    """
    """

    @property
    def signal(self):
        return self.attrs.get('signal', 0)

    @sync
    def __cmp__(self, other):
        try:
            assert isinstance(other, Signal)
            ss = self.signal if self.signal else 999
            os = other.signal if other.signal else 999
            return cmp(ss, os)
        except AssertionError:
            raise AssertionError(
                'Cannot compare Signal and %s'%other.__class__.__name__
            )

registry.register(Signal)
