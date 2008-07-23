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

from .node import NXnode
from .registry import get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXleaf(NXnode):

    """
    """

    def __getitem__(self, key):
        with self._v_lock:
            return self._v_h5Node.__getitem__(key)

    def __iter__(self):
        with self._v_lock:
            return self._v_h5Node.__iter__()

    def __len__(self):
        with self._v_lock:
            self._v_h5Node.__len__()

    def __repr__(self):
        with self._v_lock:
            rep = ['%r (%s)' %
                   (i, self._v_h5Node._v_attrs._g_getAttr(i).__class__.__name__)
                   for i in self._v_attrs]
            attrlist = '[%s]' % (', '.join(rep))
            return "%s\n  attributes: %s" % (str(self), attrlist)

    def __setitem__(self, key, value):
        with self._v_lock:
            self._v_h5Node.__setitem__(key, value)
