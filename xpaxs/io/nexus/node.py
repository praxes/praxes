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



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXNode(QtCore):

    """
    """

    def __init__(self, parent, name, *args, **kwargs):
        """
        """
        super(NXNode, self).__init__(parent)

        self.__mutex = xpaxsFile.mutex

        try:
            self.__h5Node = parent[name]
        except NoSuchNodeError:
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
        # create a __h5Node

    def flush(self):
        self.parent().flush()

    h5Node = property(lambda self: self.__h5Node)

    mutex = property(lambda self: self.__mutex)
