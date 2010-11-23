
cdef class ReadOnlyDict:

    cdef object _lock
    cdef readonly object _index