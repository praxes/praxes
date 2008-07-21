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

    def __init__(self, parent, name, *args, **kwargs):
        """
        """
        super(NXnode, self).__init__(parent)

        self.__lock = parent.lock

        self.__nxFile = parent.nx_file

        with self.lock:
            try:
                self.__h5Node = self.nx_file.get_h5node(parent.path, name)
                self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
                for id, group in self.__h5Node._v_children.items():
                    nxclass = get_nxclass_from_h5_item(group)
                    setattr(self, id, nxclass(self, id))
            except tables.NoSuchNodeError:
                self._create_entry(where, name, *args, **kwargs)
                self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
                self.nx_attrs.NX_class = self.__class__.__name__
                setattr(parent, name, self)

#    def __getattr__(self, name):
#        with self.lock:
#            return self.__h5Node._v_children[name]

    def __iter__(self):
        with self.lock:
            return self.__h5Node._f_iterNodes()

    def _create_entry(self, where, name, *args, **kwargs):
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
