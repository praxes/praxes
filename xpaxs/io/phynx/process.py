"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Process(Group):

    """
    """

    nx_class = 'NXprocess'

registry.register(Process)
