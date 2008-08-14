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

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def getLocalTime():
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(l[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class NXfile(File):

    """
    """

    def __getitem__(self, name):
        with self._lock:
            # a little hackish, for now:
            item = super(NXfile, self).__getitem__(name)
            if isinstance(item, Dataset):
                nxclass = NXdataset
            else:
                nxclass = registry[item.attrs['NX_class']]
            del item
            return nxclass(self, name)
