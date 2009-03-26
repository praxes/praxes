"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry
from .utils import simple_eval


class Detector(Group):

    """
    """

    nx_class = 'NXdetector'

    @property
    def device_id(self):
        return self.attrs.get('id', self.name)

registry.register(Detector)


class LinearDetector(Detector):

    """
    """

    @property
    def pixels(self):
        return self['counts'].shape[-1:]

registry.register(LinearDetector)


class AreaDetector(Detector):

    """
    """

    @property
    def pixels(self):
        return self['counts'].shape[-2:]

registry.register(AreaDetector)


class Mar345(AreaDetector):

    """
    """

registry.register(Mar345)
