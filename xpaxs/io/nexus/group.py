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

    """
    NXgroup is not a valid NeXus class, we use it as a base class and default
    group when the NeXus class cannot be determined.
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
                super(NXgroup, self).__init__(parent_object, name, create=False)
                if self.__class__.__name__ != 'NXgroup':
                    # NXgroup is not a valid nexus class
                    self.attrs['NX_class'] = self.__class__.__name__
            else:
                super(NXgroup, self).__init__(parent_object, name, create=True)

            if data:
                self.update(data)

    def update(self, data):
        with self._lock:
            for attr, val in data.pop(attrs, {}):
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
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)

            # TODO: would be better to check the attribute without having to
            # create create the group twice. This might be possible with the
            # 1.8 API.
            item = super(NXgroup, self).__getitem__(name)
            if isinstance(item, Dataset):
                nxclass = NXdataset
            else:
                if 'NX_class' in item.attrs:
                    nxclass = registry[item.attrs['NX_class']]
                else:
                    nxclass = NXgroup
            del item

            return nxclass(self, name)

    def __setitem__(self, name, value):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)
            super(NXgroup, self).__setitem__(name, value)

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

registry['NXgroup'] = NXgroup
