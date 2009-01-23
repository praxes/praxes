"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import operator
import os
import sys
import threading
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .group import Group

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def getLocalTime():
    """return a string representation of the local time"""
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(res[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class File(Group, h5py.File):

#    def __init__(self, name, mode='a', lock=None):
    def __init__(self, name, mode='a'):
        """
        Create a new file object.

        Valid modes (like Python's file() modes) are:
        - r   Readonly, file must exist
        - r+  Read/write, file must exist
        - w   Create file, truncate if exists
        - w-  Create file, fail if exists
        - a   Read/write if exists, create otherwise (default)

        """
#        if lock is None:
#            import threading
#            self._lock = threading.RLock()
#        else:
#            assert hasattr(lock, '__enter__')
#            assert hasattr(lock, '__exit__')
#            self._lock = lock

        h5py.File.__init__(self, name, mode)

        if self.mode != 'r':
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
            if 'format_version' not in self.attrs:
                self.attrs['format_version'] = '0.1'

    @property
    def format(self):
        # TODO: use h5py get() when available
        try:
            return self.attrs['format']
        except h5py.H5Error:
            raise RuntimeError('unrecognized format')

    def list_sorted_entries(self):
        return sorted(
            self.listobjects(), key=operator.attrgetter('acquisition_id')
        )
