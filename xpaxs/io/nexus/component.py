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


class _Component(Group):

    """
    """


class Aperture(_Component):

    """
    """

registry.register(Aperture, 'NXaperture')


class Attenuator(_Component):

    """
    """

registry.register(Attenuator, 'NXattenuator')


class Beam_stop(_Component):

    """
    """

registry.register(Beam_stop, 'NXbeam_stop')


class Bending_magnet(_Component):

    """
    """

registry.register(Bending_magnet, 'NXbeanding_magnet')


class Collimator(_Component):

    """
    """

registry.register(Collimator, 'NXcollimator')


class Crystal(_Component):

    """
    """

registry.register(Crystal, 'NX_crystal')


class Disk_chopper(_Component):

    """
    """

registry.register(Disk_chopper, 'NXdisk_chopper')


class Fermi_chopper(_Component):

    """
    """

registry.register(Fermi_chopper, 'NXfermi_chopper')


class Filter(_Component):

    """
    """

registry.register(Filter, 'NXfilter')


class Flipper(_Component):

    """
    """

registry.register(Flipper, 'NXflipper')


class Guide(_Component):

    """
    """

registry.register(Guide, 'NXguide')


class Insertion_device(_Component):

    """
    """

registry.register(Insertion_device, 'NXinsertion_device')


class Mirror(_Component):

    """
    """

registry.register(Mirror, 'NXmirror')


class Moderator(_Component):

    """
    """

registry.register(Moderator, 'NXmoderator')


class Monochromator(_Component):

    """
    """

registry.register(Monochromator, 'NXmonochromator')


class Polarizer(_Component):

    """
    """

registry.register(Polarizer, 'NXpolarizer')


class Positioner(_Component):

    """
    """

registry.register(Positioner, 'NXpositioner')


class Source(_Component):

    """
    """

registry.register(Source, 'NXsource')


class Velocity_selector(_Component):

    """
    """

registry.register(Velocity_selector, 'NXvelocity_selector')
