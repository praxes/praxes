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

from .registry import class_name_dict

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXnode(object):

    """
    """

    _protected = ('name',)

    def __init__(self, parent, name, *args, **kwargs):

        """
        """
        super(NXnode, self).__init__(parent)

        with parent._v_lock:

            # __setattr__ assumes all attributes of the instance
            # are also hdf5 attributes, so we need to bypass it:
            self.__dict__['_v_name'] = name
            self.__dict__['_v_parent'] = parent
            self.__dict__['_v_lock'] = parent._v_lock
            self.__dict__['_v_file'] = parent._v_file

            try:
                node = self._v_file.getH5Node(parent._v_pathname, name)
                self.__dict__['_v_h5Node'] = node
            except AttributeError:
                node = self._v_file.getH5Node(name)
                self.__dict__['_v_h5Node'] = node
            except tables.NoSuchNodeError:
                node = self._createH5Node()
                self.__dict__['_v_h5Node'] = node
                self.name = self._v_name
                self.NX_class = self.__class__.__name__
                self._initializeNewEntry()

    def _createH5Node(self):
        raise NotImplementedError

    def _initializeNewData(self):
        pass

    def __contains__(self, name):
        with self._v_lock:
            return name in self.__members__ or name in self.__dict__

    def __delattr__(self, name):
        with self._v_lock:
            if name in self._v_attrs:
                if name in self._protected:
                    raise AttributeError('%s can not be deleted'%name)
                self._v_h5Node._v_attrs.__delattr__(name)
            else:
                child = self.__dict__[name]
                if isinstance(child, NXnode):
                    child._f_remove()
                else:
                    raise AttributeError('%s can not be deleted'%name)

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
            elif isinstance(value, tables.Node):
                raise AttributeError("can't set an attribute to a value "
                                     "of type %s" %type(value))
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

    def _f_move(self, newparent=None, newname=None, overwrite=False):
        with self._v_lock:
            if newparent is None and newname is None:
                return
            if newname is None:
                newname = self.name
            if newparent is None:
                newparent = self._v_parent
            else:
                assert isinstance(newparent, class_name_dict['NXentry'])
            if newname in newparent and not overwrite:
                raise AttributeError('%s already exists.'
                'Set "overwrite=True" or choose another name.')
            else:
                self._v_h5Node._f_move(newparent._v_pathname, newname,
                                       overwrite=True)
                self._v_parent.__dict__.pop(self.name)
                self.name = newname
                self.__dict__['_v_name'] = newname
                setattr(newparent, newname, self)

    def _f_remove(self):
        with self._v_lock:
            self._v_parent.__dict__.pop(self.name)
            self._v_h5Node._g_remove(True)

    @property
    def _v_attrs(self):
        with self._v_lock:
            return self._v_h5Node._v_attrs._f_list()

    @property
    def name(self):
        with self._v_lock:
            try:
                return self.name
            except AttributeError:
                return self._v_name

    @property
    def _v_pathname(self):
        with self._v_lock:
            return self._v_h5Node._v_pathname

