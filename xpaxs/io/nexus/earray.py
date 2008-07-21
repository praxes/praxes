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

from .carray import NXcarray
from .registry import class_name_dict

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXearray(NXcarray):

    """
    """

    def _create_entry(self, where, name, *args, **kwargs):
        self.nxFile.create_h5earray(where, name, *args, **kwargs)

class_name_dict['NXearray'] = NXearray
