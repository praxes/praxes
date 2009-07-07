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
        return self.__data[name]

    @sync
    def __iter__(self):
        return self.__data.__iter__()

    @sync
    def __setitem__(self, name, value):
        self.__data[name] = value

    @sync
    def register(self, value):
        self.__data[value.__name__] = value
        try:
            if value.nx_class not in self.__data:
                self.__data[value.nx_class] = value
        except AttributeError:
            pass

registry = _Registry()
