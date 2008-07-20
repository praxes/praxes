"""
Wrappers around the pytables interface to the hdf5 file.

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.io.nexus.array import NXarray
from xpaxs.io.nexus.registry import class_name_dict

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXcarray(NXarray):

    """
    """

    def _create_entry(self, where, name, *args, **kwargs):
        self.nxFile.create_h5carray(where, name, *args, **kwargs)

class_name_dict['NXcarray'] = NXcarray
