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

from h5py import Dataset, Group

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import NXdataset
from .registry import registry


#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXgroup(Group):

    def __init__(self, parent_object, name, **data):
        """
        If data is None, return an existing group or raise an error.

        Otherwise, data must be a python dictionary. hdf5 attributes
        can be identified by::

            data={'attrs': {'foo':1, 'bar':2}}

        """
        with parent_object._lock:
            if name in parent_object:
                super(NXgroup, self).__init__(
                    parent_object, name, create=False
                )
                if self.__class__.__name__ != 'NXgroup':
                    # NXgroup is not a valid nexus class
                    self.attrs['NX_class'] = self.__class__.__name__
            else:
                super(NXgroup, self).__init__(
                    parent_object, name, create=True
                )

            if data:
                for attr, val in data.pop('attrs', {}).iteritems():
                    self.attrs[attr] = val

                for name, val in data.iteritems():
                    nxtype, val = val
                    registry[nxtype](self, name, **val)

    def __getitem__(self, name):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)

            # TODO: would be better to check the attribute without having to
            # create create the group twice. This might be possible with the
            # 1.8 API.
            item = super(NXgroup, self).__getitem__(name)
            if isinstance(item, Dataset):
                return NXdataset(self, name)
            else:
                if 'NX_class' in item.attrs:
                    return registry[item.attrs['NX_class']](self, name)
                else:
                    return NXgroup(self, name)

    def __setitem__(self, name, value):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)
            super(NXgroup, self).__setitem__(name, value)

    def create_dataset(self, name, **data):
        with self._lock:
            return self.create_nx(name, 'NXdataset', **data)

    def require_dataset(self, name, *args, **kwargs):
        with self._lock:
            return self.require_nx(name, 'NXdataset', **data)

    def create_group(self, name, **data):
        with self._lock:
            return self.create_nx(name, 'NXgroup', **data)

    def require_group(self, name, **data):
        with self._lock:
            return self.require_nx(name, 'NXgroup', **data)

    def create_nx(self, name, nxtype, **data):
        if not nxtype.startswith('NX'): nxtype = 'NX'+nxtype
        return registry[nxtype](self, name, **data)

    def require_nx(self, name, nxtype, **data):
        if not name in self:
            return self.create(name, nxtype, **data)
        else:
            if not nxtype.startswith('NX'): nxtype = 'NX'+nxtype
            item = self[name]
            if not isinstance(item, registry[nxtype]):
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

registry['NXgroup'] = NXgroup
