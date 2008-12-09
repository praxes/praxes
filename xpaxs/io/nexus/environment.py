"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import

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


class NXenvironment(NXgroup):

    """
    """

    def create_sensor(self, name, data=None):
        return NXsensor(self, name, data)

    def require_log(self, name, data=None):
        if not name in self:
            return self.create_sensor(name, data)
        else:
            item = self[name]
            if not isinstance(item, NXsensor):
                raise NameError("Incompatible object (%s) already exists" % item.__class__.__name__)
            if data:
                item.update(data)
            return item

registry['NXenvironment'] = NXenvironment


class NXsensor(NXgroup):

    """
    """

registry['NXsensor'] = NXsensor
