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

from h5py.highlevel import File

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

#from .root import NXroot
#from .array import NXarray
#from .carray import NXcarray
#from .earray import NXearray
from .dataset import NXdataset
from .entry import NXentry
from .sample import NXsample
from .registry import get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def getLocalTime():
    # TODO: format according to nexus
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(l[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class NXfile(File):

    """
    """

    @property
    def __members__(self):
        with self.lock:
            return list(self)

    def __getattr__(self, name):
        with self.lock:
            return self.__getitem__(name)

    def __getitem__(self, name):
        with self.lock:
            # a little hackish, for now:
            item = super(NXfile, self).__getitem__(name)
            nxclass = get_nxclass_from_h5_item(item)
            del item
            return nxclass(self, name)
