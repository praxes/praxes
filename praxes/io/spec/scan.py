import collections
import io

import numpy as np

from praxes.io.spec.readonlydict import ReadOnlyDict
from praxes.io.spec.proxies import McaProxy, ScalarProxy


class SpecScan(ReadOnlyDict):

    __slots__ = [
        '__attrs', '__bytes_read', '__file_name', '__file_offset', '__id',
        '_index', '__index_finalized', '__mca_data_indices', '__name',
        '__scalar_data_index'
        ]

    @property
    def attrs(self):
        return self.__attrs

    @property
    def file_offsets(self):
        return self.__file_offset, self.__bytes_read

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def __init__(self, name, id, file, offset, **kwargs):
        self.__name = name
        self.__id = id
        self.__file_name = file.name
        self.__file_offset = offset
        self.__bytes_read = offset

        self.__attrs = ReadOnlyDict(**kwargs)
        self.__attrs._index.update(kwargs)

        self.__scalar_data_index = []
        self.__mca_data_indices = {}
        self._index = collections.OrderedDict()
        self.__index_finalized = False

        self.update()

    def update(self):
        if self.__index_finalized:
            return

        f = io.open(self.__file_name, 'rb')
        attrs = self.__attrs._index
        f.seek(self.__bytes_read)
        file_offset = f.tell()
        readline = f.readline
        line = readline()
        while line:
            tag = line[:2]
            if tag[0] == b' ':
                pass
            elif tag[0].isdigit() or tag[0] == b'-':
                self.__scalar_data_index.append(file_offset)
            elif tag[0] == b'@':
                key = line.split(None, 1)[0]
                try:
                    index = self.__mca_data_indices[key]
                except KeyError:
                    index = self.__mca_data_indices.setdefault(key, [])
                index.append(file_offset)
            elif tag == b'#S':
                if 'command' in attrs:
                    self.__index_finalized = True
                    break
                attrs['command'] = ' '.join(line.split()[2:])
            elif tag == b'#D':
                attrs['date'] = line[3:-1]
            elif tag in (b'#T', b'#M'):
                x, val, key = line.split()
                key = key[1:-1]
                attrs['duration'] = (key, float(val))
                if x == b'#M':
                    attrs['monitor'] = key
            elif tag == b'#G':
                orientations = attrs.setdefault('orientations', [])
                orientations.append(
                    [float(i) for i in line.split()[1:]]
                    )
            elif tag == b'#Q':
                attrs['hkl'] = [float(i) for i in line.split()[1:]]
            elif tag == b'#P':
                positions = attrs.setdefault('positions', [])
                positions.extend(
                    [float(i) for i in line.split()[1:]]
                    )
            elif tag == b'#C':
                comments = attrs.setdefault('comments', [])
                comments.append(line[3:-1])
            elif tag == b'#U':
                user_comments = attrs.setdefault('user_comments', [])
                user_comments.append(line[3:-1])
            elif tag == b'#L':
                attrs['labels'] = labels = line.split()[1:]
                for column, label in enumerate(labels):
                    self._index[label] = ScalarProxy(
                        self.__file_name,
                        label,
                        column,
                        self.__scalar_data_index
                        )

            file_offset += len(line)
            line = readline()

        self.__bytes_read = f.tell()
        f.close()

        if 'positioners' in attrs:
            positioners = attrs.pop('positioners')
            positions = attrs.pop('positions')
            attrs['positions'] = dict(zip(positioners, positions))

        for key, index in self.__mca_data_indices.items():
            if key not in self._index:
                self._index[key] = McaProxy(self.__file_name, key, index)
