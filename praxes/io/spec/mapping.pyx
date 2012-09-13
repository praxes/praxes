import collections


cdef class Mapping:

    def __init__(self, index):
        self._index = index

    def __contains__(self, item):
        return item in self._index

    def __getitem__(self, item):
        return self._index[item]

    def __iter__(self):
        return iter(self._index)

    def __len__(self):
        return len(self._index)

    def get(self, key, default=None):
        "Return the value for key, or return default"
        return self._index.get(key, default)

    def items(self):
        "Return a new view of the ``(key, value)`` pairs."
        return self._index.items()

    def keys(self):
        "Return a new view of the keys."
        return self._index.keys()

    def values(self):
        "Return a new view of the values."
        return self._index.values()


collections.Mapping.register(Mapping)
