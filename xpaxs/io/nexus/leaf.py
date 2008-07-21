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

    def __init__(self, parent, h5node, *args, **kwargs):
        """
        """
        super(NXleaf, self).__init__(parent)

#        self.__lock = parent.lock

        self.__nxFile = parent._v_file

        self.__h5Node = h5node

        self.__pathname = self.__h5Node._v_pathname

        self.__attrs = NXattrs(self, self.__h5Node._v_attrs)

    def __getitem__(self, key):
        with self._v_lock:
            return self.__h5Node.__getitem__(key)

    def __iter__(self):
        with self._v_lock:
            return self.__h5Node.__iter__()

    def __len__(self):
        with self._v_lock:
            self.__h5Node.__len__()

    def __repr__(self):
        with self._v_lock:
            return self.__h5Node.__repr__()

    def __setitem__(self, key, value):
        with self._v_lock:
            self.__h5Node.__setitem__(key, value)

    def __str__(self):
        with self._v_lock:
            return self.__h5Node.__str__()

    def _v_flush(self):
        with self._v_lock:
            self.nx_file.flush()

    _v_lock = property(lambda self: self._v_file.lock)

    attrs = property(lambda self: self.__attrs)

    _v_file = property(lambda self: self.__nxFile)

    _v_pathname = property(lambda self: self.__pathname)
