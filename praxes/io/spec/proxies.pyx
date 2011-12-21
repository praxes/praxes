cdef extern from 'stdlib.h':
    double atof(char*)

cdef extern from 'ctype.h':
    int isdigit(char)

import copy
import io

cimport numpy as np
import numpy as np


ALL = slice(None, None, None)

def create_scalar_proxy(file_name, name, column, index):
    return ScalarProxy(file_name, name, column, index)

def create_epoch_proxy(filename, name, column, index, offset):
    return EpochProxy(filename, name, column, index, offset)

def create_vector_proxy(file_name, name, index):
    return VectorProxy(file_name, name, index)


class DataProxyIterator(object):

    def __init__(self, index):
        self.__index = index
        self.__next = 0

    def __next__(self):
        i = self.__next
        if i >= len(self.__index):
            raise StopIteration
        self.__next += 1
        return self.__index[i]

    def next(self):
        return self.__next__()


cdef class DataProxy:

    cdef object _index, fh
    cdef int _n_cols
    cdef readonly object file_name, name

    def __init__(self, file_name, name, index):
        self.file_name = file_name
        self.fh = io.open(self.file_name, 'rb', buffering=1024*1024*2)
        self.name = name
        self._index = index
        self._n_cols = -1

    def __len__(self):
        return len(self._index)

    def __iter__(self):
        return DataProxyIterator(self)

    def __getitem__(self, args):
        raise NotImplementedError

    cdef int n_cols(self) except -1:
        tag = b'\\'
        if self._n_cols == -1:
            try:
                self.fh.seek(self._index[0])
                s = self.fh.readline()
                while s[-2:-1] == tag:
                    s = b''.join([s[:-2].strip(), self.fh.readline()])
                self._n_cols = len(s.strip().split(b' '))
            except IndexError:
                self._n_cols = 0
        return self._n_cols

    cdef object _get_data(
        self,
        np.ndarray[np.int_t, ndim=1, mode=u'strided'] indices,
        np.ndarray[np.int_t, ndim=1, mode=u'strided'] subindices
        ):
        cdef int i, j, n_x, n_y, t_n_x, val_n
        cdef bytes s
        cdef char* cstring
        cdef char c
        cdef char tag = b'\\'
        cdef char val[20]
        cdef np.ndarray[np.float64_t, ndim=1, mode=u'strided'] temp
        cdef np.ndarray[np.float64_t, ndim=2, mode=u'strided'] ret
        cdef object f, lines

        n_y = len(indices)
        n_x = len(subindices)

        t_n_x = self.n_cols()
        if t_n_x == 0:
            return np.array([], dtype=np.float64)
        temp_arr = np.empty((t_n_x, ), dtype=np.float64)
        temp = temp_arr

        ret_arr = np.empty((n_y, n_x), dtype=np.float64)
        ret = ret_arr

        f = self.fh
        for i in range(n_y):
            f.seek(self._index[indices[i]])
            lines = []
            while True:
                lines.append(f.readline())
                c = lines[-1][-2]
                #cstring = lines[-1][-2]
                #c = cstring[0]
                if c != tag:
                    break
            s = b''.join(lines)
            cstring = s

            # convert the string to a temp array
            j = 0
            val_n = 0
            for c in cstring:
                if isdigit(c) or c in (b'-', b'+', b'.', b'e', b'E'):
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


cdef class ScalarProxy(DataProxy):

    cdef int _column

    property shape:
        def __get__(self):
            return (len(self),)

    def __init__(self, file_name, name, column, index):
        super(ScalarProxy, self).__init__(file_name, name, index)
        self._column = column

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

        res = self._get_data(items, np.asarray([self._column]))
        res.shape = (len(items),)
        if isinstance(args, int):
            return res[0]
        return res


cdef class EpochProxy(ScalarProxy):

    cdef readonly int offset

    def __init__(self, file_name, name, column, index, offset):
        super(EpochProxy, self).__init__(file_name, name, column, index)
        self.offset = offset

    def __getitem__(self, args):
        return super(EpochProxy, self).__getitem__(args) + self.offset


cdef class VectorProxy(DataProxy):

    property shape:
        def __get__(self):
            return len(self), self.n_cols()

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
            subitems = np.arange(self.n_cols())
        elif isinstance(extent, int):
            subitems = np.array([extent])
        elif isinstance(extent, slice):
            subitems = np.arange(
                extent.start or 0,
                extent.stop or self.n_cols(),
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
