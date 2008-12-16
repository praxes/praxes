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

registry.register(Geometry, 'NXgeometry')


class Translation(Group):

    """
    """

registry.register(Translation, 'NXtranslation')


class Shape(Group):

    """
    """

registry.register(Shape, 'NXshape')


class Orientation(Group):

    """
    """

registry.register(Orientation, 'NXorientation')
