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


class NXnode(object):

    """
    """

    def __init__(self, parent, h5node, *args, **kwargs):

        """
        """

        super(NXnode, self).__init__(parent)

        self.__nxFile = parent._v_file

        with self._v_lock:
            self.__h5Node = h5node
            self.__pathname = self.__h5Node._v_pathname
            self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
            for id, group in self.__h5Node._v_children.items():
                nxclass = get_nxclass_from_h5_item(group)
                setattr(self, id, nxclass(self, group))

    def __iter__(self):
        with self._v_lock:
            return self.__h5Node._f_iterNodes()

    def __repr__(self):
        with self._v_lock:
            return self.__h5Node.__repr__()

    def __str__(self):
        with self._v_lock:
            return self.__h5Node.__str__()

    def _f_flush(self):
        with self._v_lock:
            self.nx_file.flush()

    _v_lock = property(lambda self: self._v_file.lock)

    attrs = property(lambda self: self.__attrs)

    _v_file = property(lambda self: self.__nxFile)

    _v_pathname = property(lambda self: self.__pathname)
