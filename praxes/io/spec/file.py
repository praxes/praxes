import __builtin__

from .fileindex import FileIndex
from .scan import SpecScan


def open(file_name):
    return SpecFile(file_name)


class SpecFile(object):

    @property
    def file(self):
        return __builtin__.open(self._name)

    @property
    def name(self):
        return self._name

    def __init__(self, file_name):
        self._name = file_name
        self._index = FileIndex(file_name)

    def __getitem__(self, item):
        return SpecScan(self, self._index[item])

    def __iter__(self):
        return iter(self._index)

    def __len__(self):
        return len(self._index)

    def iteritems(self):
        def g(f):
            for id, index in self._index.iteritems():
                yield id, SpecScan(self, index)
        return g(self)

    def iterkeys(self):
        return self._index.iterkeys()

    def itervalues(self):
        def g(f):
            for index in self._index.itervalues():
                yield SpecScan(self, index)
        return g(self)

    def items(self):
        return [
            (id, SpecScan(self, index)) for (id, index) in self._index.items()
            ]

    def keys(self):
        return self._index.keys()

    def update(self):
        self._index.update()

    def values(self):
        return [SpecScan(self, index) for index in self._index.values()]
