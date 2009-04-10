"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry
from .utils import sync


class Entry(Group):

    """
    """

    nx_class = 'NXentry'

    @property
    def entry(self):
        return self

    @property
    @sync
    def measurement(self):
        measurements = [
            i for i in self.iterobjects()
            if isinstance(i, registry['Measurement'])
        ]
        nm = len(measurements)
        if nm == 1:
            return measurements[0]
        if nm == 0:
            return None
        else:
            raise ValueError(
                'There should be one Measurement group per entry, found %d' % nm
            )

    def _get_npoints(self):
        return self.attrs.get('npoints', 0)
    @sync
    def _set_npoints(self, np):
        def func(name, obj):
            obj.attrs['npoints'] = np
        self.visititems(func)
    npoints = property(_get_npoints, _set_npoints)

registry.register(Entry)
