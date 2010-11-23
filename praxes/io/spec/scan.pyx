cdef extern from 'ctype.h':
    int isdigit(char)

import io

import numpy as np

from praxes.io.spec.readonlydict cimport ReadOnlyDict
from praxes.io.spec.proxies import ScalarProxy, VectorProxy


cdef class SpecScan(ReadOnlyDict):

    cdef readonly object attrs, data, file_name, id, name
    cdef int _bytes_read, _file_offset
    cdef object _mca_data_indices, _scalar_data_index
    cdef char _index_finalized

    property file_offsets:
        def __get__(self):
            with self._lock:
                return self._file_offset, self._bytes_read

    def __init__(self, name, id, file, offset, lock, **kwargs):
        super(SpecScan, self).__init__(lock, ordered=True)
        self.name = name
        self.id = id
        self.file_name = file.name
        self._file_offset = offset
        self._bytes_read = offset

        self.attrs = ReadOnlyDict(lock, **kwargs)
        self.attrs._index.update(kwargs)

        self._scalar_data_index = []
        self._mca_data_indices = {}
        self._index_finalized = False

        self.data = VectorProxy(
            self.file_name, id, self._scalar_data_index, lock
            )

        self.update()

    def update(self):
        cdef int file_offset
        cdef bytes line
        cdef char* c_line
        cdef char ctag

        try:
            self._lock.acquire()
            if self._index_finalized:
                return

            f = io.open(self.file_name, 'rb', buffering=1024*1024*2)
            attrs = self.attrs._index
            f.seek(self._bytes_read)
            file_offset = f.tell()
            readline = f.readline
            line = readline()
            c_line = line
            while line:
                tag = line[0]
                ctag = c_line[0]
                if ctag == b' ':
                    pass
                elif isdigit(ctag) or ctag == b'-':
                    self._scalar_data_index.append(file_offset)
                elif ctag == b'@':
                    key = line.split(None, 1)[0].decode('ascii')
                    try:
                        index = self._mca_data_indices[key]
                    except KeyError:
                        index = self._mca_data_indices.setdefault(key, [])
                    index.append(file_offset + len(key) + 1)
                elif ctag == b'#':
                    tag = line[1]
                    ctag = c_line[1]
                    if ctag == b'S':
                        if 'command' in attrs:
                            self._index_finalized = True
                            break
                        attrs['command'] = \
                            ' '.join(line.decode('ascii').split()[2:])
                    elif ctag == b'D':
                        attrs['date'] = line[3:-1]
                    elif ctag in (b'T', b'M'):
                        x, val, key = line[1:].decode('ascii').split()
                        key = key[1:-1]
                        attrs['duration'] = (key, float(val))
                        if x == b'M':
                            attrs['monitor'] = key
                    elif ctag == b'G':
                        orientations = attrs.setdefault('orientations', [])
                        temp = line.decode('ascii').split()[1:]
                        orientations.append(
                            [float(i) for i in temp]
                            )
                    elif ctag == b'Q':
                        temp = line.decode('ascii').split()[1:]
                        attrs['hkl'] = [float(i) for i in temp]
                    elif ctag == b'P':
                        positions = attrs.setdefault('positions', [])
                        temp = line.decode('ascii').split()[1:]
                        positions.extend(
                            [float(i) for i in temp]
                            )
                    elif ctag == b'C':
                        comments = attrs.setdefault('comments', [])
                        comments.append(line[3:-1].decode('ascii'))
                    elif ctag == b'U':
                        user_comments = attrs.setdefault('user_comments', [])
                        user_comments.append(line[3:-1].decode('ascii'))
                    elif ctag == b'L':
                        labels = line.decode('ascii').split()[1:]
                        attrs['labels'] = labels
                        if 'monitor' not in attrs:
                            attrs['monitor'] = labels[-1]
                        for column, label in enumerate(labels):
                            self._index[label] = ScalarProxy(
                                self.file_name,
                                label,
                                column,
                                self._scalar_data_index,
                                self._lock
                                )

                file_offset += len(line)
                line = readline()
                c_line = line

            self._bytes_read = f.tell()
            f.close()

            if 'positioners' in attrs:
                positioners = attrs.pop('positioners')
                positions = attrs.pop('positions')
                attrs['positions'] = dict(zip(positioners, positions))

            for key, index in self._mca_data_indices.items():
                if key not in self._index:
                    self._index[key] = VectorProxy(
                        self.file_name, key, index, self._lock
                        )
        finally:
            self._lock.release()
