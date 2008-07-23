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

from .leaf import NXleaf
from .node import NXnode
from .registry import class_name_dict, get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXentry(NXnode):

    """
    """

    def __init__(self, parent, name, *args, **kwargs):
        super(NXentry, self).__init__(parent, name, *args, **kwargs)

        with self._v_lock:
            for id, node in self._v_h5Node._v_children.items():
                nxclass = get_nxclass_from_h5_item(node)
                self.__dict__[id] = nxclass(self, id, h5Node=node)

    def _createH5Node(self):
        return
        with self._v_lock:
            # how do I do this? I need access to the tables file.
            print self.__class__.__name__

    def __repr__(self):
        with self._v_lock:
            rep = ['%r (%s)' %
                   (i, self._v_h5Node._v_attrs._g_getAttr(i).__class__.__name__)
                   for i in self._v_attrs]
            attrlist = '[%s]' % (', '.join(rep))
            rep = ['%r (%s)' % (i, val.__class__.__name__)
                   for i, val in self.__dict__.items()
                   if isinstance(val, NXentry)]
            childlist = '[%s]' % (', '.join(rep))
            rep = ['%r (%s)' % (i, val.__class__.__name__)
                   for i, val in self.__dict__.items()
                   if isinstance(val, NXleaf)]
            datalist = '[%s]' % (', '.join(rep))
            return "%s\n  attributes: %s\n  children: %s\n  data: %s" % \
                   (str(self), attrlist, childlist, datalist)

class_name_dict['NXentry'] = NXentry
