"""
"""

from __future__ import absolute_import, with_statement

import copy
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

    @sync
    def _get_acquired(self):
        return self.attrs.get('acquired', self.npoints)
    @sync
    def _set_acquired(self, value):
        self.attrs['acquired'] = int(value)
    acquired = property(_get_acquired, _set_acquired)

    @property
    @sync
    def entry(self):
        try:
            target = self.parent['/'.join(self.parent.path.split('/')[:2])]
            assert isinstance(target, registry['Entry'])
            return target
        except AssertionError:
            return None

    @property
    @sync
    def map(self):
        res = np.zeros(self.acquisition_shape, self.dtype)
        res.flat[:len(self)] = self.value.flatten()
        return res

    @property
    def masked(self):
        return MaskedProxy(self)

    @property
    def measurement(self):
        try:
            return self.entry.measurement
        except AttributeError:
            return None

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
            if data is None and shape is None:
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
        """enumerate unmasked items"""
        return AcquisitionEnumerator(self)

    @sync
    def mean(self, indices=None):
        if indices is None:
            indices = range(self.acquired)
        elif len(indices):
            indices = [i for i in indices if i < self.acquired]

        res = np.zeros(self.shape[1:], 'f')
        nitems = 0
        for i in indices:
            if not self.masked[i]:
                nitems += 1
                res += self[i]
            print i
        if nitems:
            return res / nitems
        return res

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
            return (self.value[[0, -1]])

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

    def _get_efficiency(self):
        return self.attrs.get('efficiency', 1)
    def _set_efficiency(self, value):
        assert np.isscalar(value)
        self.attrs['efficiency'] = value
    efficiency = property(_get_efficiency, _set_efficiency)

    @property
    def signal(self):
        return self.attrs.get('signal', 0)

    @property
    def corrected_value(self):
        return CorrectedDataProxy(self)

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
        return self.attrs['dead_time_format']
    def _set_format(self, format):
        valid = ('percent', '%', 'fraction', 'normalization', 'correction')
        try:
            assert format in valid
        except AssertionError:
            raise ValueError(
                'dead time format must one of: %r, got %s'
                % (', '.join(valid), format)
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

    """
    A class for iterating over datasets, even during data acquisition. The
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
    @sync
    def current_index(self):
        return copy.copy(self._current_index)

    @property
    def plock(self):
        return self._plock

    @property
    @sync
    def total_skipped(self):
        return copy.copy(self._total_skipped)

    def __init__(self, dataset):
        with dataset.plock:
            self._dataset = dataset
            self._plock = dataset.plock

            self._current_index = 0
            self._total_skipped = 0

    def __iter__(self):
        return self

    @sync
    def next(self):
#        print 'entering next'
        if self.current_index >= self._dataset.npoints:
            raise StopIteration()
        elif self.current_index + 1 > self._dataset.acquired:
            raise IndexError()
        else:
            try:
                i = self.current_index
                if self._dataset.masked[i]:
                    self._total_skipped += 1
                    self._current_index += 1
                    return self.next()

#                print 'getting data for point', i
                res = self._dataset[i]
#                print 'got data for point', i
                self._current_index += 1
#                print 'updated enum index, exiting next'
                return i, res
            except H5Error:
                raise IndexError()


class DataProxy(object):

    @property
    def acquired(self):
        return self._dset.acquired

    @property
    def map(self):
        res = np.zeros(self._dset.acquisition_shape, self._dset.dtype)
        res.flat[:len(self)] = self[:].flatten()
        return res

    @property
    def masked(self):
        return self._dset.masked

    @property
    def npoints(self):
        return self._dset.npoints

    @property
    def plock(self):
        return self._dset.plock

    @property
    def shape(self):
        return self._dset.shape

    def __init__(self, dataset):
        with dataset.plock:
            self._dset = dataset

    @sync
    def __getitem__(self, args):
        raise NotImplementedError(
            '__getitem__ must be implemented by $s' % self.__class__.__name__
        )

    def __len__(self):
        return len(self._dset)

    def enumerate_items(self):
        return AcquisitionEnumerator(self)

    @sync
    def mean(self, indices=None):
        if indices is None:
            indices = range(self.acquired)
        elif len(indices):
            indices = [i for i in indices if i < self.acquired]

        res = np.zeros(self.shape[1:], 'f')
        nitems = 0
        for i in indices:
            if not self.masked[i]:
                nitems += 1
                res += self[i]
            print i
        if nitems:
            return res / nitems
        return res


class CorrectedDataProxy(DataProxy):

    @sync
    def __getitem__(self, key):
        data = self._dset.__getitem__(key)

        try:
            data /= self._dset.efficiency
        except AttributeError:
            pass

        # normalization may be something like ring current or monitor counts
        try:
            norm = self._dset.parent['normalization'].__getitem__(key)
            if norm.shape and len(norm.shape) < len(data.shape):
                newshape = [1]*len(data.shape)
                newshape[:len(norm.shape)] = norm.shape
                norm.shape = newshape
            data /= norm
        except H5Error:
            # fails if normalization is not defined
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


class DeadTimeProxy(DataProxy):

    @property
    def format(self):
        return self._format

    def __init__(self, dataset, format):
        with dataset.plock:
            super(DeadTimeProxy, self).__init__(dataset)

            assert format in (
                'percent', '%', 'fraction', 'normalization', 'correction'
            )
            self._format = format

    @sync
    def __getitem__(self, args):
        if self._dset.format == 'fraction':
            fraction = self._dset.__getitem__(args)
        elif self._dset.format in ('percent', '%'):
            fraction = self._dset.__getitem__(args) / 100.0
        elif self._dset.format == 'correction':
            fraction = self._dset.__getitem__(args) - 1
        elif self._dset.format == 'normalization':
            fraction = 1.0 / self._dset.__getitem__(args) - 1
        else:
            raise ValueError(
                'Unrecognized dead time format: %s' % self._dset.format
            )

        if self.format == 'fraction':
            return fraction
        elif self.format in ('percent', '%'):
            return 100 * fraction
        elif self.format == 'correction':
            return 1 + fraction
        elif self.format == 'normalization':
            return 1 / (1 + fraction)
        else:
            raise ValueError(
                'Unrecognized dead time format: %s' % self.format
            )


class MaskedProxy(DataProxy):

    @property
    def masked(self):
        return self

    @sync
    def __getitem__(self, args):
        try:
            return self._dset.parent['masked'].__getitem__(args)
        except H5Error:
            if isinstance(args, int):
                return False
            return np.zeros(len(self._dset), '?').__getitem__(args)
