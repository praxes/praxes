"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from h5py.highlevel import Group

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

#from .leaf import NXleaf
#from .node import NXnode
from .registry import get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXgroup(Group):

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
            item = super(NXgroup, self).__getitem__(name)
            nxclass = get_nxclass_from_h5_item(item)
            del item
            return nxclass(self, name)
