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


def get_local_time():
    # TODO: format according to nexus
    return time.localtime()


class NXfile(QtCore.QObject):

    """
    """

    _readonly = ()

    def __init__(self, file_name, mode='r+', parent=None):
        super(NXFile, self).__init__(parent)

        self.__mutex = QtCore.QMutex()

        try:
            self.mutex.lock()
            self.__h5file = tables.openFile(file_name, mode)
        except IOError, err:
            if mode == 'r+': self.__h5file = tables.openFile(file_name, 'w')
            else: raise err

            now = get_local_time
            self.h5File._v_attrs.file_name = file_name
            self.h5File._v_attrs.file_time = now
            self.h5File._v_attrs.file_update_time = now
            self.h5File._v_attrs.creator = sys.argv[0]
            self.h5File._v_attrs.NeXus_version = ''
        finally:
            self.mutex.unlock()

    def __getattr__(self, name):
        try:
            self.mutex.lock()
            return getattr(self.h5File._v_attrs, name)
        finally:
            self.mutex.unlock()

    def __setattr__(self, name, value):
        try:
            self.mutex.lock()
            if name in self._readonly:
                raise AttributeError("can't set attribute")
            return setattr(self.h5File._v_attrs, name, value)
        finally:
            self.mutex.unlock()

    def __iter__(self):
        try:
            self.mutex.lock()
            return self.h5File.walkNodes('/')
        finally:
            self.mutex.unlock()

    def close(self):
        try:
            self.mutex.lock()
            self.h5File.close()
        finally:
            self.mutex.unlock()

    def flush(self):
        try:
            self.mutex.lock()
            self.h5File.flush()
        finally:
            self.mutex.unlock()

        self.file_update_time = get_local_time()

    h5File = property(lambda self: self.__h5file)

    mutex = property(lambda self: self.__mutex)

    nxFile = property(lambda self: self)

    nxNode = property(lambda self: self.h5File.root)

    path = property(lambda self: '/')
