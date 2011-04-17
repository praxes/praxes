"""
"""

from __future__ import absolute_import

from collections import OrderedDict
import copy
import posixpath

import numpy as np

from .group import Group
from .registry import registry
from .utils import memoize, simple_eval, sync


class Measurement(Group):

    """
    A group to contain all the information reported by the measurement. This
    group provides a link between standard tabular data formats (like spec)
    and the emerging hierarchical NeXus format.
    """

    @property
    @sync
    def acquired(self):
        try:
            return self.attrs.get['acquired']
        except:
            return self.entry.npoints
    @acquired.setter
    @sync
    def acquired(self, value):
        self.attrs['acquired'] = int(value)

    @property
    @memoize
    def masked(self):
        return MaskedProxy(self)

    @property
    @sync
    def mcas(self):
        return dict([
            (posixpath.split(a.name)[-1], a) for a in self.values()
            if isinstance(a, registry['MultiChannelAnalyzer'])
        ])

    @property
    @memoize
    @sync
    def positioners(self):
        targets = [
            i for i in self.values() if isinstance(i, Positioners)
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
            # would like to use json.loads here:
            config = simple_eval(self.attrs.get('pymca_config', '{}'))
            self._pymca_config = ConfigDict(config)
            return copy.deepcopy(self._pymca_config)
    @pymca_config.setter
    @sync
    def pymca_config(self, config):
        self._pymca_config = copy.deepcopy(config)
        # would like to use json.dumps here:
        self.attrs['pymca_config'] = str(config)

    @property
    @memoize
    @sync
    def scalar_data(self):
        targets = [
            i for i in self.values() if isinstance(i, ScalarData)
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

    @sync
    def update(self, **kwargs):
        with self:
            i = kwargs['scalar_data/i']
            for k, val in kwargs.items():
                try:
                    self[k][i] = val
                except ValueError:
                    self[k].resize(i+1, axis=0)
                    self[k][i] = val
            self.acquired = i+1


class HasSignals(object):

    @property
    @sync
    def signals(self):
        from .dataset import Signal
        return OrderedDict(
            (posixpath.basename(j.name), j)
            for j in sorted(i for i in self.values() if isinstance(i, Signal))
            )


class HasAxes(object):

    @property
    @sync
    def axes(self):
        from .dataset import Axis
        return OrderedDict(
            (posixpath.basename(j.name), j)
            for j in sorted(i for i in self.values() if isinstance(i, Axis))
            )


class HasMonitor(object):

    @property
    @sync
    def monitor(self):
        id = self.attrs.get('monitor', None)
        if id is not None:
            return self[id]


class ScalarData(Group, HasAxes, HasMonitor, HasSignals):

    """
    A group containing all the scanned scalar data in the measurement,
    including:

    * positions of motors or other axes
    * counters
    * timers
    * single channel analyzers
    * etc.

    """


class Positioners(Group):

    """
    A group containing the reference positions of the various axes in the
    measurement.
    """



class MaskedProxy(object):

    @property
    def masked(self):
        return self

    def __init__(self, measurement):
        self._measurement = measurement

    def __getitem__(self, args):
        try:
            return self._measurement.scalar_data['masked'].__getitem__(args)
        except KeyError:
            if isinstance(args, int):
                return False
            temp = np.zeros(self._measurement.entry.npoints, '?')
            return temp.__getitem__(args)
