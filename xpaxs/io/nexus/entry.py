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



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .node import NXnode
from .registry import class_name_dict, get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXentry(NXnode):

    """
    """

    def __init__(self, parent, h5node, *args, **kwargs):
        super(NXentry, self).__init__(parent, h5node)
        with self._v_lock:
            for id, group in h5node._v_children.items():
                nxclass = get_nxclass_from_h5_item(group)
                self.__dict__[id] = nxclass(self, group)

class_name_dict['NXentry'] = NXentry
