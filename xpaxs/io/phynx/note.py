"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Note(Group):

    """
    """

    nx_class = 'NXnote'

registry.register(Note)
