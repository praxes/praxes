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


class _BaseGroup(Group):

    def __init__(self, parent_object, name):
        """
        If data is None, return an existing group or raise an error.

        Otherwise, data must be a python dictionary. hdf5 attributes
        can be identified by::

            data={'attrs': {'foo':1, 'bar':2}}

        """
        with parent_object._lock:
            if name in parent_object:
                super(_BaseGroup, self).__init__(
                    parent_object, name, create=False
                )
                if self.__class__.__name__ != 'NXgroup':
                    # NXgroup is not a valid nexus class
                    self.attrs['NX_class'] = self.__class__.__name__
            else:
                super(_BaseGroup, self).__init__(
                    parent_object, name, create=True
                )

    def __getitem__(self, name):
        with self._lock:
            # lets allow integer and floats as keys:
            if isinstance(name, (int, float)): name = str(name)

            # TODO: would be better to check the attribute without having to
            # create create the group twice. This might be possible with the
            # 1.8 API.
            item = super(_BaseGroup, self).__getitem__(name)
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
            super(_BaseGroup, self).__setitem__(name, value)

    def create_log(self, name, **data):
        return registry['NXlog'](self, name, **data)

    def require_log(self, name, **data):
        if not name in self:
            return self.create_log(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXlog']):
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

    def create_note(self, name, **data):
        return registry['NXNote'](self, name, **data)

    def require_note(self, name, **data):
        if not name in self:
            return self.create_note(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXnote']):
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


class NXgroup(_BaseGroup):

    """
    NXgroup is not a valid NeXus class, we use it as a base class and default
    group when the NeXus class cannot be determined.
    """

    def __init__(self, parent_object, name, **data):
        """
        If data is None, return an existing group or raise an error.

        Otherwise, data must be a python dictionary. hdf5 attributes
        can be identified by::

            data={'attrs': {'foo':1, 'bar':2}}

        """
        super(NXgroup, self).__init__(parent_object, name)

        with parent_object._lock:
            if data:
                for attr, val in data.pop('attrs', {}).iteritems():
                    self.attrs[attr] = val

                for name, val in data.iteritems():
                    nxtype, val = val
                    registry[nxtype](self, name, **val)

    def create_beam(self, name, **data):
        return registry['NXbeam'](self, name, **data)

    def require_beam(self, name, **data):
        if not name in self:
            return self.create_beam(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXbeam']):
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

    def create_data(self, name, **data):
        return registry['NXdata'](self, name, **data)

    def require_data(self, name, **data):
        if not name in self:
            return self.create_data(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXdata']):
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

    def create_environment(self, name, **data):
        return registry['NXenvironment'](self, name, **data)

    def require_environment(self, name, **data):
        if not name in self:
            return self.create_environment(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXenvironment']):
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

    def create_geometry(self, name, **data):
        return registry['NXgeometry'](self, name, **data)

    def require_geometry(self, name, **data):
        if not name in self:
            return self.create_geometry(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXgeometry']):
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
