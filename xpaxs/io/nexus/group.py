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

from h5py import Group

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import NXdataset
from .registry import registry


#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXgroup(Group):

    """
    """

    def __init__(self, parent_object, name, data=None):
        """
        If data is None, return an existing group or raise an error.

        Otherwise, data must be a python dictionary. hdf5 attributes
        can be identified by::

            data={'attrs': {'foo':1, 'bar':2}}

        """
        with parent_object._lock:
            if name in parent_object:
                Group(self, parent_object, name, create=False)
            else:
                Group(self, parent_object, name, create=True)

            self.update(data)

    def update(self, data):
        with self._lock:
            for attr, val in kwargs.pop(attrs, {}):
                self.attrs[attr] = val

            for key, val in data:
                nxclassName, nxdata = val
                if nxclassName == 'Dataset':
                    NXdataset(self, key, nxdata)
                else:
                    nxclass = registry[nxclassName]
                    nxclass(self, key, nxdata)

    def __getitem__(self, name):
        with self._lock:
            # would be better to check the attribute without creating the
            # Group:
            item = super(NXfile, self).__getitem__(name)
            if isinstance(item, Dataset):
                nxclass = NXdataset
            else:
                nxclass = registry[item.attrs['NX_class']]
            del item

            return nxclass(self, name)

    def create_log(self, name, data=None):
        return registry['NXlog'](self, name, data)

    def require_log(self, name, data=None):
        if not name in self:
            return self.create_log(name, data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXlog']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_note(self, name, data=None):
        return registry['NXNote'](self, name, data)

    def require_note(self, name, data=None):
        if not name in self:
            return self.create_note(name, data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXnote']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_beam(self, name, data=None):
        return registry['NXbeam'](self, name, data)

    def require_beam(self, name, data=None):
        if not name in self:
            return self.create_beam(name, data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXbeam']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_geometry(self, name, data=None):
        return registry['NXgeometry'](self, name, data)

    def require_geometry(self, name, data=None):
        if not name in self:
            return self.create_geometry(name, data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXgeometry']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_environment(self, name, data=None):
        return registry['NXenvironment'](self, name, data)

    def require_environment(self, name, data=None):
        if not name in self:
            return self.create_environment(name, data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXenvironment']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item
