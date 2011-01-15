"""
"""

from __future__ import absolute_import, with_statement

from .group import Group


class Data(Group):

    """
    """

    nx_class = 'NXdata'


class EventData(Group):

    """
    """

    nx_class = 'NXevent_data'


class Monitor(Group):

    """
    """

    nx_class = 'NXmonitor'
