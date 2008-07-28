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


class NXcomponent(NXgroup):

    """
    """


class NXaperture(NXcomponent):

    """
    """

registry['NXaperture'] = NXaperture


class NXaperture(NXcomponent):

    """
    """

registry['NXaperture'] = NXaperture


class NXattenuator(NXcomponent):

    """
    """

registry['NXattenuator'] = NXattenuator


class NXbeam_stop(NXcomponent):

    """
    """

registry['NXbeam_stop'] = NXbeam_stop


class NXbending_magnet(NXcomponent):

    """
    """

registry['NXbending_magnet'] = NXbending_magnet


class NXcollimator(NXcomponent):

    """
    """

registry['NXcollimator'] = NXcollimator


class NXcrystal(NXcomponent):

    """
    """

registry['NXcrystal'] = NXcrystal


class NXdetector(NXcomponent):

    """
    """

registry['NXdetector'] = NXdetector


class NXdisk_chopper(NXcomponent):

    """
    """

registry['NXdisk_chopper'] = NXdisk_chopper


class NXfermi_chopper(NXcomponent):

    """
    """

registry['NXfermi_chopper'] = NXfermi_chopper


class NXfilter(NXcomponent):

    """
    """

registry['NXfilter'] = NXfilter


class NXflipper(NXcomponent):

    """
    """

registry['NXflipper'] = NXflipper


class NXguide(NXcomponent):

    """
    """

registry['NXguide'] = NXguide


class NXinsertion_device(NXcomponent):

    """
    """

registry['NXinsertion_device'] = NXinsertion_device


class NXmirror(NXcomponent):

    """
    """

registry['NXmirror'] = NXmirror


class NXmoderator(NXcomponent):

    """
    """

registry['NXmoderator'] = NXmoderator


class NXmonitor(NXcomponent):

    """
    """

registry['NXmonitor'] = NXmonitor


class NXmonochromator(NXcomponent):

    """
    """

registry['NXmonochromator'] = NXmonochromator


class NXpolarizer(NXcomponent):

    """
    """

registry['NXpolarizer'] = NXpolarizer


class NXpositioner(NXcomponent):

    """
    """

registry['NXpositioner'] = NXpositioner


class NXsource(NXcomponent):

    """
    """

registry['NXsource'] = NXsource


class NXvelocity_selector(NXcomponent):

    """
    """

registry['NXvelocity_selector'] = NXvelocity_selector
