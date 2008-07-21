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



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXattrs(object):

    """
    """

    def __init__(self, parent, attrs, *args, **kwargs):
        """
        """
        super(NXattrs, self).__init__(parent)
        self.__lock = parent.lock
        self.__h5Node = attrs

    def __getitem__(self, name):
        with self.lock:
            return getattr(self.__h5Node, name)

    def __setitem__(self, name, value):
        with self.lock:
            return setattr(self.__h5Node, name, value)

    def __iter__(self):
        with self.lock:
            print 1
            names = self.__h5Node._v_attrnames
            print names
            for name in names:
                print name
                print gettattr(self.__h5Node, name)
                yield gettattr(self.__h5Node, name)

    lock = property(lambda self: self.__lock)
