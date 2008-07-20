"""
Wrappers around the pytables interface to the hdf5 file.

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



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


class NXleaf(QtCore.QObject):

    """
    """

    def __init__(self, parent, name, *args, **kwargs):
        """
        """
        super(NXleaf, self).__init__(parent)

        self.__mutex = parent.mutex

        self.__nxFile = parent.nx_file

        try:
            self.__h5Node = self.nx_file.get_h5node(parent.path, name)
        except tables.NoSuchNodeError:
            self._create_entry(parent.path, name, *args, **kwargs)

        self.__attrs = NXattrs(self, self.__h5Node._v_attrs)

    def __getitem__(self, key):
        try:
            self.mutex.lock()
            return self.__h5Node.__getitem__(key)
        finally:
            self.mutex.unlock()

    def __iter__(self):
        try:
            self.mutex.lock()
            return self.__h5Node.__iter__()
        finally:
            self.mutex.unlock()

    def __len__(self):
        try:
            self.mutex.lock()
            self.__h5Node.__len__()
        except:
            self.mutex.unlock()

    def __setitem__(self, key, value):
        try:
            self.mutex.lock()
            self.__h5Node.__getitem__(key, value)
        finally:
            self.mutex.unlock()

    def _create_entry(self, where, name):
        raise NotImplementedError

    def _initialize_entry(self):
        pass

    attrs = property(lambda self: self.__attrs)

    def flush(self):
        self.nx_file.flush()

    mutex = property(lambda self: self.__mutex)

    nx_file = property(lambda self: self.__nxFile)

    @property
    def path(self):
        try:
            self.mutex.lock()
            return self.__h5Node._v_pathname
        finally:
            self.mutex.unlock()
