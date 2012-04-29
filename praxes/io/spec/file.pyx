from collections import OrderedDict
from copy import deepcopy
import io
import os
import re

from praxes.io.spec.mapping cimport Mapping
from praxes.io.spec.scan import create_scan


def create_file(file_name):
    return FileIndex(file_name)


cdef class FileIndex(Mapping):

    "An OrderedDict-like interface to scans contained in spec data files."

    cdef readonly object _file, name
    cdef unsigned long long _bytes_read
    cdef object _headers

    def __init__(self, file_name):
        super(FileIndex, self).__init__(OrderedDict())

        self._file = io.open(file_name, 'rb', buffering=1024*1024*2)
        self.name = file_name
        self._bytes_read = 0
        self._headers = {}

        self.update()

    def update(self):
        "Update the file index based on any data appended to the file."
        if os.stat(self.name).st_size == self._bytes_read:
            return

        f = self._file
        if len(self):
            # updating an existing file index,
            # may need to update last scan
            list(self._index.values())[-1].update()

        f.seek(self._bytes_read)
        line = f.readline()
        while line:
            if line[:2] == b'#S':
                name = id = line.split()[1].decode('ascii')
                # need to assure that id is unique:
                dup = 1
                while id in self._index:
                    dup += 1
                    id = '%s.%d' % (name, dup)
                scan = create_scan(
                    f, name, id, self, f.tell()-len(line),
                    **deepcopy(self._headers)
                    )
                self._index[id] = scan
                f.seek(scan.file_offsets[1])
            elif line[:2] == b'#F':
                self._headers['file_origin'] = \
                    line.split()[1].decode('ascii')
            elif line[:2] == b'#E':
                self._headers['epoch_offset'] = int(line.split()[1])
            elif line[:2] == b'#D':
                self._headers['file_date'] = \
                    line.split(None, 1)[1][:-1].decode('ascii')
            elif line[:2] == b'#C' and line.split()[2] == b'User':
                temp = line.decode('ascii').split()
                program, user = temp[1], temp[-1]
                self._headers['program'] = program
                self._headers['user'] = user
            elif line[:2] == b'#O':
                pos = self._headers.setdefault('positioners', [])
                temp = line.decode('ascii').split(None, 1)[1][:-1]
                pos.extend(re.split('  +', temp))

            line = f.readline()

        self._bytes_read = f.tell()
