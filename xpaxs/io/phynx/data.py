"""
"""

from __future__ import absolute_import, with_statement

from .group import Group
from .registry import registry


class Data(Group):

    """
    """

    nx_class = 'NXdata'

registry.register(Data)


class EventData(Group):

    """
    """

    nx_class = 'NXevent_data'

registry.register(EventData)


class Monitor(Group):

    """
    """

    nx_class = 'NXmonitor'

registry.register(Monitor)
