"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
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

from .root import NXroot
from .array import NXarray
from .carray import NXcarray
from .earray import NXearray
from .entry import NXentry
from .sample import NXsample

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def getLocalTime():
    # TODO: format according to nexus
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(l[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


class NXfile(object):

    """
    """

    _readonly = ()

    def __init__(self, file_name, mode='r+', **kwargs):
        super(NXfile, self).__init__(kwargs.get('parent'))

        self.__lock = threading.RLock()

        with self._v_lock:
            try:
                self.__h5File = tables.openFile(file_name, mode, **kwargs)
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
                self.root.file_time = now
                self.root.file_update_time = now
                self.root.file_name = file_name
                self.root.creator = sys.argv[0]
                self.root.NeXus_version = ''
                self.root.HDF5_Version = tables.hdf5Version

    def __str__(self):
        with self._v_lock:
            if not self.__h5File.isopen:
                return "<closed File>"

            date = time.asctime(time.localtime(os.stat(self.__h5File.filename)[8]))
            astring =  self.__h5File.filename + '\n'
            astring += 'Last modif.: ' + repr(date) + '\n'
            return astring

    def __repr__(self):
        with self._v_lock:
            if not self.__h5File.isopen:
                return "<closed File>"

            astring = 'NXfile(filename=' + repr(self.__h5File.filename) + \
                      ', title=' + repr(self.__h5File.title) + \
                      ', mode=' + repr(self.__h5File.mode) + \
                      ', trMap=' + repr(self.__h5File.trMap) + \
                      ', rootUEP=' + repr(self.__h5File.rootUEP) + \
                      ', filters=' + repr(self.__h5File.filters) + \
                      ')\n'
            return astring

    def createNXarray(self, parent, name):
        with self._v_lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, name)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createArray(parent._v_pathname, name)
            setattr(parent, name, NXarray(parent, h5node))

    def createNXcarray(self, parent, name):
        with self._v_lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, name)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createCArray(parent._v_pathname, name)
            setattr(parent, name, NXcarray(parent, h5node))

    def createNXearray(self, parent, name):
        with self._v_lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, name)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createEArray(parent._v_pathname, name)
            setattr(parent, name, NXearray(parent, h5node))

    def createNXentry(self, parent, name):
        with self._v_lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, name)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createGroup(parent._v_pathname, name)
            setattr(parent, name, NXentry(parent, h5node))

    def createNXsample(self, parent, name):
        with self._v_lock:
            try:
                h5node = self.__h5File.getNode(parent._v_pathname, name)
            except tables.NoSuchNodeError:
                h5node = self.__h5File.createGroup(parent._v_pathname, name)
            setattr(parent, name, NXsample(parent, h5node))

    def close(self):
        with self._v_lock:
            self.__h5File.close()

    def flush(self):
        with self._v_lock:
            self.__h5File.flush()
            self.root.file_update_time = getLocalTime()

    _v_lock = property(lambda self: self.__lock)

    root = property(lambda self: self.__root)

    _v_file = property(lambda self: self)
