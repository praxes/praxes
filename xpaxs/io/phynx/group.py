"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from posixpath import basename

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

try:
    from enthought.traits.api import HasTraits
except ImportError:
    class HasTraits(object):
        pass
import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import Axis, Dataset, Signal
from .registry import registry


#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Group(h5py.Group, HasTraits):

    def __init__(self, parent_object, name, **data):
        """
        If data is not specified, return an existing group or raise an error.

        Otherwise, data must be a python dictionary. hdf5 attributes can be
        identified by::

            data={'attrs': {'foo':1, 'bar':2}}

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

                for attr in [
                    'entry_shape', 'file_name', 'entry_name', 'npoints'
                ]:
                    try:
                        self.attrs[attr] = parent_object.attrs[attr]
                    except h5py.H5Error:
                        pass

            if data:
                for attr, val in data.pop('attrs', {}).iteritems():
                    self.attrs[attr] = val

                for name, val in data.iteritems():
                    gtype, val = val
                    registry[gtype](self, name, **val)

    def __repr__(self):
        with self._lock:
            try:
                return '<%s group "%s" (%d members, %d attrs)>' % (
                    self.__class__.__name__,
                    self.name,
                    len(self),
                    len(self.attrs)
                )
            except Exception:
                return "<Closed %s group>" % self.__class__.__name__

    def __getitem__(self, name):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)

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

    def __setitem__(self, name, value):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)
            super(Group, self).__setitem__(name, value)

    @property
    def children(self):
        return self.listobjects()

    @property
    def name(self):
        return basename(super(Group, self).name)

    @property
    def path(self):
        return super(Group, self).name

    @property
    def signals(self):
        with self._lock:
            return sorted(
                [s for s in self.iterobjects() if isinstance(s, Signal)]
            )

    @property
    def signal_names(self):
        with self._lock:
            return [s.name for s in self.signals]

    @property
    def axes(self):
        with self._lock:
            return sorted(
                [a for a in self.iterobjects() if isinstance(a, Axis)]
            )

    @property
    def axis_names(self):
        with self._lock:
            return [a.name for a in self.axes]

    def get_axes(self, direction=1):
        with self._lock:
            return [a for a in self.axes if a.axis==direction]

    def create_dataset(self, name, *args, **kwargs):
        type = kwargs.pop('type', 'Dataset')
        return registry[type](self, name, *args, **kwargs)

    def require_dataset(self, name, *args, **kwargs):
        with self._lock:
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

    def require_group(self, name, type='Group', **data):
        with self._lock:
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
