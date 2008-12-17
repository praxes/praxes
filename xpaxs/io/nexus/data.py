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

from .dataset import Axis, Signal
from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Data(Group):

    """
    """

    @property
    def signals(self):
        with self._lock:
            return sorted(
                [s for s in self.iterobjects() if isinstance(s, Signal)]
            )

    @property
    def signal_names(self):
        with self._lock:
            return sorted(
                [s.name for s in self.iterobjects() if isinstance(s, Signal)]
            )

    @property
    def axes(self):
        with self._lock:
            return sorted(
                [a for a in self.iterobjects() if isinstance(a, Axis)]
            )

    @property
    def axes_names(self):
        with self._lock:
            return sorted(
                [a.name for a in self.iterobjects() if isinstance(a, Axis)]
            )

    def get_axes(self, direction=1):
        with self._lock:
            return [a for a in self.axes if a.axis==direction]

registry.register(Data, 'NXdata')


class Event_data(Group):

    """
    """

registry.register(Event_data, 'NXevent_data')


class Monitor(Group):

    """
    """

registry.register(Monitor, 'NXmonitor')
