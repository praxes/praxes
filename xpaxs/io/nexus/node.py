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

import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXnode(object):

    """
    """

    def __init__(self, parent, h5node, *args, **kwargs):

        """
        """
        # Adding the names of visible children nodes here
        # allows readline-style completion to work on them
        # although they are actually not attributes of this object.
        # This must be the *very first* assignment and it must bypass
        # ``__setattr()__`` to let the later work from this moment on.
        with parent._v_lock:
            self.__dict__['__members__'] = []
            super(NXnode, self).__init__(parent)

            self.__dict__['_v_parent'] = parent
            self.__dict__['_v_lock'] = parent._v_lock
            self.__dict__['_v_file'] = parent._v_file

            self.__dict__['_v_h5Node'] = h5node
            self.__dict__['_v_pathname'] = h5node._v_pathname
            self.__members__.extend(h5node._v_attrs._v_attrnamesuser)

    def __getattr__(self, name):
        with self._v_lock:
            try:
                return self.__dict__[name]
            except KeyError:
                return getattr(self._v_h5Node._v_attrs, name)

    def __iter__(self):
        with self._v_lock:
            return self._v_h5Node._f_iterNodes()

    def __repr__(self):
        with self._v_lock:
            return self._v_h5Node.__repr__()

    def __setattr__(self, name, value):
        if '__members__' in self.__dict__ and name in self.__members__:
            warnings.warn(
                "group ``%s`` already has a child node or "
                "attribute named ``%s``; you will not be able"
                " to use natural naming to access the child node"
                % (self._v_pathname, name), tables.NaturalNameWarning)
        with self._v_lock:
            if isinstance(value, NXnode):
                super(NXnode, self).__setattr__(name, value)
            else:
                setattr(self._v_h5Node._v_attrs, name, value)
                self.__members__.insert(0, name)

    def __str__(self):
        with self._v_lock:
            return self._v_h5Node.__str__()

    def _f_flush(self):
        with self._v_lock:
            self._v_file.flush()
