"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Entry(Group):

    """
    """

    nx_class = 'NXentry'

    def _get_npoints(self):
        with self._lock:
            # TODO: use h5py get() when available
            try:
                return int(self.attrs['npoints'])
            except h5py.H5Error:
                return 0
    def _set_npoints(self, np):
        def func(name, obj):
            obj.attrs['npoints'] = np

        self.visititems(func)
    npoints = property(_get_npoints, _set_npoints)

registry.register(Entry)
