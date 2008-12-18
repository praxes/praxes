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

from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Environment(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXenvironment'

registry.register(Environment)


class Sensor(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXsensor'

registry.register(Sensor)
