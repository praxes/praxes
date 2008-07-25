"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import warnings

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import h5py.highlevel as h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class_name_dict = {}

def get_nxclass_by_name(class_name):
    """
    Get the node class matching the `class_name`.
    """
    if class_name not in class_name_dict:
        warnings.warn("there is no registered node class named `%s`, "
                      "defaulting to NXentry"% class_name)
        return class_name_dict['NXentry']

    return class_name_dict[class_name]

def get_nxclass_from_h5_item(h5_item):
    try:
        return get_nxclass_by_name(h5_item.attrs.NX_class)
    except AttributeError:
        if isinstance(h5_item, h5py.Dataset):
            return get_nxclass_by_name('NXdataset')
        elif isinstance(h5_item, h5py.Group):
            return get_nxclass_by_name('NXentry')
        else:
            raise AttributeError('Unrecognized "%s" object')
