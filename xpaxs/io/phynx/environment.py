"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class Environment(Group):

    """
    """

    nx_class = 'NXenvironment'

registry.register(Environment)


class Sensor(Group):

    """
    """

    nx_class = 'NXsensor'

registry.register(Sensor)
