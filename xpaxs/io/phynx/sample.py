"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Sample(Group):

    """
    """

    nx_class = 'NXsample'

registry.register(Sample)
