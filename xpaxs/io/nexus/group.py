"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import Dataset
from .registry import registry


#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Group(h5py.Group):

    def __init__(self, parent_object, name, **data):
        """
        If data is None, return an existing group or raise an error.

        Otherwise, data must be a python dictionary. hdf5 attributes
        can be identified by::

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
                for attr in ['entry_shape', 'file_name', 'scan_number']:
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

    def __getitem__(self, name):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)

            # TODO: would be better to check the attribute without having to
            # create create the group twice. This might be possible with the
            # 1.8 API.
            item = super(Group, self).__getitem__(name)
            if isinstance(item, h5py.Dataset):
                return Dataset(self, name)
            else:
                if 'class' in item.attrs:
                    return registry[item.attrs['class']](self, name)
                elif 'NX_class' in item.attrs:
                    return registry[item.attrs['NX_class']](self, name)
                else:
                    return Group(self, name)

    def __setitem__(self, name, value):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)
            super(Group, self).__setitem__(name, value)

    def create_dataset(self, name, *args, **kwargs):
        return Dataset(self, name, *args, **kwargs)

    def require_dataset(self, name, *args, **kwargs):
        with self._lock:
            attrs = kwargs.pop('attrs', {})
            dset = super(Group, self).require_dataset(name, *args, **kwargs)
            for key, val in attrs:
                dset.attrs[key] = val
            return dset

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
