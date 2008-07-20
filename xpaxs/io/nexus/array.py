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

from xpaxs.io.nexus.leaf import NXleaf
from xpaxs.io.nexus.registry import class_name_dict

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXarray(NXleaf):

    """
    """

    def __getitem__(self, key):
        try:
            self.mutex.lock()
            return self.__h5Node.__getitem__(key)
        finally:
            self.mutex.unlock()

    def __iter__(self):
        try:
            self.mutex.lock()
            return self.__h5Node.__iter__()
        finally:
            self.mutex.unlock()

    def __setitem__(self, key, value):
        try:
            self.mutex.lock()
            self.__h5Node.__getitem__(key, value)
        finally:
            self.mutex.unlock()

    def _create_entry(self, where, name, *args, **kwargs):
        self.nxFile.create_h5array(where, name, *args, **kwargs)

class_name_dict['NXarray'] = NXarray
