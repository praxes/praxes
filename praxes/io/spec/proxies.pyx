cdef extern from 'stdlib.h':
    double atof(char*)

import io

cimport numpy as np
import numpy as np


ALL = slice(None, None, None)


class DataProxyIterator(object):

    def __init__(self, proxy):
        self.__proxy = proxy
        self.__next = 0

    def next(self):
        i = self.__next
        if i >= len(self.__proxy):
            raise StopIteration
        self.__next += 1
        return self.__proxy[i]


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
        return DataProxyIterator(self)

    def __getitem__(self, args):
        raise NotImplementedError

    def _get_data(self, item, extent=None):
        cdef bytes b
        with io.open(self.file_name, 'rb') as f:
            f.seek(self._index[item])
            b = f.readline()
            while b[-2] == b'\\':
                b = b[:-2] + f.readline()

        l = b.split()
        if isinstance(extent, int):
            return [l[extent]]
        if extent is None or extent is Ellipsis or extent == ALL:
            return l
        elif isinstance(extent, slice):
            if extent.stop is None:
                raise ValueError('slice must declare stop value')
            extent = xrange(
                extent.start or 0,
                extent.stop,
                extent.step or 1
                )
        return [l[i] for i in extent]


class ScalarProxy(DataProxy):

    __slots__ = ['__column']

    def __init__(self, file_name, name, column, index):
        super(ScalarProxy, self).__init__(file_name, name, index)
        self.__column = column

    def __getitem__(self, args):
        cdef char* c_string
        cdef bytes py_string
        cdef int i, j, n_x
        cdef np.ndarray[np.float64_t, ndim=1] ret

        if isinstance(args, tuple):
            raise IndexError('Invalid index')
        if isinstance(args, slice):
            args = xrange(
                args.start or 0,
                args.stop or len(self),
                args.step or 1
                )
        elif args is Ellipsis:
            args = xrange(len(self))
        n_x = 1 if isinstance(args, int) else len(args)

        ret_arr = np.empty((n_x,), dtype=np.float64)
        ret = ret_arr

        # This lets us write a single loop:
        nargs = [args] if isinstance(args, int) else args

        j = 0
        column = self.__column
        for i in nargs:
            l = self._get_data(i, column)
            for py_string in l:
                c_string = py_string
                ret[j] = atof(c_string)
                j += 1
        if isinstance(args, int):
            ret_arr = ret_arr[0]
        return ret_arr


class McaProxy(DataProxy):

    @property
    def shape(self):
        return len(self), self.__n_cols

    def __init__(self, file_name, name, index):
        super(McaProxy, self).__init__(file_name, name, index)
        self.__n_cols = len(self._get_data(0))

    def __getitem__(self, args):
        cdef char* c_string
        cdef bytes py_string
        cdef int i, j, n_x, n_y
        cdef np.ndarray[np.float64_t, ndim=1] ret

        extent = Ellipsis
        if isinstance(args, tuple):
            if len(args) > 2:
                raise IndexError('Invalid index')
            extent = args[1]
            args = args[0]
        if isinstance(args, slice):
            args = xrange(
                args.start or 0,
                args.stop or len(self),
                args.step or 1
                )
        elif args is Ellipsis:
            args = xrange(len(self))
        n_y = 1 if isinstance(args, int) else len(args)

        if extent == ALL:
            extent = Ellipsis
        if extent is Ellipsis:
            n_x = self.__n_cols
        elif isinstance(extent, int):
            n_x = 1
        elif isinstance(extent, slice):
            extent = xrange(
                extent.start or 0,
                extent.stop or self.__n_cols,
                extent.step or 1
                )
            n_x = len(extent)
        elif isinstance(extent, list):
            n_x = len(extent)

        ret_arr = np.empty((n_y * n_x,), dtype=np.float64)
        ret = ret_arr

        # This lets us write a single loop:
        nargs = [args] if isinstance(args, int) else args

        j = 0
        for i in nargs:
            l = self._get_data(i, extent)
            for py_string in l:
                c_string = py_string
                ret[j] = atof(c_string)
                j += 1
        ret_arr.shape = (n_y, n_x)
        if isinstance(args, int):
            ret_arr = ret_arr[args]
        if isinstance(extent, int):
            ret_arr = ret_arr[extent]
        return ret_arr
