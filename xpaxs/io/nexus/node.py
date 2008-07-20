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

from xpaxs.io.nexus.file import NXfile

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXnode(QtCore):

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
        except NoSuchNodeError:
            try:
                self.mutex.lock()
                self.__h5Node = tables.Group(parent.h5node, name)
                self.h5Node._v_attrs.NX_class = self.__class__.__name__
            finally:
                self.mutex.unlock()
            self._initialize_entry()

    def __getattr__(self, name):
        try:
            self.mutex.lock()
            return getattr(self.h5Node._v_attrs, name)
        finally:
            self.mutex.unlock()

    def __setattr__(self, name, value):
        try:
            self.mutex.lock()
            return setattr(self.h5Node._v_attrs, name, value)
        finally:
            self.mutex.unlock()

    def __iter__(self):
        try:
            self.mutex.lock()
            return self.h5Node._f_iterNodes()
        finally:
            self.mutex.unlock()

    def _initialize_entry(self):
        pass

    def flush(self):
        self.nxFile.flush()

    h5Node = property(lambda self: self.__h5Node)

    mutex = property(lambda self: self.__mutex)

    nxFile = property(lambda self: self.__nxFile)

    @property
    def path(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_pathname
        finally:
            self.mutex.unlock()
