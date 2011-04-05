"""
"""

from __future__ import absolute_import, with_statement

from distutils import version
import operator
import os
import sys
import threading
import time

import h5py

from .group import Group
from .utils import sync
from .version import __format_version__


def getLocalTime():
    """return a string representation of the local time"""
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(res[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class DummyLock(object):
    def acquire(self):
        pass
    def release(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass


def open(file_name, mode='a', **kwargs):
    lock = kwargs.pop('lock', None)
    if lock is None:
        lock = DummyLock()
    f = File(h5py.File(file_name, mode=mode, **kwargs), lock)
    if f.mode != 'r' and len(f) == 0:
        if 'file_name' not in f.attrs:
            f.attrs['file_name'] = file_name
        if 'file_time' not in f.attrs:
            f.attrs['file_time'] = getLocalTime()
        if 'HDF5_version' not in f.attrs:
            f.attrs['HDF5_version'] = h5py.version.hdf5_version
        if 'HDF5_API_version' not in f.attrs:
            f.attrs['HDF5_API_version'] = h5py.version.api_version
        if 'HDF5_version' not in f.attrs:
            f.attrs['h5py_version'] = h5py.version.version
        if 'creator' not in f.attrs:
            f.attrs['creator'] = 'phynx'
        if 'format_version' not in f.attrs and len(f) == 0:
            f.attrs['format_version'] = __format_version__

    return f


class File(Group):

    @property
    def creator(self):
        try:
            return self.attrs['creator']
        except KeyError:
            raise RuntimeError('unrecognized format')

    @property
    def file(self):
        return self

    @property
    def file_name(self):
        return self._h5node.filename

    @property
    def format(self):
        return self.attrs.get('format_version', None)

    @property
    def mode(self):
        return self._h5node.mode

#    @sync
#    def create_entry(self, name, **data):
#        """A convenience function to build the most basic hierarchy"""
#        entry = self.create_group(name, type='Entry', **data)
#        measurement = entry.create_group('measurement', type='Measurement')
#        scalar_data = measurement.create_group('scalar_data', type='ScalarData')
#        pos = measurement.create_group('positioners', type='Positioners')
#        return entry
#
#    @sync
#    def require_entry(self, name, **data):
#        """A convenience function to access/build the most basic hierarchy"""
#        entry = self.require_group(name, type='Entry', **data)
#        measurement = entry.require_group('measurement', type='Measurement')
#        scalars = measurement.require_group('scalar_data', type='ScalarData')
#        pos = measurement.require_group('positioners', type='Positioners')
#        return entry
#
#    def sorted_with(self, value):
#        """
#        Set the default sorting behavior for nodes with methods returning
#        lists. Accepts a callable or None. If a callable, the callable should
#        accept and reorganize a list of phynx nodes.
#        """
#        try:
#            assert value is None or callable(value)
#            self._sorted = value
#        except AssertionError:
#            raise AsserionError('value must be a callable or None')

    def keys(self):
        return [n.name for n in self.values()]

    def values(self):
        return sorted(self[key] for key in self._h5node.keys())

    def items(self):
        return [(n.name, n) for n in self.values()]
