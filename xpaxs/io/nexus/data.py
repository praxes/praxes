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

registry.register(Data, 'NXdata')


class Event_data(Group):

    """
    """

registry.register(Event_data, 'NXevent_data')


class Monitor(Group):

    """
    """

registry.register(Monitor, 'NXmonitor')
