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


class NXattrs(QtCore.QObject):

    """
    """

    def __init__(self, parent, attrs, *args, **kwargs):
        """
        """
        super(NXattrs, self).__init__(parent)
        self.__dict__['__mutex'] = parent.mutex
        self.__dict__['__h5Node'] = attrs

    def __getattr__(self, name):
        try:
            self.mutex.lock()
            return getattr(self.__h5Node, name)
        finally:
            self.mutex.unlock()

    def __setattr__(self, name, value):
        try:
            self.mutex.lock()
            return setattr(self.__h5Node, name, value)
        finally:
            self.mutex.unlock()

    def __iter__(self):
        try:
            self.mutex.lock()
            names = self.__h5Node._v_attrnames
            for name in names:
                yield gettattr(self.__h5Node, name)
        finally:
            self.mutex.unlock()

    mutex = property(lambda self: self.__mutex)
