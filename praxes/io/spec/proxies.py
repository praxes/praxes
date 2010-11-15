import io

import numpy as np


class DataProxy(object):

    __slots__ = ['_index', '__file_name', '__name']

    @property
    def file_name(self):
        return self.__file_name

    @property
    def name(self):
        return self.__name

    def __init__(self, file_name, name, index):
        self.__file_name = file_name
        self.__name = name
        self._index = index

    def __len__(self):
        return len(self._index)

    def __iter__(self):
        def g(f):
            for i in xrange(len(f)):
                yield(f[i])
        return g(self)

    def __getitem__(self, args):
        raise NotImplementedError


class ScalarProxy(DataProxy):

    __slots__ = ['__column']

    def __init__(self, file_name, name, column, index):
        super(ScalarProxy, self).__init__(file_name, name, index)
        self.__column = column

    def __getitem__(self, args):
        with io.open(self.file_name, 'rb') as f:
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

            readline = f.readline
            if isinstance(args, int):
                f.seek(self._index[args])
                l = readline()
                return np.fromstring(l, dtype='d', sep=' ')[self.__column]
            temp = []
            for i in args:
                f.seek(self._index[i])
                l = readline()
                temp.append(np.fromstring(l, dtype='f', sep=' ')[self.__column])
            return np.asarray(temp)


class McaProxy(DataProxy):

    def __getitem__(self, args):
        with io.open(self.file_name, 'rb') as f:
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

            readline = f.readline
            if isinstance(args, int):
                f.seek(self._index[args])
                l = readline().split(None, 1)[1].rstrip()
                while l[-1] == '\\':
                    l = l[:-1] + readline().rstrip()
                return np.fromstring(l, dtype='d', sep=' ')[extent]
            temp = []
            for i in args:
                f.seek(self._index[i])
                l = readline().split(None, 1)[1].rstrip()
                while l[-1] == '\\':
                    l = l[:-1] + readline().rstrip()
                temp.append(np.fromstring(l, dtype='f', sep=' ')[extent])
            return np.asarray(temp)
