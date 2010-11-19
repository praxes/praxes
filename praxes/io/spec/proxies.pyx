cdef extern from 'stdlib.h':
    double atof(char*)

cdef extern from 'ctype.h':
    int isdigit(char)

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

    __slots__ = ['_index', '__file_name', '__name', '__n_cols']

    @property
    def file_name(self):
        return self.__file_name

    @property
    def name(self):
        return self.__name

    @property
    def _n_cols(self):
        try:
            return self.__n_cols
        except AttributeError:
            # determine the number of columns
            b = bytearray()
            with io.open(self.file_name, 'rb') as f:
                f.seek(self._index[0])
                b.extend(f.readline())
                while b[-2] == 92: #b'\\'
                    del(b[-2])
                    b.extend(f.readline())
            self.__n_cols = len(bytes(b).split(b' '))
            return self.__n_cols

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

    def _get_data(
        self,
        np.ndarray[np.int64_t, ndim=1] indices,
        np.ndarray[np.int64_t, ndim=1] subindices
        ):
        cdef int i, j, n_x, n_y, t_n_x, val_n
        cdef bytes data
        cdef char* cdata
        cdef char c
        cdef char val[20]
        cdef np.ndarray[np.float64_t, ndim=1] temp
        cdef np.ndarray[np.float64_t, ndim=2] ret

        n_y = len(indices)
        n_x = len(subindices)

        t_n_x = self._n_cols
        temp_arr = np.empty((t_n_x, ), dtype=np.float64)
        temp = temp_arr

        ret_arr = np.empty((n_y, n_x), dtype=np.float64)
        ret = ret_arr

        for i in range(n_y):
            # get the data string
            with io.open(self.file_name, 'rb') as f:
                f.seek(self._index[indices[i]])
                b = [f.readline()]
                while b[-1][-2] == b'\\':
                    b.append(f.readline())
            data = ''.join(b)
            cdata = data

            # convert the string to a temp array
            j = 0
            val_n = 0
            for c in cdata:
                if isdigit(c) or c in (b'-', b'.', b'e', b'E'):
                    val[j] = c
                    j += 1
                elif j:
                    val[j] = b'\0'
                    j = 0
                    temp[val_n] = atof(val)
                    val_n += 1

            # update the return array
            for j in range(n_x):
                ret[i, j] = temp[subindices[j]]

        return ret_arr


class ScalarProxy(DataProxy):

    __slots__ = ['__column']

    @property
    def shape(self):
        return (len(self),)

    def __init__(self, file_name, name, column, index):
        super(ScalarProxy, self).__init__(file_name, name, index)
        self.__column = column

    def __getitem__(self, args):
        if isinstance(args, tuple):
            raise IndexError('Invalid index')
        elif isinstance(args, int):
            if args > len(self):
                raise IndexError('Invalid index')
            items = np.array([args])
        elif isinstance(args, slice):
            items = np.arange(
                args.start or 0,
                args.stop or len(self),
                args.step or 1
                )
        elif args is Ellipsis:
            items = np.arange(len(self))
        else:
            items = np.asarray(args)

        res = self._get_data(items, np.asarray([self.__column]))
        res.shape = (len(items),)
        if isinstance(args, int):
            return res[0]
        return res


class VectorProxy(DataProxy):

    @property
    def shape(self):
        return len(self), self._n_cols

    def __getitem__(self, args):
        extent = Ellipsis
        if isinstance(args, tuple):
            args, extent = args
        if args is Ellipsis:
            items = np.arange(len(self))
        elif isinstance(args, int):
            if args > len(self):
                raise IndexError('Invalid index')
            items = np.array([args])
        elif isinstance(args, slice):
            items = np.arange(
                args.start or 0,
                args.stop or len(self),
                args.step or 1
                )
        else:
            items = np.asarray(args)

        if extent is Ellipsis:
            subitems = np.arange(self._n_cols)
        elif isinstance(extent, int):
            subitems = np.array([extent])
        elif isinstance(extent, slice):
            subitems = np.arange(
                extent.start or 0,
                extent.stop or self._n_cols,
                extent.step or 1
                )
        else:
            subitems = np.asarray(extent)

        res = self._get_data(items, subitems)
        cdef int x_int, y_int
        y_int, x_int = isinstance(args, int), isinstance(extent, int)
        if y_int or x_int:
            if y_int and x_int:
                return res[0,0]
            res.shape = (np.prod(res.shape),)
        return res