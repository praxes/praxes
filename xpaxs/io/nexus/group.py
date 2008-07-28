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

from h5py import Dataset, Group

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import NXdataset
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXgroup(Group):

    """
    """

    def __getitem__(self, name):
        with self.lock:
            # a little hackish, for now:
            item = super(NXgroup, self).__getitem__(name)
            if isinstance(item, Dataset):
                nxclass = NXdataset
            else:
                nxclass = registry[item.attrs['NX_class']]
            del item
            return nxclass(self, name)
