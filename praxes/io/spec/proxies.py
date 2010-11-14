import numpy as np


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
