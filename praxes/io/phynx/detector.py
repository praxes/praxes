"""
"""

from __future__ import absolute_import

import posixpath

from .group import Group


class Detector(Group):

    """
    """

    nx_class = 'NXdetector'

    @property
    def device_id(self):
        return self.attrs.get('id', posixpath.basename(self.name))


class LinearDetector(Detector):

    """
    """

    @property
    def pixels(self):
        return self['counts'].shape[-1:]


class AreaDetector(Detector):

    """
    """

    @property
    def pixels(self):
        return self['counts'].shape[-2:]

    @property
    def subexposures(self):
        return self.attrs.get('subexposures', 1)


class Mar345(AreaDetector):

    """
    """
