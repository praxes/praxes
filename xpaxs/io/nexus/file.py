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
from .registry import get_nxclass_from_h5_item

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
                self.__h5Node = self.__h5File.root
                self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
                for id, group in self.__h5Node._v_children.items():
                    nxclass = get_nxclass_from_h5_item(group)
                    setattr(self, id, nxclass(self, id))
            except IOError, err:
                if mode == 'r+':
                    self.__h5file = tables.openFile(file_name, 'w')
                    self.__h5Node = self.__h5File.root
                    self.__attrs = NXattrs(self, self.__h5Node._v_attrs)
                else:
                    raise err
                now = get_local_time
                self.nx_attrs.file_name = file_name
                self.nx_attrs.file_time = now
                self.nx_attrs.file_update_time = now
                self.nx_attrs.creator = sys.argv[0]
                self.nx_attrs.NeXus_version = ''
                setattr(parent, name, self)

#    def __getattr__(self, name):
#        with self.lock:
#            return self.__h5Node._v_children[name]

    def __iter__(self):
        with self.lock:
            return self.__h5File.walkNodes('/')

    def create_h5array(self, where, name):
        with self.lock:
            return self.__h5File.createArray(where, name)

    def create_h5carray(self, where, name):
        with self.lock:
            return self.__h5File.createCArray(where, name)

    def create_h5earray(self, where, name):
        with self.lock:
            return self.__h5File.createEArray(where, name)

    def create_h5group(self, where, name):
        with self.lock:
            return self.__h5File.createGroup(where, name)

    def close(self):
        with self.lock:
            self.__h5File.close()

    def flush(self):
        with self.lock:
            self.__h5File.flush()

# TODO:
#        self.file_update_time = get_local_time()

    def get_h5node(self, where, name):
        with self.lock:
            return self.__h5File.getNode(where, name)

    lock = property(lambda self: self.__lock)

    nx_attrs = property(lambda self: self.__attrs)

    nx_file = property(lambda self: self)

    path = property(lambda self: '/')
