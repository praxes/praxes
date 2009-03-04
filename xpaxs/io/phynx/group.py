"""
"""

from __future__ import absolute_import, with_statement

from posixpath import basename

try:
    from enthought.traits.api import HasTraits
except ImportError:
    class HasTraits(object):
        pass
import h5py
import numpy as np

from .base import _PhynxProperties
from .dataset import Axis, Dataset, Signal
from .registry import registry
from .utils import sync


class Group(h5py.Group, _PhynxProperties, HasTraits):

    def __init__(self, parent_object, name, **attrs):
        """
        Open an existing group or create a new one.

        attrs is a python dictionary of strings and numbers to be saved as hdf5
        attributes of the group.

        """
        with parent_object._lock:
            if name in parent_object:
                super(Group, self).__init__(
                    parent_object, name, create=False
                )
            else:
                super(Group, self).__init__(
                    parent_object, name, create=True
                )

                self.attrs['class'] = self.__class__.__name__
                try:
                    self.attrs['NX_class'] = self.nx_class
                except AttributeError:
                    pass

                _PhynxProperties.__init__(self, parent_object)

            if attrs:
                for attr, val in attrs.iteritems():
                    try:
                        assert np.isscalar(val)
                    except AssertionError:
                        raise TypeError(
                            'attributes must be strings or scalars, '
                            'got %r which is of %r' % (val, type(val))
                        )
                    self.attrs[attr] = val

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
        item = super(Group, self).__getitem__(name)
        if 'class' in item.attrs:
            return registry[item.attrs['class']](self, name)
        elif 'NX_class' in item.attrs:
            return registry[item.attrs['NX_class']](self, name)
        elif isinstance(item, h5py.Dataset):
            return Dataset(self, name)
        else:
            return Group(self, name)

    @sync
    def __setitem__(self, name, value):
        super(Group, self).__setitem__(name, value)

    @property
    def children(self):
        # used by traits
        return self.listobjects()

    @property
    @sync
    def name(self):
        return basename(super(Group, self).name)

    @property
    @sync
    def path(self):
        return super(Group, self).name

    @property
    @sync
    def signals(self):
        return dict(
            [(s.name, s) for s in self.iterobjects()
                if isinstance(s, Signal)]
        )

    @property
    @sync
    def axes(self):
        return dict(
            [(a.name, a) for a in self.iterobjects() if isinstance(a, Axis)]
        )

    @sync
    def get_sorted_axes_list(self, direction=1):
        return sorted([a for a in self.axes.values() if a.axis==direction])

    @sync
    def get_sorted_signals_list(self, direction=1):
        return sorted([s for s in self.signals.values()])

    def create_dataset(self, name, *args, **kwargs):
        type = kwargs.pop('type', 'Dataset')
        return registry[type](self, name, *args, **kwargs)

    @sync
    def require_dataset(self, name, *args, **kwargs):
        type = kwargs.setdefault('type', 'Dataset')
        if not name in self:
            return self.create_dataset(name, *args, **kwargs)
        else:
            item = self[name]
            if not isinstance(item, registry[type]):
                raise NameError(
                    "Incompatible object (%s) already exists" % \
                    item.__class__.__name__
                )
            if args or kwargs:
                raise RuntimeError(
                    "Can not define data for existing %s object" % \
                    item.__class__.__name__
                )
            return item

    def create_group(self, name, type='Group', **data):
        return registry[type](self, name, **data)

    @sync
    def require_group(self, name, type='Group', **data):
        if not name in self:
            return self.create_group(name, type, **data)
        else:
            item = self[name]
            if not isinstance(item, registry[type]):
                raise NameError(
                    "Incompatible object (%s) already exists" % \
                    item.__class__.__name__
                )
            if data:
                raise RuntimeError(
                    "Can not define data for existing %s object" % \
                    item.__class__.__name__
                )
            return item

registry.register(Group)
