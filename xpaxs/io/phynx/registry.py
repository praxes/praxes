"""
"""

from __future__ import absolute_import

import threading
import warnings

from .utils import sync


class _Registry(object):

    @property
    def plock(self):
        return self._plock

    def __init__(self):
        self._plock = threading.Lock()
        self.__data = {}

    @sync
    def __contains__(self, name):
        return name in self.__data

    @sync
    def __getitem__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            warnings.warn("there is no registered class named `%s`, "
                          "defaulting to Group"% name)
            return self.__data['Group']

    @sync
    def __iter__(self):
        return self.__data.__iter__()

    @sync
    def __setitem__(self, name, value):
        self.__data[name] = value

    @sync
    def register(self, value, *alt_keys):
        self.__data[value.__name__] = value
        for k in alt_keys:
            assert isinstance(k, str)
            self.__data[k] = value
        try:
            self.__data[value.nx_class] = value
        except AttributeError:
            pass

registry = _Registry()
