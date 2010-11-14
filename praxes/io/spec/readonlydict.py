class ReadOnlyDict(object):

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
        "Return a new view of the ``(key, value)`` pairs."
        return self._index.viewitems()

    def keys(self):
        "Return a new view of the keys."
        return self._index.viewkeys()

    def values(self):
        "Return a new view of the values."
        return self._index.viewvalues()

