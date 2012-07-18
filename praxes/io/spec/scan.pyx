cdef extern from 'ctype.h':
    int isdigit(char)

from collections import OrderedDict
import io

import numpy as np

from praxes.io.spec.mapping cimport Mapping
from praxes.io.spec.proxies import (
    create_scalar_proxy, create_epoch_proxy, create_vector_proxy
    )

def create_scan(*args, **kwargs):
    return ScanIndex(*args, **kwargs)


cdef class ScanIndex(Mapping):

    cdef readonly object _file, attrs, data, file_name, id, name
    cdef unsigned long long _bytes_read, _file_offset
    cdef object _mca_data_indices, _scalar_data_index
    cdef char _index_finalized

    property file_offsets:
        def __get__(self):
            return self._file_offset, self._bytes_read

    def __init__(self, f, name, id, file, offset, **kwargs):
        super(ScanIndex, self).__init__({})
        self._file = f
        self.name = name
        self.id = id
        self.file_name = file.name
        self._file_offset = offset
        self._bytes_read = offset

        self.attrs = Mapping(kwargs)

        self._scalar_data_index = []
        self._mca_data_indices = {}
        self._index_finalized = False

        self.data = create_vector_proxy(
            self._file, id, self._scalar_data_index
            )

        self.update()

    def update(self):
        cdef unsigned long long file_offset
        cdef bytes line
        cdef char* c_line
        cdef char ctag

        if self._index_finalized:
            return

        f = self._file#io.open(self.file_name, 'rb', buffering=1024*1024*2)
        attrs = self.attrs._index
        comments = attrs.setdefault('comments', [])
        user_comments = attrs.setdefault('user_comments', [])
        mca_info = attrs.setdefault('mca_info', OrderedDict())
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
                    if len(self._mca_data_indices) == 1:
                        # common case where one MCA is defined
                        # but tagged @MCA in header, and @AMCA in data
                        index = self._mca_data_indices.values()[0]
                    else:
                        index = self._mca_data_indices.setdefault(key, [])
                index.append(file_offset + len(key) + 1)
            elif ctag == b'\n':
                # blank line indicates data has ended
                self._index_finalized = True
                break
            elif ctag == b'#':
                tag = line[1]
                ctag = c_line[1]

                if ctag == b'C':
                    # These can be interleaved with data
                    attrs['comments'].append(line[3:-1].decode('ascii'))
                elif 'labels' in attrs:
                    # non-comment control line, data has ended
                    self._index_finalized = True
                    break
                elif ctag == b'S':
                    attrs['command'] = \
                        ' '.join(line.decode('ascii').split()[2:])
                elif ctag == b'D':
                    attrs['date'] = line[3:-1].decode('ascii')
                elif ctag in (b'T', b'M'):
                    x, val, key = line[1:].decode('ascii').split()
                    key = key[1:-1]
                    attrs['duration'] = (key, float(val))
                    if x == 'M':
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
                elif ctag == b'U':
                    attrs['user_comments'].append(line[3:-1].decode('ascii'))
                elif ctag == b'@':
                    temp = line[1:].decode('ascii').split()
                    if temp[0] == '@CHANN':
                        mca_info.values()[-1]['channels'] = [
                            int(i) for i in temp[1:]
                            ]
                    elif temp[0] == '@CALIB':
                        mca_info.values()[-1]['calibration'] = [
                            float(i) for i in temp[1:]
                            ]
                    else:
                        # this line declared the mca id
                        mca_info[temp[0]] = {}
                        self._mca_data_indices.setdefault(temp[0], [])
                elif ctag == b'L':
                    labels = line.decode('ascii').split()[1:]
                    attrs['labels'] = labels
                    for column, label in enumerate(labels):
                        if label == 'Epoch':
                            self._index[label] = create_epoch_proxy(
                                self._file,
                                label,
                                column,
                                self._scalar_data_index,
                                attrs['epoch_offset']
                                )
                        else:
                            self._index[label] = create_scalar_proxy(
                                self._file,
                                label,
                                column,
                                self._scalar_data_index
                                )

            file_offset += len(line)
            line = readline()
            c_line = line

        self._bytes_read = file_offset
        #f.close()

        if 'positioners' in attrs:
            positioners = attrs.pop('positioners')
            positions = attrs.pop('positions')
            attrs['positions'] = dict(zip(positioners, positions))

        if 'monitor' not in attrs:
            try:
                attrs['monitor'] = [
                    i for i in attrs['user_comments']
                    if i.startswith('monitor =')
                    ][0].split('=')[-1].strip()
            except IndexError:
                attrs['monitor'] = attrs['labels'][-2]
        if 'monitor_efficiency' not in attrs:
            eff = [i for i in attrs['user_comments']
                   if i.startswith('monitor efficiency')]
            if eff:
                eff = float(eff[0].split()[-1])
            else:
                eff = 1
            attrs['monitor_efficiency'] = eff

        for key, index in self._mca_data_indices.items():
            if key not in self._index:
                self._index[key] = create_vector_proxy(
                    self._file, key, index
                    )
