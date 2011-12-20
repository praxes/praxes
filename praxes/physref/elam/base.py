import collections
from functools import wraps

def memoize(f, cache={}):
    @wraps(f)
    def g(*args, **kwargs):
        key = (f, tuple(args), frozenset(list(kwargs.items())))
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return g


class Mapping(collections.Hashable, collections.Mapping):

    def __contains__(self, item):
        return item in self.keys()

    def __getitem__(self, item):
        raise NotImplementedError

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(list(self.keys()))

    def get(self, item, default=None):
        "Return the value for *key*, or return *default*"
        return self[item] if item in self else None

    def items(self):
        "Return a new view of the (key, value) pairs"
        return zip(self.keys(), self.values())

    def keys(self):
        raise NotImplementedError

    def values(self):
        "return a new view of the values"
        return (self[i] for i in self.keys())
