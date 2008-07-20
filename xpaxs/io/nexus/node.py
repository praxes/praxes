"""
Wrappers around the pytables interface to the hdf5 file.

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import sys
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.io.nexus.attrs import NXattrs
from xpaxs.io.nexus.registry import get_nxclass_from_h5_item

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXnode(QtCore.QObject):

    """
    """

    def __init__(self, parent, name, *args, **kwargs):
        """
        """
        super(NXnode, self).__init__(parent)

        self.__mutex = parent.mutex

        self.__nxFile = parent.nx_file

        try:
            self.__h5Node = self.nx_file.get_h5node(parent.path, name)
            self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
            for id, group in self.__h5Node._v_children.items():
                nxclass = get_nxclass_from_h5_item(group)
                setattr(self, 'nx_%s'%id, nxclass(self, id))
        except tables.NoSuchNodeError:
            self._create_entry(where, name, *args, **kwargs)
            self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
            self.nx_attrs.NX_class = self.__class__.__name__
            setattr(parent, 'nx_%s'%name, self)

    def __getattr__(self, name):
        try:
            self.mutex.lock()
            return self.__h5Node._v_children[name]
        finally:
            self.mutex.unlock()

    def __iter__(self):
        try:
            self.mutex.lock()
            return self.__h5Node._f_iterNodes()
        finally:
            self.mutex.unlock()

    def _create_entry(self, where, name, *args, **kwargs):
        raise NotImplementedError

    def _initialize_entry(self):
        pass

    def flush(self):
        self.nx_file.flush()

    mutex = property(lambda self: self.__mutex)

    nx_attrs = property(lambda self: self.__attrs)

    nx_file = property(lambda self: self.__nxFile)

    @property
    def path(self):
        try:
            self.mutex.lock()
            return self.__h5Node._v_pathname
        finally:
            self.mutex.unlock()
