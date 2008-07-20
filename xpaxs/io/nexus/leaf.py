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

        self.__nxFile = parent.nxFile

        try:
            self.__h5Node = parent[name]
        except NoSuchNodeError:
            self._create_entry(parent.path, name, *args, **kwargs)

        self.__attrs = NXattrs(self)

    def __len__(self):
        try:
            self.mutex.lock()
            self.__h5Node.__len__()
        except:
            self.mutex.unlock()

    def _create_entry(self, where, name):
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
