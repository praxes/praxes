"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

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

    def __init__(self, name, mode='a', lock=None):
        """
        Create a new file object.

        Valid modes (like Python's file() modes) are:
        - r   Readonly, file must exist
        - r+  Read/write, file must exist
        - w   Create file, truncate if exists
        - w-  Create file, fail if exists
        - a   Read/write if exists, create otherwise (default)

        lock is a recursive thread lock conformant to python's context manager.
        If lock is None, an threading.RLock is used from the standard library.
        """
        if lock is None:
            import threading
            self._lock = threading.RLock()
        else:
            assert hasattr(lock, __enter__)
            assert hasattr(lock, __exit__)
            self._lock = lock

        h5py.File.__init__(self, name, mode)

        with self._lock:
            if self.mode != 'r':
                if not 'file_name' in self.attrs:
                    self.attrs['file_name'] = name
                if not 'file_time' in self.attrs:
                    self.attrs['file_time'] = getLocalTime()
                if not 'HDF5_version' in self.attrs:
                    self.attrs['HDF5_version'] = h5py.version.hdf5_version
                if not 'HDF5_API_version' in self.attrs:
                    self.attrs['HDF5_API_version'] = h5py.version.api_version
                if not 'HDF5_version' in self.attrs:
                    self.attrs['h5py_version'] = h5py.version.version
#                if not 'creator' in self.attrs:
#                    self.attrs['creator'] = 'XPaXS'
