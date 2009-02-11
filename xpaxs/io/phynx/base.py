
from __future__ import with_statement

import re
from distutils import version

import h5py


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

    @property
    def id(self):
        return self._id

    @property
    def idstring(self):
        return self._idstring

    def __str__(self):
        return self.idstring

    def __repr__(self):
        return "AcquisitionID('%s')" % str(self)

    def __cmp__(self, other):
        if isinstance(other, str):
            other = AcquisitionID(other)

        return cmp(self.id, other.id)


class _PhynxProperties:

    """A mix-in class to propagate attributes from the parent object to
    the new HDF5 group or dataset, and to expose those attributes via
    python properties.
    """

    def __init__(self, parent_object):
        for attr in [
            'acquisition_shape', 'file_name', 'acquisition_name',
            'acquisition_id', 'npoints', 'format_version'
        ]:
            try:
                self.attrs[attr] = parent_object.attrs[attr]
            except h5py.H5Error:
                pass

    @property
    def format_version(self):
        return version.LooseVersion(self.attrs.get('format_version', '0.0'))

    @property
    def acquisition_shape(self):
        temp = self.attrs.get('acquisition_shape', '()').lstrip('(').rstrip(')')
        return tuple(int(i) for i in temp.split(',') if i) if temp else tuple()

    @property
    def acquisition_id(self):
        return AcquisitionID(self.attrs.get('acquisition_id', '0'))

    @property
    def acquisition_command(self):
        return self.attrs.get('acquisition_command', '')

    @property
    def file_name(self):
        return self.attrs.get('file_name', '')

    @property
    def npoints(self):
        return self.attrs.get('npoints', 0)
