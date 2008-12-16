"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Dataset(h5py.Dataset):

    """
    """

    def __init__(self, parent_object, name, *args, **kwargs):
        with parent_object._lock:
            attrs = kwargs.pop('attrs', {})
            super(Dataset, self).__init__(parent_object, name, *args, **kwargs)

            for key, val in attrs:
                self.attrs[key] = val

registry.register(Dataset)
