from collections import OrderedDict


class ReadOnlyDict(object):

    __slots__ = ['_index', '_lock']

    def __init__(self, lock, ordered=False, **kwargs):
        self._lock = lock
        self._index = OrderedDict(**kwargs) if ordered else dict(**kwargs)

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
        return self._index.viewitems()

    def keys(self):
        "Return a new view of the keys."
        return self._index.viewkeys()

    def values(self):
        "Return a new view of the values."
        return self._index.viewvalues()

