"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Beam(Group):

    """
    """

    nx_class = 'NXbeam'

registry.register(Beam)
