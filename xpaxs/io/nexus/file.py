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


class NXFile(QtCore.QObject):

    def __init__(self, filename, mode='r+', parent=None):
        super(NXFile, self).__init__(parent)

        self.__mutex = QtCore.QMutex()

        try:
            self.__h5file = tables.openFile(filename, mode)
        except IOError, err:
            if mode == 'r+': self.__h5file = tables.openFile(filename, 'w')
            else: raise err
            self.__initialize_file()

    def __getattr__(self, name):
        try:
            self.mutex.lock()
            return getattr(self.h5File._v_attrs, name)
        finally:
            self.mutex.unlock()

    def __setattr__(self, name, value):
        try:
            self.mutex.lock()
            return setattr(self.h5File._v_attrs, name, value)
        finally:
            self.mutex.unlock()

    def __initialize_file(self):
        now = get_local_time
        self.h5File._v_attrs.file_time = now
        self.h5File._v_attrs.file_update_time = now
        self.h5File._v_attrs.creator = sys.argv[0]
        self.h5File._v_attrs.NeXus_version = ''

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

    @property
    def creator(self):
        try:
            self.mutex.lock()
            return self.h5File._v_attrs.creator
        except AttributeError:
            return ''
        finally:
            self.mutex.unlock()

    @property
    def file_name(self):
        try:
            self.mutex.lock()
            return self.h5File._v_attrs.file_name
        except AttributeError:
            return ''
        finally:
            self.mutex.unlock()

    @property
    def file_time(self):
        try:
            self.mutex.lock()
            return self.h5File._v_attrs.file_time
        except AttributeError:
            return ''
        finally:
            self.mutex.unlock()

    def flush(self):
        try:
            self.mutex.lock()
            self.h5File.flush()
        finally:
            self.mutex.unlock()

    def get_file_update_time(self):
        try:
            self.mutex.lock()
            return self.h5File._v_attrs.file_update_time
        except AttributeError:
            return ''
        finally:
            self.mutex.unlock()
    def set_file_update_time(self):
        try:
            self.mutex.lock()
            self.h5File._v_attrs.file_update_time = get_local_time()
        finally:
            self.mutex.unlock()
    file_update_time = property(get_file_update_time,
                                set_file_update_time)

    @property
    def HDF5_version(self):
        try:
            self.mutex.lock()
            return self.h5File._v_attrs.HDF5_version
        except AttributeError:
            return ''
        finally:
            self.mutex.unlock()

    h5File = property(lambda self: self.__h5file)

    mutex = property(lambda self: self.__mutex)

    @property
    def NeXus_version(self):
        try:
            self.mutex.lock()
            return self.h5File._v_attrs.NeXus_version
        except AttributeError:
            return ''
        finally:
            self.mutex.unlock()
