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



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .group import NXgroup
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

# sample user

class NXentry(NXgroup):

    """
    """

    def create_characterization(self, name, **data):
        return registry['NXcharacterization'](self, name, **data)

    def require_characterization(self, name, **data):
        if not name in self:
            return self.create_characterization(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXcharacterization']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_data(self, name, **data):
        return registry['NXdata'](self, name, **data)

    def require_data(self, name, **data):
        if not name in self:
            return self.create_data(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXdata']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_event_data(self, name, **data):
        return registry['NXevent_data'](self, name, **data)

    def require_event_data(self, name, **data):
        if not name in self:
            return self.create_event_data(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXevent_data']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_instrument(self, name, **data):
        return registry['NXinstrument'](self, name, **data)

    def require_instrument(self, name, **data):
        if not name in self:
            return self.create_instrument(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXinstrument']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_monitor(self, name, **data):
        return registry['NXmonitor'](self, name, **data)

    def require_monitor(self, name, **data):
        if not name in self:
            return self.create_monitor(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXmonitor']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_process(self, name, **data):
        return registry['NXprocess'](self, name, **data)

    def require_process(self, name, **data):
        if not name in self:
            return self.create_process(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXprocess']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_sample(self, name, **data):
        return registry['NXsample'](self, name, **data)

    def require_sample(self, name, **data):
        if not name in self:
            return self.create_sample(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXsample']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

    def create_user(self, name, **data):
        return registry['NXuser'](self, name, **data)

    def require_user(self, name, **data):
        if not name in self:
            return self.create_user(name, **data)
        else:
            item = self[name]
            if not isinstance(item, registry['NXuser']):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

registry['NXentry'] = NXentry
