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
from .entry import NXentry
from .group import NXgroup
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def getLocalTime():
    """return a string representation of the local time"""
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(l[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class NXfile(NXgroup, File):

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

        File.__init__(self, name, mode)

    def create_entry(self, name, data=None):
        return NXentry(self, name, data)
