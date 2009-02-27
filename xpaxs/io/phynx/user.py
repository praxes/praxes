"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class User(Group):

    """
    """

    nx_class = 'NXuser'

registry.register(User)
