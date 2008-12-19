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

from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Data(Group):

    """
    """

    nx_class = 'NXdata'

registry.register(Data)


class Event_data(Group):

    """
    """

    nx_class = 'NXevent_data'

registry.register(Event_data)


class Monitor(Group):

    """
    """

    nx_class = 'NXmonitor'

registry.register(Monitor)
