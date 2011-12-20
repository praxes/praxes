"""
"""

import posixpath
import sys

from distutils.version import LooseVersion

import h5py

from .registry import registry
from .utils import memoize#, simple_eval


# this class is necessary because h5py does not accept unicode values:
class AttrsProxy(object):

    def __init__(self, attrs):
        self._attrs = attrs

    def __len__(self):
        return len(self._attrs)

    def __contains__(self, key):
        return key in self._attrs

    def __delitem__(self, key):
        del self._attrs[key]

    def __getitem__(self, key):
        return self._attrs[key]

    def __setitem__(self, key, val):
        if sys.version_info[0] < 3:
            if isinstance(val, str):
                val = str(val)
        self._attrs[key] = val

    def get(self, key, default=None):
        return self._attrs.get(key, default)

    def keys(self):
        return self._attrs.keys()

    def values(self):
        return self._attrs.values()

    def items(self):
        return self._attrs.items()


class _RegisterPhynxClass(type):

    def __init__(cls, name, bases, attrs):
        if cls.__name__ is not 'Node':
            from .registry import registry
            registry.register(cls)


class Node(object, metaclass=_RegisterPhynxClass):

    """A mix-in class to propagate attributes from the parent object to
    the new HDF5 group or dataset, and to expose those attributes via
    python properties.
    """

    @property
    @memoize
    def attrs(self):
        return AttrsProxy(self._h5node.attrs)

    @property
    def entry(self):
        target = self.file['/'.join(self.id.split('/')[:2])]
        return target if isinstance(target, registry['Entry']) else None

    @property
    @memoize
    def file(self):
        from .file import File
        return File(self._h5node.file, self._lock)

#    @property
#    def lock(self):
#        return self._lock

#    @property
#    def npoints(self):
#        return self.attrs.get('npoints', 0)

    @property
    @memoize
    def id(self):
        return self._h5node.name

#    @property
#    def measurement(self):
#        return getattr(self.entry, 'measurement', None)

    @property
    @memoize
    def name(self):
        return posixpath.basename(self.id)

    @property
    @memoize
    def path(self):
        return posixpath.dirname(self.id)

    @property
    @memoize
    def parent(self):
        return self.file[self.path]

    def __init__(self, h5node, lock):
        self._h5node = h5node
        self._lock = lock
#        for attr in ['acquisition_shape', 'source_file', 'npoints']:
#            if (attr not in self.attrs) and (attr in parent_object.attrs):
#                self.attrs[attr] = parent_object.attrs[attr]

    def __len__(self):
        return self._h5node.__len__()

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._h5node.__eq__(other._h5node)

    def __hash__(self):
        return hash((self.__class__, self._h5node))

    def __enter__(self):
        self._lock.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self._lock.__exit__(type, value, traceback)

    def __bool__(self):
        return bool(self._h5node.id)
