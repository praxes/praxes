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


class _Component(NXgroup):

    """
    """


class NXaperture(_Component):

    """
    """

registry['NXaperture'] = NXaperture


class NXaperture(_Component):

    """
    """

registry['NXaperture'] = NXaperture


class NXattenuator(_Component):

    """
    """

registry['NXattenuator'] = NXattenuator


class NXbeam_stop(_Component):

    """
    """

registry['NXbeam_stop'] = NXbeam_stop


class NXbending_magnet(_Component):

    """
    """

registry['NXbending_magnet'] = NXbending_magnet


class NXcollimator(_Component):

    """
    """

registry['NXcollimator'] = NXcollimator


class NXcrystal(_Component):

    """
    """

registry['NXcrystal'] = NXcrystal


class NXdetector(_Component):

    """
    """

registry['NXdetector'] = NXdetector


class NXdisk_chopper(_Component):

    """
    """

registry['NXdisk_chopper'] = NXdisk_chopper


class NXfermi_chopper(_Component):

    """
    """

registry['NXfermi_chopper'] = NXfermi_chopper


class NXfilter(_Component):

    """
    """

registry['NXfilter'] = NXfilter


class NXflipper(_Component):

    """
    """

registry['NXflipper'] = NXflipper


class NXguide(_Component):

    """
    """

registry['NXguide'] = NXguide


class NXinsertion_device(_Component):

    """
    """

registry['NXinsertion_device'] = NXinsertion_device


class NXmirror(_Component):

    """
    """

registry['NXmirror'] = NXmirror


class NXmoderator(_Component):

    """
    """

registry['NXmoderator'] = NXmoderator


class NXmonochromator(_Component):

    """
    """

registry['NXmonochromator'] = NXmonochromator


class NXpolarizer(_Component):

    """
    """

registry['NXpolarizer'] = NXpolarizer


class NXpositioner(_Component):

    """
    """

registry['NXpositioner'] = NXpositioner


class NXsource(_Component):

    """
    """

registry['NXsource'] = NXsource


class NXvelocity_selector(_Component):

    """
    """

registry['NXvelocity_selector'] = NXvelocity_selector
