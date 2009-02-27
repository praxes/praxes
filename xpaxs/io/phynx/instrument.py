"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Instrument(Group):

    """
    """

    nx_class = 'NXinstrument'

registry.register(Instrument)
