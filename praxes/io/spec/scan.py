import weakref

from .scanindex import ScanIndex


class SpecScan(object):

    @property
    def key(self):
        return self.__key

    @property
    def name(self):
        return self.__name

    def __init__(self, name, key, file, offset):
        self.__name = name
        self.__key = key
        self.__file_name = file.name
        self.__index = ScanIndex(file.name, offset)

