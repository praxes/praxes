"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Log(Group):

    """
    """

    nx_class = 'NXlog'

registry.register(Log)
