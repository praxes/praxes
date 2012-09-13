import collections


class Mapping(collections.Hashable, collections.Mapping):

    '''The base class used for accessing physical reference data

    Subclasses must provide an implementation of the _keys property and
    the __hash__ and __getitem__ methods.
    '''

    @property
    def _keys(self):
        raise NotImplementedError

    def __contains__(self, item):
        return item in self._keys

    def __iter__(self):
        return iter(self._keys)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __len__(self):
        return len(self._keys)

    def get(self, item, default=None):
        "Return the value for *key*, or return *default*"
        return self[item] if item in self else None

    def items(self):
        "Return a new view of the (key, value) pairs"
        return super(Mapping, self).items()

    def keys(self):
        "return a new view of the keys"
        return super(Mapping, self).keys()

    def values(self):
        "return a new view of the values"
        return super(Mapping, self).values()
