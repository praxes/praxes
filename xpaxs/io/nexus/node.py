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
        with parent._v_lock:
            super(NXnode, self).__init__(parent)

            # __setattr__ assumes all attributes of the instance
            # are also hdf5 attributes, so we need to bypass it:
            self.__dict__['_v_parent'] = parent
            self.__dict__['_v_lock'] = parent._v_lock
            self.__dict__['_v_file'] = parent._v_file

            self.__dict__['_v_h5Node'] = h5node
            self.__dict__['_v_pathname'] = h5node._v_pathname

            self.name = h5node._v_name

    def __contains__(self, name):
        with self._v_lock:
            return name in self.__members__ or name in self.__dict__

    def __getattr__(self, name):
        with self._v_lock:
            try:
                return self.__dict__[name]
            except KeyError:
                return getattr(self._v_h5Node._v_attrs, name)

    def __iter__(self):
        with self._v_lock:
            return self._v_h5Node._f_iterNodes()

    # support readline-style tab completion, even for attributes
    @property
    def __members__(self):
        return self._v_attrs

    def __setattr__(self, name, value):
        with self._v_lock:
            if name in self.__dict__:
                raise AttributeError("can't set attribute")
            if isinstance(value, NXnode):
                super(NXnode, self).__setattr__(name, value)
            else:
                setattr(self._v_h5Node._v_attrs, name, value)
                self.__members__.insert(0, name)

    def __str__(self):
        with self._v_lock:
            pathname = self._v_pathname
            classname = self.__class__.__name__
        return "%s (%s)" % (pathname, classname)

    def _f_flush(self):
        with self._v_lock:
            self._v_file.flush()

    def _f_remove(self):
        with self._v_lock:
            self._v_parent.__dict__.pop(self.name)
            self._v_h5Node._g_remove(True)

    @property
    def _v_attrs(self):
        with self._v_lock:
            return self._v_h5Node._v_attrs._f_list()

