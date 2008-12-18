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



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class _Registry(object):

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
                warnings.warn("there is no registered class named `%s`, "
                              "defaulting to Group"% name)
                return self.__data['Group']

    def __iter__(self):
        with self.__lock:
            return self.__data.__iter__()

    def __setitem__(self, name, value):
        with self.__lock:
            self.__data[name] = value

    def register(self, value):
        with self.__lock:
            self.__data[value.__name__] = value
            try:
                self.__data[value.nx_class] = value
            except AttributeError:
                pass

registry = _Registry()
