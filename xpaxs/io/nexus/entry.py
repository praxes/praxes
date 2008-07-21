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



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .node import NXnode
from .registry import class_name_dict

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXentry(NXnode):

    """
    """

    def _create_entry(self, where, name, *args, **kwargs):
        self.nx_file.create_h5group(where, name, *args, **kwargs)

class_name_dict['NXentry'] = NXentry
