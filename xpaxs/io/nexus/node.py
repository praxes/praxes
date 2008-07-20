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

        self.__nxFile = parent.nxFile

        try:
            self.__h5Node = parent[name]
            self.__attrs = NXattrs(self)
            for id, group in self.__h5Node._v_children.items():
                nxclass = get_nxclass_from_h5_item(group)
                nxclass(self, id)
        except NoSuchNodeError:
            self._create_entry(where, name, *args, **kwargs)
            self.__attrs = NXattrs(self)
            self.attrs.NX_class = self.__class__.__name__

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

    attrs = property(lambda self: self.__attrs)

    def flush(self):
        self.nxFile.flush()

    mutex = property(lambda self: self.__mutex)

    nxFile = property(lambda self: self.__nxFile)

    @property
    def path(self):
        try:
            self.mutex.lock()
            return self.__h5Node._v_pathname
        finally:
            self.mutex.unlock()
