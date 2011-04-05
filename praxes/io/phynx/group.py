"""
"""

from __future__ import absolute_import, with_statement

import posixpath
import warnings

import h5py
import numpy as np

from .base import Node
from .registry import registry
from .utils import sync


# keep a list of unrecognized classes, so we only raise an error the first time:
_unrecognized = []

def update_metadata(node, cls=None, nx_class=None, **kwargs):
    # these are items that only need to be set when a node is first created,
    # not each time the interface to an existing node is created
    if cls is not None:
        node.attrs['class'] = cls
    if nx_class is not None:
        node.attrs['NX_class'] = nx_class
    for key, val in kwargs.iteritems():
        if not np.isscalar(val):
            val = str(val)
        node.attrs[key] = val

def pop_dataset_kwargs(kwargs):
    dset = {}
    dset['shape'] = kwargs.pop('shape')
    dset['dtype'] = kwargs.pop('dtype')
    dset['exact'] = kwargs.pop('exact', False)
    for key in (
        'data', 'chunks', 'compression', 'shuffle', 'fletcher32', 'maxshape'
        'compression_opts', '_rawid'
        ):
        dset[key] = kwargs.pop(key, None)
    return dset


class Group(Node):

    """
    """

    @property
    def children(self):
        return self.values()

    @property
    def entry(self):
        target = self['/'.join(self.name.split('/')[:2])]
        return target if isinstance(target, registry['Entry']) else None

    @property
    def measurement(self):
        return getattr(self.entry, 'measurement', None)

    @property
    @sync
    def signals(self):
        from .dataset import Signal
        return dict(
            (posixpath.basename(j.name), j)
            for j in sorted(i for i in self.values() if isinstance(i, Axis))
            )

    @property
    @sync
    def axes(self):
        from .dataset import Axis
        return dict(
            (posixpath.basename(j.name), j)
            for j in sorted(i for i in self.values() if isinstance(i, Axis))
            )

#    def __init__(self, h5node, lock):
#        """
#        Open an existing group or create a new one.
#
#        attrs is a python dictionary of strings and numbers to be saved as hdf5
#        attributes of the group.
#
#        """
#        super(Group, self).__init__(h5node, lock)
#        if 'class' not in self.attrs:
#            self.attrs['class']
#        self.attrs['class'] = self.__class__.__name__
#            try:
#                self.attrs['NX_class'] = self.nx_class
#            except AttributeError:
#                pass
#
#        _PhynxProperties.__init__(self, parent_object)
#
#        if attrs:
#            for attr, val in attrs.iteritems():
#                if not np.isscalar(val):
#                    val = str(val)
#                self.attrs[attr] = val

    @sync
    def __repr__(self):
        try:
            return '<%s group "%s" (%d members, %d attrs)>' % (
                self.__class__.__name__,
                self.name,
                len(self),
                len(self.attrs)
            )
        except Exception:
            return "<Closed %s group>" % self.__class__.__name__

    @sync
    def __getitem__(self, name):
        # TODO: would be better to check the attribute without having to
        # create create the group twice. This might be possible with the
        # 1.8 API.
        h5node = self._h5node[name]

        cls = h5node.attrs.get('class')
        if cls is None:
            cls = h5node.attrs.get('NX_class')

        if cls is not None:
            try:
                return registry[cls](h5node, self._lock)
            except (KeyError, TypeError):
                if cls not in _unrecognized:
                    _unrecognized.append(cls)
                    warnings.warn(
                        'phynx does not recognize the "%r" class and will '
                        'provide a default interface instead. If this is an '
                        'official phynx or NeXus class, please file a bug '
                        'report with the praxes project at '
                        'https://github.com/praxes/praxes/issues.' % cls
                        )

        cls = 'Group' if isinstance(h5node, h5py.Group) else 'Dataset'
        return registry[cls](h5node, self._lock)

    def __setitem__(self, name, value):
        self._h5node.__setitem__(name, value)

    def create_dataset(self, name, shape, dtype, type='Dataset', **kwargs):
        cls = registry[type]
        node = self._h5node.create_dataset(
            name, shape, dtype, **pop_dataset_kwargs(kwargs)
            )
        res = cls(node, self._lock)
        nx_class = getattr(res, 'nx_class', None)
        update_metadata(res, cls=cls.__name__, nx_class=nx_class, **kwargs)
        return res

#    @sync
#    def require_dataset(self, name, shape, dtype, type='Dataset', **kwargs):
#        if not name in self:
#            return self.create_dataset(name, shape, dtype, **kwargs)
#        else:
#            requested_cls = registry[type]
#            node = self._h5node.require_dataset(
#                name, shape, dtype, **pop_dataset_kwargs(kwargs)
#                )
#            cls = registy[node.attrs.get('class', 'Dataset')]
#            if not issubclass(cls, requested_class):
#                raise NameError("Incompatible object %s already exists" % cls)
#            res = cls(node, self._lock)
#            update_metadata(res, **kwargs)
#            return res

    def create_group(self, name, type='Group', **kwargs):
        cls = registry[type]
        node = self._h5node.create_group(name)
        res = cls(node, self._lock)
        nx_class = getattr(res, 'nx_class', None)
        update_metadata(res, type, nx_class, **kwargs)
        return res

#    @sync
#    def require_group(self, name, type='Group', **kwargs):
#        if not name in self:
#            return self.create_group(name, type, **kwargs)
#        else:
#            requested_cls = registry[type]
#            node = self._h5node.require_group(name)
#            cls = registy[node.attrs.get('class', 'Group')]
#            if not issubclass(cls, requested_cls):
#                raise NameError("Incompatible object %s already exists" % cls)
#            res = cls(node, self._lock)
#            if attrs:
#                add_metadata(res, **kwargs)
#            return res

    @sync
    def values(self):
        return [self[key] for key in self._h5node.keys()]

    @sync
    def keys(self):
        return self._h5node.keys()

    @sync
    def items(self):
        return [(key, self[key]) for key in self._h5node.keys()]
