"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import sys
import threading
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .attrs import NXattrs
from .root import NXroot
from .array import NXarray
from .carray import NXcarray
from .earray import NXearray
from .entry import NXentry
from .sample import NXsample

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def get_local_time():
    # TODO: format according to nexus
    return time.localtime()


class NXfile(object):

    """
    """

    _readonly = ()

    def __init__(self, file_name, mode='r+', parent=None):
        super(NXfile, self).__init__(parent)

        self.__lock = threading.RLock()

        with self.lock:
            try:
                self.__h5File = tables.openFile(file_name, mode)
                self.__root = NXroot(self, self.__h5File.root)
            except IOError, err:
                if mode == 'r+':
                    temp = tables.openFile(file_name, 'w')
                    temp.close()

                    self.__h5File = tables.openFile(file_name, mode)
                    self.__root = NXroot(self)

                else:
                    raise err
                now = get_local_time
                self.root.attrs.file_time = now
                self.root.attrs.file_update_time = now
                self.root.attrs.file_name = file_name
                self.root.attrs.creator = sys.argv[0]
                self.root.attrs.NeXus_version = ''

    def __iter__(self):
        with self.lock:
            return self.__h5File.walkNodes('/')

    def __repr__(self):
        with self._v_lock:
            return self.__h5Node.__repr__()

    def __str__(self):
        with self._v_lock:
            return self.__h5Node.__str__()

    def create_NXarray(self, parent, name):
        with self.lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, where)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createArray(parent._v_pathname, name)
            setattr(parent, name, NXarray(parent, h5node))

    def create_NXcarray(self, parent, name):
        with self.lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, where)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createCArray(parent._v_pathname, name)
            setattr(parent, name, NXcarray(parent, h5node))

    def create_NXearray(self, parent, name):
        with self.lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, where)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createEArray(parent._v_pathname, name)
            setattr(parent, name, NXearray(parent, h5node))

    def create_NXentry(self, parent, name):
        with self.lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, where)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createGroup(parent._v_pathname, name)
            setattr(parent, name, NXentry(parent, h5node))

    def create_NXsample(self, parent, name):
        with self.lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, where)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createGroup(parent._v_pathname, name)
            setattr(parent, name, NXsample(parent, h5node))

    def close(self):
        with self.lock:
            self.__h5File.close()

    def flush(self):
        with self.lock:
            self.__h5File.flush()

# TODO:
#        self.file_update_time = get_local_time()

#    def get_h5node(self, where, name=None):
#        with self.lock:
#            return self.__h5File.getNode(where, name)

    lock = property(lambda self: self.__lock)

    root = property(lambda self: self.__root)

    _v_file = property(lambda self: self)
