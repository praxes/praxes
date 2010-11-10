import __builtin__

from .index import FileIndex
from .scan import SpecScan


def open(file_name):
    return SpecFile(file_name)


class SpecFile(object):

    @property
    def file(self):
        return __builtin__.open(self._name)

    @property
    def name(self):
        return self._name

    def __init__(self, file_name):
        self._name = file_name
        self.__index = FileIndex(file_name)

    def __getitem__(self, item):
        # need to return a SpecScan object
        pass

    def __iter__(self):
        for i in self.__index:
            yield SpecScan(i)
