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

import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .attrs import NXattrs
from .registry import get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXleaf(object):

    """
    """

    def __init__(self, parent, name, *args, **kwargs):
        """
        """
        super(NXleaf, self).__init__(parent)

        self.__lock = parent.lock

        self.__nxFile = parent.nx_file

        try:
            self.__h5Node = self.nx_file.get_h5node(parent.path, name)
        except tables.NoSuchNodeError:
            self._create_entry(parent.path, name, *args, **kwargs)

        self.__attrs = NXattrs(self, self.__h5Node._v_attrs)

    def __getitem__(self, key):
        with self.lock:
            return self.__h5Node.__getitem__(key)

    def __iter__(self):
        with self.lock:
            return self.__h5Node.__iter__()

    def __len__(self):
        with self.lock:
            self.__h5Node.__len__()

    def __setitem__(self, key, value):
        with self.lock:
            self.__h5Node.__getitem__(key, value)

    def _create_entry(self, where, name):
        raise NotImplementedError

    def _initialize_entry(self):
        pass

    def flush(self):
        with self.lock:
            self.nx_file.flush()

    lock = property(lambda self: self.__lock)

    nx_attrs = property(lambda self: self.__attrs)

    nx_file = property(lambda self: self.__nxFile)

    @property
    def path(self):
        with self.lock:
            return self.__h5Node._v_pathname
