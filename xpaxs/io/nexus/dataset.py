"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from h5py import Dataset

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXdataset(Dataset):

    """
    """

    def __init__(self, parent_object, name, *args, **kwargs):
        attrs = kwargs.pop('attrs', {})
        super(NXdataset, self).__init__(parent_object, name, *args, **kwargs)

        for key, val in attrs:
            self.attrs[key] = val

registry['NXdataset'] = NXdataset
