"""
"""

from __future__ import absolute_import, with_statement

import copy
import json
import posixpath

import h5py
import numpy as np

from .base import Node
from .registry import registry
from .utils import memoize, simple_eval, sync


class Dataset(Node):

    """
    """

    @property
    def dtype(self):
        return self._h5node.dtype

    @property
    @sync
    def map(self):
        shape = [np.prod(self.entry.acquisition_shape)]
        shape.extend(self.shape[1:])
        res = np.zeros(shape, self._h5node.dtype)
        res[:len(self)] = self._h5node[...]
        res.shape = self.entry.acquisition_shape
        if self.entry.acquisition_command.startswith('zzmesh'):
            for i, val in enumerate(res):
                if i%2:
                    res[i] = np.array(val[::-1])
        return res

    @property
    def shape(self):
        return self._h5node.shape

#    def __init__(
#        self, parent_object, name, shape=None, dtype=None, data=None,
#        chunks=None, compression='gzip', shuffle=None, fletcher32=None,
#        maxshape=None, compression_opts=None, **kwargs
#    ):
#        if data is None and shape is None:
#            h5py.Dataset.__init__(self, parent_object, name)
#            _PhynxProperties.__init__(self, parent_object)
#        else:
#            h5py.Dataset.__init__(
#                self, parent_object, name, shape=shape, dtype=dtype,
#                data=data, chunks=chunks, compression=compression,
#                shuffle=shuffle, fletcher32=fletcher32, maxshape=maxshape,
#                compression_opts=compression_opts
#            )
#            _PhynxProperties.__init__(self, parent_object)
#
#            self.attrs['class'] = self.__class__.__name__
#
#        for key, val in kwargs.iteritems():
#            if not np.isscalar(val):
#                val = str(val)
#            self.attrs[key] = val

    def __getitem__(self, args):
        return self._h5node.__getitem__(args)

    def __setitem__(self, args, vals):
        self._h5node.__setitem__(args, vals)

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

    @sync
    def mean(self, indices=None):
        acquired = self.entry.acquired
        if indices is None:
            indices = range(acquired)
        elif len(indices):
            indices = [i for i in indices if i < acquired]

        res = np.zeros(self.shape[1:], 'f')
        nitems = 0
        mask = self.measurement.masked
        for i in indices:
            if not mask[i]:
                nitems += 1
                res += self[i]
        if nitems:
            return res / nitems
        return res


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
        temp = self.attrs.get('range', None)
        if temp is None:
            return self[[0, -1]]
        try:
            return json.loads(temp)
        except ValueError:
            return json.loads(temp.replace('(', '[').replace(')', ']'))

    @sync
    def __cmp__(self, other):
        try:
            assert isinstance(other, Axis)
            return cmp(self.primary, other.primary)
        except AssertionError:
            raise AssertionError(
                'Cannot compare Axis and %s'%other.__class__.__name__
            )


class Signal(Dataset):

    """
    """

    @property
    def efficiency(self):
        return self.attrs.get('efficiency', 1)
    @efficiency.setter
    def efficiency(self, value):
        self.attrs['efficiency'] = float(value)

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


class ImageData(Signal):

    """
    """


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

    @property
    def format(self):
        return self.attrs['dead_time_format']

    def __init__(self, *args, **kwargs):
        format = kwargs.pop('dead_time_format', None)
        super(DeadTime, self).__init__(*args, **kwargs)

        if format:
            valid = ('percent', '%', 'fraction', 'normalization', 'correction')
            if format not in valid:
                raise ValueError(
                    'dead time format must one of: %r, got %s'
                    % (', '.join(valid), format)
                    )
            self.attrs['dead_time_format'] = format


class DataProxy(object):

    @property
    def map(self):
        res = self._dset[...]
        res.shape = self._dset.entry.acquisition_shape
        return res

    @property
    def shape(self):
        return self._dset.shape

    def __init__(self, dataset):
        self._dset = dataset
        self._lock = dataset._lock

    def __getitem__(self, args):
        raise NotImplementedError(
            '__getitem__ must be implemented by $s' % self.__class__.__name__
        )

    def __len__(self):
        return len(self._dset)

    @sync
    def mean(self, indices=None):
        acquired = self._dset.entry.acquired
        if indices is None:
            indices = range(acquired)
        elif len(indices):
            indices = [i for i in indices if i < acquired]

        res = np.zeros(self.shape[1:], 'f')
        nitems = 0
        mask = self.measurement.masked
        for i in indices:
            if not mask[i]:
                nitems += 1
                res += self[i]
        if nitems:
            return res / nitems
        return res


class CorrectedDataProxy(DataProxy):

    @sync
    def __getitem__(self, key):
        data = self._dset[key]

        try:
            data /= self._dset.efficiency
        except AttributeError:
            pass

        return data


class DeadTimeProxy(DataProxy):

    @property
    def format(self):
        return self._format

    def __init__(self, dataset, format):
        super(DeadTimeProxy, self).__init__(dataset)

        assert format in (
            'percent', '%', 'fraction', 'normalization', 'correction'
        )
        self._format = format

    @sync
    def __getitem__(self, args):
        in_format = self._dset.format
        out_format = self.format

        data = self._dset.__getitem__(args)
        if in_format == out_format:
            return data

        if in_format == 'fraction':
            fraction = data
        elif in_format in ('percent', '%'):
            fraction = data / 100.0
        elif in_format == 'correction':
            fraction = 1.0 - 1.0 / data
        elif in_format == 'normalization':
            fraction = 1.0 - data
        else:
            raise ValueError(
                'Unrecognized dead time format: %s' % self._dset.format
            )

        if out_format == 'fraction':
            return fraction
        elif out_format in ('percent', '%'):
            return 100 * fraction
        elif out_format == 'correction':
            return 1.0 / (1.0 - fraction)
        elif out_format == 'normalization':
            return 1.0 - fraction
        else:
            raise ValueError(
                'Unrecognized dead time format: %s' % self.format
            )
