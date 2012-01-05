"""
"""

from distutils import version
import operator
import os
import sys
import threading
import time

import h5py

from .group import Group
from .utils import sync
from .version import __format_version__
from ...rlock import FastRLock


global_lock = FastRLock()


def getLocalTime():
    """return a string representation of the local time"""
    res = list(time.localtime())[:6]
    g = time.gmtime()
    res.append(res[3]-g[3])
    return '%d-%02d-%02dT%02d:%02d:%02d%+02d:00'%tuple(res)


def open(file_name, mode='a', **kwargs):
    # h5py issue 230: file-specific locks lead to segfaults:
    #lock = kwargs.pop('lock', None)
    #if lock is None:
    #    lock = DummyLock()
    # need to synchronize all h5py interaction with a single lock:
    lock = global_lock
    f = File(h5py.File(file_name, mode=mode, **kwargs), lock)
    if f.mode != 'r' and len(f) == 0:
        if 'file_name' not in f.attrs:
            f.attrs['file_name'] = file_name
        if 'file_time' not in f.attrs:
            f.attrs['file_time'] = getLocalTime()
        if 'HDF5_version' not in f.attrs:
            f.attrs['HDF5_version'] = h5py.version.hdf5_version
        if 'HDF5_API_version' not in f.attrs:
            f.attrs['HDF5_API_version'] = h5py.version.api_version
        if 'HDF5_version' not in f.attrs:
            f.attrs['h5py_version'] = h5py.version.version
        if 'creator' not in f.attrs:
            f.attrs['creator'] = 'phynx'
        if 'format_version' not in f.attrs and len(f) == 0:
            f.attrs['format_version'] = __format_version__

    return f


class File(Group):

    @property
    def creator(self):
        try:
            return self.attrs['creator']
        except KeyError:
            raise RuntimeError('unrecognized format')

    @property
    def file(self):
        return self

    @property
    def file_name(self):
        return self._h5node.filename

    @property
    def format(self):
        return self.attrs.get('format_version', None)

    @property
    def mode(self):
        return self._h5node.mode

    @property
    def name(self):
        return '/'

    def close(self):
        self._h5node.close()

    def flush(self):
        self._h5node.flush()
