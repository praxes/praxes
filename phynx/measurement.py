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
    def acquired(self):
        return self.attrs.get('acquired', self.npoints)
    @acquired.setter
    @sync
    def acquired(self, value):
        self.attrs['acquired'] = int(value)

    @property
    def masked(self):
        return MaskedProxy(self)

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
    def pymca_config(self):
        try:
            return self._pymca_config
        except AttributeError:
            from PyMca.ConfigDict import ConfigDict
            config = self.attrs.get('pymca_config', '{}')
            self._pymca_config = ConfigDict(simple_eval(config))
            return copy.deepcopy(self._pymca_config)
    @pymca_config.setter
    @sync
    def _set_pymca_config(self, config):
        self._pymca_config = copy.deepcopy(config)
        self.attrs['pymca_config'] = str(config)

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


class Positioners(Group):

    """
    A group containing the reference positions of the various axes in the
    measurement.
    """



class MaskedProxy(object):

    @property
    def acquired(self):
        return self._measurement.acquired

    @property
    def masked(self):
        return self

    @property
    def npoints(self):
        return self._measurement.npoints

    @property
    def plock(self):
        return self._measurement.plock

    def __init__(self, measurement):
        self._measurement = measurement

    @sync
    def __getitem__(self, args):
        try:
            return self._measurement.scalar_data['masked'].__getitem__(args)
        except H5Error:
            if isinstance(args, int):
                return False
            return np.zeros(self._measurement.npoints, '?').__getitem__(args)
