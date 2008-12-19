"""
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

    nx_class = 'NXgeometry'

registry.register(Geometry)


class Translation(Group):

    """
    """

    nx_class = 'NXtranslation'

registry.register(Translation)


class Shape(Group):

    """
    """

    nx_class = 'NXshape'

registry.register(Shape)


class Orientation(Group):

    """
    """

    nx_class = 'NXorientation'

registry.register(Orientation)
