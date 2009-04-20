"""
"""
from __future__ import absolute_import, with_statement

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
    def npoints(self):
        return self.attrs.get('npoints', 0)

    @property
    def plock(self):
        return self._plock

    @property
    def source_file(self):
        return self.attrs.get('source_file', self.file.name)

    def __init__(self, parent_object):
        with parent_object.plock:
            self._plock = parent_object.plock
            self._file = parent_object.file
            for attr in ['acquisition_shape', 'source_file', 'npoints']:
                if (attr not in self.attrs) and (attr in parent_object.attrs):
                    self.attrs[attr] = parent_object.attrs[attr]

    def __enter__(self):
        self.plock.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.plock.__exit__(type, value, traceback)
