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
        return self.attrs.get('id', posixpath.split(self.name)[-1])


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


class Mar345(AreaDetector):

    """
    """
