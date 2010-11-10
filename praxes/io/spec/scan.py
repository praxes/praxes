class SpecScan(object):

    @property
    def file(self):
        return self._file

    @property
    def id(self):
        return self.__index.id

    @property
    def name(self):
        return self.__index.name

    def __init__(self, file, index):
        self._file = file
        self.__index = index

