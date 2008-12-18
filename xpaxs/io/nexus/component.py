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

    @property
    def nx_class(self):
        return 'NXaperture'

registry.register(Aperture)


class Attenuator(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXattenuator'

registry.register(Attenuator)


class Beam_stop(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXbeam_stop'

registry.register(Beam_stop)


class Bending_magnet(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXbending_magnet'

registry.register(Bending_magnet)


class Collimator(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXcollimator'

registry.register(Collimator)


class Crystal(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXcrystal'

registry.register(Crystal)


class Disk_chopper(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXdisk_chopper'

registry.register(Disk_chopper)


class Fermi_chopper(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXfermi_chopper'

registry.register(Fermi_chopper)


class Filter(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXfilter'

registry.register(Filter)


class Flipper(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXflipper'

registry.register(Flipper)


class Guide(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXguide'

registry.register(Guide)


class Insertion_device(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXinsertion_device'

registry.register(Insertion_device)


class Mirror(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXmirror'

registry.register(Mirror)


class Moderator(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXmoderator'

registry.register(Moderator)


class Monochromator(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXmonochromator'

registry.register(Monochromator)


class Polarizer(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXpolarizer'

registry.register(Polarizer)


class Positioner(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXpositioner'

registry.register(Positioner)


class Source(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXsource'

registry.register(Source)


class Velocity_selector(_Component):

    """
    """

    @property
    def nx_class(self):
        return 'NXvelocity_selector'

registry.register(Velocity_selector)
