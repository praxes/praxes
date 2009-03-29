"""
"""

from __future__ import absolute_import, with_statement

import posixpath

import h5py
import numpy as np

from .base import _PhynxProperties
from .exceptions import H5Error
from .registry import registry
from .utils import simple_eval, sync


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
        return MaskedProxy(self)

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

    def enumerate_items(self):
        return AcquisitionEnumerator(self)

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
        except H5Error:
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


class DeadTime(Signal):

    """
    The native format of the dead time data needs to be specified. This can be
    done when creating a new DeadTime dataset by passing a dead_time_format
    keyword argument with one of the following values:

    * 'percent' - the percent of the real time that the detector is not live
    * '%' - same as 'percent'
    * 'fraction' - the fraction of the real time that the detector is not live
    * 'normalization' - data is corrected by dividing by the dead time value
    * 'correction' - data is corrected by muliplying by the dead time value

    Alternatively, the native format can be specified after the fact by setting
    the format property to one of the values listed above.
    """

    @property
    def correction(self):
        return DeadTimeProxy(self, 'correction')

    @property
    def percent(self):
        return DeadTimeProxy(self, 'percent')

    @property
    def fraction(self):
        return DeadTimeProxy(self, 'fraction')

    @property
    def normalization(self):
        return DeadTimeProxy(self, 'normalization')

    def _get_format(self):
        return self.attrs.get('dead_time_format', 'Format not specified')
    def _set_format(self, format):
        valid = ('percent', '%', 'fraction', 'normalization', 'correction')
        try:
            assert format in valid
        except AssertionError:
            raise ValueError(
                'dead time format must one of: %r' % (', '.join(valid))
            )
        self.attrs['dead_time_format'] = format
    format = property(_get_format, _set_format)

    def __init__(self, *args, **kwargs):
        format = kwargs.pop('dead_time_format', None)
        super(DeadTime, self).__init__(*args, **kwargs)

        if format:
            self.format = format

registry.register(DeadTime)


class AcquisitionEnumerator(object):

    """A class for iterating over datasets, even during data acquisition. The
    dataset can either be a phynx dataset or a proxy to a phynx dataset.

    If a datapoint is marked as invalid, it is skipped.

    If the end of the current index is out of range, but smaller than the number
    of points expected for the acquisition (npoints), an IndexError is raised
    instead of StopIteration. This allows the code doing the iteration to assume
    the acquisition is ongoing and continue attempts to iterate until
    StopIteration is encountered. If a scan is aborted, the number of expected
    points must be updated or AcquisitionEnumerator will never raise
    StopIteration.

    The enumerator yields an index, item tuple.
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
                i = self._current_index
                self._current_index += 1
                if self._dataset.masked[i]:
                    self._total_skipped += 1
                    return self.next()

                return i, self._dataset[i]
            except H5Error:
                raise IndexError


class DeadTimeProxy(object):

    _valid = ('percent', '%', 'fraction', 'normalization', 'correction')

    def __init__(self, dset, format):
        self._dset = dset

        assert format in self._valid
        self._format = format

    def __getitem__(self, args):
        if self._dset.format in ('percent', '%'):
            fraction = self._dset.__getitem__(args) / 100.0
        elif self._dset.format == 'correction':
            fraction = self._dset.__getitem__(args) - 1
        elif self._dset.format == 'normalization':
            fraction = 1.0 / self._dset.__getitem__(args) - 1
        elif self._dset.format == 'fraction':
            fraction = self._dset.__getitem__(args)
        else:
            raise ValueError('Unrecognized dead time format')

        if self._format in ('percent', '%'):
            return 100 * fraction
        elif self._format == 'correction':
            return 1 + fraction
        elif self._format == 'normalization':
            return 1 / (1 + fraction)
        else:
            return fraction


class MaskedProxy(object):

    def __init__(self, dset):
        self._dset = dset

        try:
            self._dset_mask = dset.parent['masked']
        except H5Error:
            self._dset_mask = None

    def __getitem__(self, args):
        with self._dset.plock:
            if self._dset_mask is not None:
                return self._dset_mask.__getitem__(args)
            else:
                if isinstance(args, int):
                    return False
                return np.zeros(len(self._dset), '?').__getitem__(args)
