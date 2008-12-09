"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import threading
import warnings

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py.highlevel as h5py
from h5py import h5

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXregistry(object):

    def __init__(self):
        self.__lock = threading.Lock()
        self.__data = {}

    def __contains__(self, name):
        with self.__lock:
            return name in self.__data

    def __getitem__(self, name):
        with self.__lock:
            try:
                return self.__data[name]
            except KeyError:
                warnings.warn("there is no registered NeXus class named `%s`, "
                              "defaulting to NXgroup"% name)
                return self.__data['NXgroup']

            return class_name_dict[name]

    def __iter__(self):
        with self.__lock:
            return self.__data.__iter__()

    def __setitem__(self, name, value):
        with self.__lock:
            self.__data[name] = value

registry = NXregistry()
