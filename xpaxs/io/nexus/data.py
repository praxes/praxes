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

from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Data(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXdata'

registry.register(Data)


class Event_data(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXevent_data'

registry.register(Event_data)


class Monitor(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXmonitor'

registry.register(Monitor)
