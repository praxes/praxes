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

from .group import NXgroup
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXgeometry(NXgroup):

    """
    """

registry['NXgeometry'] = NXgeometry


class NXtranslation(NXgroup):

    """
    """

registry['NXtranslation'] = NXtranslation


class NXshape(NXgroup):

    """
    """

registry['NXshape'] = NXshape


class NXorientation(NXgroup):

    """
    """

registry['NXorientation'] = NXorientation
