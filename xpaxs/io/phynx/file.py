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

from .exceptions import H5Error
from .group import Group
from .utils import sync
from .version import __format_version__


def getLocalTime():
    """return a string representation of the local time"""
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(res[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class File(Group, h5py.File):

    @property
    def creator(self):
        try:
            return self.attrs['creator']
        except H5Error:
            raise RuntimeError('unrecognized format')

    @property
    def file(self):
        return self

    @property
    def format(self):
        return self.attrs.get('format_version', None)

    @property
    def parent(self):
        return None

    @property
    def path(self):
        return '/'

    def __init__(self, name, mode='a', lock=None):
        """
        Create a new file object.

        Valid modes (like Python's file() modes) are:
        - r   Readonly, file must exist
        - r+  Read/write, file must exist
        - w   Create file, truncate if exists
        - w-  Create file, fail if exists
        - a   Read/write if exists, create otherwise (default)

        parent is used for used for GUI interfaces
        """

        h5py.File.__init__(self, name, mode)
        if lock is None:
            lock = threading.RLock()
        else:
            try:
                with lock:
                    pass
            except AttributeError:
                raise RuntimeError(
                    'lock must be a context manager, providing __enter__ and '
                    '__exit__ methods'
                )
        self._plock = lock

        if self.mode != 'r' and len(self) == 0:
            if 'file_name' not in self.attrs:
                self.attrs['file_name'] = name
            if 'file_time' not in self.attrs:
                self.attrs['file_time'] = getLocalTime()
            if 'HDF5_version' not in self.attrs:
                self.attrs['HDF5_version'] = h5py.version.hdf5_version
            if 'HDF5_API_version' not in self.attrs:
                self.attrs['HDF5_API_version'] = h5py.version.api_version
            if 'HDF5_version' not in self.attrs:
                self.attrs['h5py_version'] = h5py.version.version
            if 'creator' not in self.attrs:
                self.attrs['creator'] = 'phynx'
            if 'format_version' not in self.attrs and len(self) == 0:
                self.attrs['format_version'] = __format_version__

    @sync
    def create_entry(self, name, **data):
        """A convenience function to build the most basic hierarchy"""
        entry = self.create_group(name, type='Entry', **data)
        measurement = entry.create_group('measurement', type='Measurement')
        scalar_data = measurement.create_group('scalar_data', type='ScalarData')
        pos = measurement.create_group('positioners', type='Positioners')
        return entry

    @sync
    def require_entry(self, name, **data):
        """A convenience function to access or build the most basic hierarchy"""
        entry = self.require_group(name, type='Entry', **data)
        measurement = entry.require_group('measurement', type='Measurement')
        scalars = measurement.require_group('scalar_data', type='ScalarData')
        pos = measurement.require_group('positioners', type='Positioners')
        return entry

    @sync
    def list_sorted_entries(self):
        return sorted(
            self.listobjects(), key=operator.attrgetter('acquisition_id')
        )
