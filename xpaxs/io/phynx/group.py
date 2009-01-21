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
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .base import _PhynxProperties
from .dataset import Axis, Dataset, Signal
from .registry import registry


#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class AcquisitionIterator(object):

    def __init__(self, parent, dataset):
        self._currentIndex = 0
        self._parent = parent
        self._dataset = dataset

    def __iter__(self):
        return self

    @property
    def currentIndex(self):
        return self._currentIndex

    def next(self):
        if self._currentIndex >= self._dataset.npoints:
            raise StopIteration

        else:
            try:
                if self._parent.is_valid_index(self._currentIndex):
                    i = self._currentIndex
                    data = self._dataset[i]
                    try:
                        data /= self._parent.normalization[i]
                    except TypeError:
                        pass
                    self._currentIndex += 1

                    return i, data

                else:
                    self._currentIndex += 1
                    return self.next()

            except h5py.H5Error:
                raise IndexError


class Group(h5py.Group, _PhynxProperties, HasTraits):

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

                _PhynxProperties.__init__(self, parent_object)

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
        # used by traits
        return self.listobjects()

    @property
    def name(self):
        with self._lock:
            return basename(super(Group, self).name)

    @property
    def path(self):
        with self._lock:
            return super(Group, self).name

    @property
    def signals(self):
        with self._lock:
            return dict(
                [(s.name, s) for s in self.iterobjects()
                    if isinstance(s, Signal)]
            )

    @property
    def axes(self):
        with self._lock:
            return dict(
                [(a.name, a) for a in self.iterobjects() if isinstance(a, Axis)]
            )

    @property
    def valid_indices(self):
        indices = numpy.arange(len(self.axes.values()[0]))
        try:
            return indices[self['skipped'].value]
        except h5py.H5Error:
            return indices

    def get_sorted_axes_list(self, direction=1):
        with self._lock:
            return sorted([a for a in self.axes.values() if a.axis==direction])

    def get_sorted_signals_list(self, direction=1):
        with self._lock:
            return sorted([s for s in self.signals.values()])

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

    def is_valid_index(self, index):
        if 'skipped' in self:
            return not self['skipped'][index]
        else:
            return True

registry.register(Group)
