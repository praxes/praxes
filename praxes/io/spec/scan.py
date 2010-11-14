import collections

import numpy as np

class Index(object):

    __slots__ = ['_index']

    def __init__(self, **kwargs):
        self._index = dict(**kwargs)

    def __contains__(self, item):
        return item in self._index

    def __getitem__(self, item):
        return self._index[item]

    def __iter__(self):
        return iter(self._index)

    def __len__(self):
        return len(self._index)

    def get(self, key, default=None):
        return self._index.get(key, default)

    def items(self):
        "Return a new view of the index's ``(key, value)`` pairs."
        return self._index.viewitems()

    def keys(self):
        "Return a new view of the index's keys."
        return self._index.viewkeys()

    def values(self):
        "Return a new view of the index's values."
        return self._index.viewvalues()


class SpecScan(object):



    __slots__ = [
        '__attrs', '__bytes_read', '__file_name', '__file_offset', '__id',
        '__index', '__index_finalized', '__mca_data_indices', '__name',
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

        self.__attrs = Index(**kwargs)
        self.__attrs._index.update(kwargs)

        self.__scalar_data_index = []
        self.__mca_data_indices = {}
        self.__index = collections.OrderedDict()
        self.__index_finalized = False

        self.update()

    def __contains__(self, item):
        return item in self.__index

    def __getitem__(self, item):
        return self.__index[item]

    def __iter__(self):
        return iter(self.__index)

    def __len__(self):
        return len(self.__index)

    def get(self, key, default=None):
        return self.__index.get(key, default)

    def items(self):
        "Return a new view of the scan's attributes' ``(key, val)`` pairs."
        return self.__index.viewitems()

    def keys(self):
        "Return a new view of the scan's attributes' keys."
        return self.__index.viewkeys()

    def values(self):
        "Return a new view of the scan's attributes' values."
        return self.__index.viewvalues()


    def update(self):
        if self.__index_finalized:
            return

        with open(self.__file_name, 'rb') as f:
            attrs = self.__attrs._index
            f.seek(self.__bytes_read)
            file_offset = f.tell()
            line = f.readline()
            while line:
                if line[0].isdigit() or line[0] == '-':
                    self.__scalar_data_index.append(file_offset)
                elif line[0] == '@':
                    key = line.split(None, 1)[0]
                    try:
                        index = self.__mca_data_indices[key]
                    except KeyError:
                        index = self.__mca_data_indices.setdefault(key, [])
                    index.append(file_offset)
                elif line[:2] == '#S':
                    if 'command' in attrs:
                        self.__index_finalized = True
                        break
                    attrs['command'] = ' '.join(line.split()[2:])
                elif line[:2] == '#D':
                    attrs['date'] = line[3:-1]
                elif line[:2] in ('#T', '#M'):
                    x, val, key = line.split()
                    key = key[1:-1]
                    attrs['duration'] = (key, float(val))
                    if x == '#M':
                        attrs['monitor'] = key
                elif line[:2] == '#G':
                    orientations = attrs.setdefault('orientations', [])
                    orientations.append(
                        [float(i) for i in line.split()[1:]]
                        )
                elif line[:2] == '#Q':
                    attrs['hkl'] = [float(i) for i in line.split()[1:]]
                elif line[:2] == '#P':
                    positions = attrs.setdefault('positions', [])
                    positions.extend(
                        [float(i) for i in line.split()[1:]]
                        )
                elif line[:2] == '#C':
                    comments = attrs.setdefault('comments', [])
                    comments.append(line[3:-1])
                elif line[:2] == '#U':
                    user_comments = attrs.setdefault('user_comments', [])
                    user_comments.append(line[3:-1])
                elif line[:2] == '#L':
                    attrs['labels'] = labels = line.split()[1:]
                    for column, label in enumerate(labels):
                        self.__index[label] = ScalarProxy(
                            self.__file_name,
                            label,
                            column,
                            self.__scalar_data_index
                            )

                file_offset = f.tell()
                line = f.readline()

            self.__bytes_read = f.tell()

        if 'positioners' in attrs:
            positioners = attrs.pop('positioners')
            positions = attrs.pop('positions')
            attrs['positions'] = dict(zip(positioners, positions))

        for key, index in self.__mca_data_indices.items():
            if key not in self.__index:
                self.__index[key] = McaProxy(self.__file_name, key, index)


class ScalarProxy(object):

    __slots__ = ['__column', '__data_index', '__file_name', '__name']

    @property
    def name(self):
        return self.__name

    def __init__(self, file_name, name, column, data_index):
        self.__file_name = file_name
        self.__name = name
        self.__column = column
        self.__data_index = data_index

    def __len__(self):
        return len(self.__data_index)

    def __iter__(self):
        def g(f):
            for i in xrange(len(f)):
                yield(f[i])
        return g(self)

    def __getitem__(self, args):
        with open(self.__file_name) as f:
            if isinstance(args, slice):
                args = xrange(
                    args.start or 0,
                    args.stop or len(self),
                    args.step or 1
                    )
            elif args is Ellipsis:
                args = xrange(len(self))
            elif isinstance(args, tuple):
                raise IndexError('Invalid index')
            if isinstance(args, int):
                f.seek(self.__data_index[args])
                l = f.readline()
                return np.fromstring(l, dtype='d', sep=' ')[self.__column]
            temp = []
            for i in args:
                f.seek(self.__data_index[i])
                l = f.readline()
                temp.append(np.fromstring(l, dtype='f', sep=' ')[self.__column])
            return np.asarray(temp)


class McaProxy(object):

    __slots__ = ['__file_name', '__data_index', '__name']

    @property
    def name(self):
        return self.__name

    def __init__(self, file_name, name, data_index):
        self.__file_name = file_name
        self.__name = name
        self.__data_index = data_index

    def __len__(self):
        return len(self.__data_index)

    def __iter__(self):
        def g(f):
            for i in xrange(len(f)):
                yield(f[i])
        return g(self)

    def __getitem__(self, args):
        with open(self.__file_name) as f:
            extent = Ellipsis
            if isinstance(args, tuple):
                extent = args[1:]
                args = args[0]
            if isinstance(args, slice):
                args = xrange(
                    args.start or 0,
                    args.stop or len(self),
                    args.step or 1
                    )
            elif args is Ellipsis:
                args = xrange(len(self))

            if isinstance(args, int):
                f.seek(self.__data_index[args])
                l = f.readline().split(None, 1)[1].rstrip()
                while l[-1] == '\\':
                    l = l[:-1] + f.readline.rstrip()
                return np.fromstring(l, dtype='d', sep=' ')[extent]
            temp = []
            for i in args:
                f.seek(self.__data_index[i])
                l = f.readline().split(None, 1)[1].rstrip()
                while l[-1] == '\\':
                    l = l[:-1] + f.readline.rstrip()
                temp.append(np.fromstring(l, dtype='f', sep=' ')[extent])
            return np.asarray(temp)
