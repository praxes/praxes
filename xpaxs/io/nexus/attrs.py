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

        self.__lock = parent._v_lock

        self.__h5Node = attrs

    def __contains__(self, name):
        with self._v_lock:
            return name in self.__h5Node

    def __getattr__(self, name):
        with self._v_lock:
            return getattr(self.__h5Node, name)

    def __setattr__(self, name, value):
        if name.startswith('_'+self.__class__.__name__):
            super(NXattrs, self).__setattr__(name, value)
        else:
            with self._v_lock:
                setattr(self.__h5Node, name, value)

    def __iter__(self):
        with self._v_lock:
            names = self.__h5Node._v_attrnames
            for name in names:
                yield (name, getattr(self.__h5Node, name))

    def __repr__(self):
        with self._v_lock:
            return self.__h5Node.__repr__()

    def __str__(self):
        with self._v_lock:
            return self.__h5Node.__str__()

    _v_lock = property(lambda self: self.__lock)
