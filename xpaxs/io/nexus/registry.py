"""
Wrappers around the pytables interface to the hdf5 file.

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import warnings

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore
import tables

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

    return class_name_dict[class_name]

def get_nxclass_from_h5_item(h5_item):
    try:
        class_name = h5_item._v_attrs.NX_class
    except AttributeError:
        if isinstance(h5_item, tables.table.Table):
            warnings.warn('PyTables.Table object "%s" incompatible with '
            'NeXus API')
        if isinstance(h5_item, tables.leaf.Leaf):
            class_name = 'NX_' + h5_item.__class__.__name__.lower()
    return get_nxclass_by_name(class_name)
