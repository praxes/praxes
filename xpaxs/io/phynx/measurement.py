"""
"""

from __future__ import absolute_import

import posixpath

from .group import Group
from .registry import registry
from .utils import sync


class Measurement(Group):

    """
    A group to contain all the information reported by the measurement. This
    group provides a link between standard tabular data formats (like spec)
    and the emerging hierarchical NeXus format.
    """

    @property
    @sync
    def mcas(self):
        return dict([
            (posixpath.split(a.name)[-1], a) for a in self.iterobjects()
            if isinstance(a, registry['MultiChannelAnalyzer'])
        ])

    @property
    @sync
    def positioners(self):
        targets = [
            i for i in self.iterobjects() if isinstance(i, Positioners)
        ]
        nt = len(targets)
        if nt == 1:
            return targets[0]
        if nt == 0:
            return None
        else:
            raise ValueError(
                'There should be one Positioners group per entry, found %d' % nm
            )

    @property
    @sync
    def scalar_data(self):
        targets = [
            i for i in self.iterobjects() if isinstance(i, ScalarData)
        ]
        nt = len(targets)
        if nt == 1:
            return targets[0]
        if nt == 0:
            return None
        else:
            raise ValueError(
                'There should be one ScalarData group per entry, found %d' % nm
            )

registry.register(Measurement)


class ScalarData(Group):

    """
    A group containing all the scanned scalar data in the measurement,
    including:

    * positions of motors or other axes
    * counters
    * timers
    * single channel analyzers
    * etc.

    """

    @property
    @sync
    def monitor(self):
        id = self.attrs.get('monitor', None)
        if id is not None:
            return self[id]

registry.register(ScalarData)


class Positioners(Group):

    """
    A group containing the reference positions of the various axes in the
    measurement.
    """

registry.register(Positioners)
