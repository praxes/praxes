"""
"""

from __future__ import absolute_import

import re

from .group import Group
from .registry import registry
from .utils import sync


class AcquisitionID(object):

    """A class for comparing acquisition IDs copied from python's
    LooseVersion. Implements the standard interface for AcquisitionIDs.
    An ID number consists of a series of numbers, separated by either
    periods or strings of letters.  When comparing ID numbers, the
    numeric components will be compared numerically, and the alphabetic
    components lexically.  The following are all valid version numbers,
    in no particular order:

        1
        1.1
        1.5.1
        1.5.2b2
        161
        3.10a
        8.02
        3.4j
        1996.07.12
        3.2.pl0
        3.1.1.6
        2g6
        11g
        0.960923
        2.2beta29
        1.13++
        5.5.kw
        2.0b1pl0

    In fact, there is no such thing as an invalid version number under
    this scheme; the rules for comparison are simple and predictable,
    but may not always give the results you want (for some definition
    of "want").
    """

    component_re = re.compile(r'(\d+ | [a-z]+ | \.)', re.VERBOSE)

    @property
    def id(self):
        return self._id

    @property
    def idstring(self):
        return self._idstring

    def __init__(self, idstring):
        if not isinstance(idstring, str):
            idstring = str(idstring)
        try:
            assert idstring
        except:
            raise ValueError(" '%s' is not a valid ID"%idstring)
        if idstring:
            self.parse(idstring)

    def parse(self, idstring):
        # I've given up on thinking I can reconstruct the version string
        # from the parsed tuple -- so I just store the string here for
        # use by __str__
        self._idstring = idstring
        components = filter(lambda x: x and x != '.',
                            self.component_re.split(idstring))
        for i in range(len(components)):
            try:
                components[i] = int(components[i])
            except ValueError:
                pass

        self._id = components

    def __str__(self):
        return self.idstring

    def __repr__(self):
        return "AcquisitionID('%s')" % str(self)

    def __cmp__(self, other):
        if isinstance(other, str):
            other = AcquisitionID(other)

        return cmp(self.id, other.id)


class Entry(Group):

    """
    """

    nx_class = 'NXentry'

    @property
    def acquisition_command(self):
        return self.attrs.get('acquisition_command', '')

    @property
    def acquisition_id(self):
        return AcquisitionID(self.attrs.get('acquisition_id', '0'))

    @property
    def entry(self):
        return self

    @property
    @sync
    def measurement(self):
        measurements = [
            i for i in self.iterobjects()
            if isinstance(i, registry['Measurement'])
        ]
        nm = len(measurements)
        if nm == 1:
            return measurements[0]
        if nm == 0:
            return None
        else:
            raise ValueError(
                'There should be one Measurement group per entry, found %d' % nm
            )

    @sync
    def _get_npoints(self):
        return self.attrs.get('npoints', 0)
    @sync
    def _set_npoints(self, np):
        def func(name, obj):
            obj.attrs['npoints'] = np
            try:
                obj.resize(np, axis=0)
            except (AttributeError, TypeError):
                pass
        self.visititems(func)
    npoints = property(_get_npoints, _set_npoints)
