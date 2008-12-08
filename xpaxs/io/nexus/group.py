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

import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import NXdataset
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXgroup(object):

    """
    """

    def __init__(self, parent_object, name, data=None):
        """
        If create is None, return an existing group or raise an error

        If create is not None, it must be a python dictionary. hdf5 attributes
        can be identified by::

            data={'attrs': {'foo':1, 'bar':2}}

        """
        with parent_object._lock:
            if name in self._h5:
                self._h5 = h5py.Group(parent_object._h5, name, create=False)
            else:
                self._h5 = h5py.Group(parent_object._h5, name, create=True)

            for attr, val in kwargs.pop(attrs, {}):
                self.attrs[attr] = val

            for key, val in data:
                nxclassName, nxdata = val
                if nxclassName == 'Dataset':
                    NXdataset(self, key, nxdata)
                else:
                    nxclass = registry[]

    def __getitem__(self, name):
        with self._lock:
            item = self._h5[name]
            if isinstance(item, h5py.Dataset):
                nxclass = NXdataset
            else:
                nxclass = registry[item.attrs['NX_class']]
            return nxclass(self, item)
