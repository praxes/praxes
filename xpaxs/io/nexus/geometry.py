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

from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Geometry(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXgeometry'

registry.register(Geometry)


class Translation(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXtranslation'

registry.register(Translation)


class Shape(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXshape'

registry.register(Shape)


class Orientation(Group):

    """
    """

    @property
    def nx_class(self):
        return 'NXorientation'

registry.register(Orientation)
