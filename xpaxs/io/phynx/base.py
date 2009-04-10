"""
"""
from __future__ import absolute_import, with_statement

import h5py
try:
    from enthought.traits.api import HasTraits_DISABLED
except ImportError:
    class HasTraits(object):
        pass

from .exceptions import H5Error
from .utils import simple_eval


class _PhynxProperties(HasTraits):

    """A mix-in class to propagate attributes from the parent object to
    the new HDF5 group or dataset, and to expose those attributes via
    python properties.
    """

    @property
    def acquisition_shape(self):
        return simple_eval(self.attrs.get('acquisition_shape', '()'))

    @property
    def file(self):
        return self._file

    @property
    def source_file(self):
        return self.attrs.get('source_file', self.file.name)

    @property
    def npoints(self):
        return self.attrs.get('npoints', 0)

    @property
    def plock(self):
        return self._plock

    def __init__(self, parent_object):
        for attr in ['acquisition_shape', 'source_file', 'npoints']:
            with parent_object.plock:
                self._plock = parent_object.plock
                self._file = parent_object.file
                if attr not in self.attrs:
                    try:
                        self.attrs[attr] = parent_object.attrs[attr]
                    except h5py.H5Error:
                        pass
