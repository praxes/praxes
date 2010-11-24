import io
import os
import re

from praxes.io.spec.readonlydict cimport ReadOnlyDict
from praxes.io.spec.scan import SpecScan


class DummyRLock(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def acquire(self):
        pass

    def release(self):
        pass


cdef class SpecFile(ReadOnlyDict):

    "An OrderedDict-like interface to scans contained in spec data files."

    cdef readonly object name
    cdef int _bytes_read
    cdef object _headers

    def __init__(self, file_name, lock=None):
        if lock is True:
            import threading
            lock = threading.RLock()
        lock = lock or DummyRLock()
        super(SpecFile, self).__init__(lock, ordered=True)

        self.name = file_name
        self._bytes_read = 0
        self._headers = {}

        self.update()

    def update(self):
        try:
            f = None
            self._lock.acquire()
            "Update the file index based on any data appended to the file."
            if os.stat(self.name).st_size == self._bytes_read:
                return

            f = io.open(self.name, 'rb')
            if len(self):
                # updating an existing file index,
                # may need to update last scan
                list(self._index.values())[-1].update()

            f.seek(self._bytes_read)
            file_offset = f.tell()
            line = f.readline()
            while line:
                if line[:2] == b'#S':
                    name = id = line.split()[1].decode('ascii')
                    # need to assure that id is unique:
                    dup = 1
                    while id in self._index:
                        dup += 1
                        id = '%s.%d' % (name, dup)
                    scan = SpecScan(
                        name, id, self, file_offset, lock=self._lock,
                        **self._headers
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

                file_offset += len(line)
                line = f.readline()

            self._bytes_read = f.tell()
        finally:
            if f is not None:
                f.close()
