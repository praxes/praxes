"""
"""

from __future__ import absolute_import

from .group import Group


class Geometry(Group):

    """
    """

    nx_class = 'NXgeometry'


class Translation(Group):

    """
    """

    nx_class = 'NXtranslation'


class Shape(Group):

    """
    """

    nx_class = 'NXshape'


class Orientation(Group):

    """
    """

    nx_class = 'NXorientation'
