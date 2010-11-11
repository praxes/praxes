import __builtin__

import collections

from .scan import SpecScan


def open(file_name):
    return SpecFile(file_name)


class SpecFile(object):

    __slots__ = ['__weakref__', '_name', '__index', '__bytes_read']

    @property
    def name(self):
        return self._name

    def __init__(self, file_name):
        self._name = file_name
        self.__bytes_read = 0
        self.__index = collections.OrderedDict()

        self.update()

    def __contains__(self, item):
        return item in self.__index

    def __getitem__(self, item):
        return self.__index[item]

    def __iter__(self):
        return iter(self.__index)

    def __len__(self):
        return len(self.__index)

    def items(self):
        return self.__index.viewitems()

    def keys(self):
        return self.__index.viewkeys()

    def update(self):
        with __builtin__.open(self._name, 'r+b') as f:
            if len(self):
                # updating an existing file index, will probably have
                # to mark the last scan index as dirty so the data can
                # be updated
                f.seek(0, 2)
                if f.tell() > self.__bytes_read:
                    # assume new data has been appended to the previous scan
                    # might be able to improve this
                    self.__index.values()[-1].dirty = True

            f.seek(self.__bytes_read)
            file_offset = f.tell()
            for line in f:
                if line[:2] == '#S':
                    scan_name = scan_key = line.split()[1]
                    # need to assure that scan_key is unique:
                    dup = 1
                    while scan_key in self:
                        dup += 1
                        scan_key = '%s.%d' % (scan_name, dup)
                    scan = SpecScan(
                        scan_name,
                        scan_key,
                        self,
                        file_offset
                        )
                    self.__index[scan_key] = scan
                file_offset += len(line)

            self.__bytes_read = file_offset

    def values(self):
        return self.__index.viewvalues()
