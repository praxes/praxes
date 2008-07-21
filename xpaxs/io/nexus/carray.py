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

from .array import NXarray
from .registry import class_name_dict

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXcarray(NXarray):

    """
    """

    def _create_entry(self, where, name, *args, **kwargs):
        self.nx_file.create_h5carray(where, name, *args, **kwargs)

class_name_dict['NXcarray'] = NXcarray
