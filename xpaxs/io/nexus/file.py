"""
Wrappers around the pytables interface to the hdf5 file.

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

from h5py import Dataset, File

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import NXdataset
from .registry import registry
from .group import NXgroup

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def getLocalTime():
    """return a string representation of the local time"""
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(l[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class DummyLock(object):
    def __enter__(self):
        return 0

    def __exit__(self, a, b, c):
        return 0

    def acquire(self, blocking=1):
        return 1

    def release(self):
        return 0


class NXfile(NXGroup):

    def __init__(self, name, mode, lock=None):
        """
        Create a new file object.

        Valid modes (like Python's file() modes) are:
        - r   Readonly, file must exist
        - r+  Read/write, file must exist
        - w   Create file, truncate if exists
        - w-  Create file, fail if exists
        - a   Read/write if exists, create otherwise (default)

        lock is a recursive thread lock conformant to python's context manager
        """
        if lock is None:
            self._lock = DummyLock()
        else:
            assert hasattr(lock, __enter__)
            assert hasattr(lock, __exit__)
            self._lock = lock

        self._h5 = h5py.File(name, mode)
        super(NXfile, self).__init__(self, '/')

    def __getitem__(self, name):
        with self._lock:
            # a little hackish, for now:
            item = super(File, self).__getitem__(name)
            if isinstance(item, Dataset):
                nxclass = NXdataset
            else:
                nxclass = registry[item.attrs['NX_class']]

            return nxclass(self, item)
