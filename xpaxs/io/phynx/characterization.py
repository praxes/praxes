"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Characterization(Group):

    """
    """

    nx_class = 'NXcharacterization'

registry.register(Characterization)
