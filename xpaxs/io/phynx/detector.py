"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Detector(Group):

    """
    """

    nx_class = 'NXdetector'

    @property
    def device_id(self):
        return self.attrs.get('id', self.name)

registry.register(Detector)
