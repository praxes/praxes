import collections
import os
import re

from .readonlydict import ReadOnlyDict
from .scan import SpecScan


class SpecFile(ReadOnlyDict):

    "An OrderedDict-like interface to scans contained in spec data files."

    __slots__ = ['__bytes_read', '__headers', '_index', '_name']

    @property
    def name(self):
        return self._name

    def __init__(self, file_name):
        self._name = file_name
        self.__bytes_read = 0
        self._index = collections.OrderedDict()
        self.__headers = {}

        self.update()

    def update(self):
        "Update the file index based on any data appended to the file."
        if os.stat(self._name).st_size == self.__bytes_read:
            return

        index = self._index
        with open(self._name, 'rb') as f:
            if len(self):
                # updating an existing file index, may need to update last scan
                index.values()[-1].update()

            f.seek(self.__bytes_read)
            file_offset = f.tell()
            line = f.readline()
            while line:
                if line[:2] == '#S':
                    name = id = line.split()[1]
                    # need to assure that id is unique:
                    dup = 1
                    while id in index:
                        dup += 1
                        id = '%s.%d' % (name, dup)
                    scan = SpecScan(
                        name, id, self, file_offset, **self.__headers
                        )
                    index[id] = scan
                    f.seek(scan.file_offsets[1])
                elif line[:2] == '#F':
                    self.__headers['file_origin'] = line.split()[1]
                elif line[:2] == '#E':
                    self.__headers['epoch_offset'] = int(line.split()[1])
                elif line[:2] == '#D':
                    self.__headers['date'] = line.split(None, 1)[1][:-1]
                elif line[:2] == '#C' and line.split()[2] == 'User':
                    temp = line.split()
                    program, user = temp[1], temp[-1]
                    self.__headers['program'] = program
                    self.__headers['user'] = user
                elif line[:2] == '#O':
                    if line[2] == '0':
                        self.__headers['positioners'] = []
                    self.__headers['positioners'].extend(
                        re.split('  +', line.split(None, 1)[1][:-1])
                        )

                file_offset = f.tell()
                line = f.readline()

            self.__bytes_read = f.tell()
