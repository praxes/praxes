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
from .node import NXnode
from .registry import get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXroot(NXnode):

    """
    """

#    def __init__(self, parent, h5node, *args, **kwargs):
#        """
#        """
#        self.__file = parent
#
#        with self._v_file.lock:
#            self.__h5Node = h5node
#            self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
#            for id, group in self.__h5Node._v_children.items():
#                nxclass = get_nxclass_from_h5_item(group)
#                setattr(self, id, nxclass(self, id))

#    attrs = property(lambda self: self.__attrs)
#
#    _v_file = property(lambda self: self.__nxFile)
#
#    _v_pathname = property(lambda self: '/')
