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


class NXinstrument(NXgroup):

    """
    """

    def create_component(self, name, component, **data):
        return registry[component](self, name, **data)

    def require_component(self, name, component, **data):
        if not name in self:
            return self.create_component(name, component, **data)
        else:
            item = self[name]
            if not isinstance(item, registry[component]):
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

registry['NXinstrument'] = NXinstrument
