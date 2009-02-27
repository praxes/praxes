"""
"""

from __future__ import absolute_import

from .group import Group
from .registry import registry


class _Component(Group):

    """
    """


class Aperture(_Component):

    """
    """

    nx_class = 'NXaperture'

registry.register(Aperture)


class Attenuator(_Component):

    """
    """

    nx_class = 'NXattenuator'

registry.register(Attenuator)


class Beam_stop(_Component):

    """
    """

    nx_class = 'NXbeam_stop'

registry.register(Beam_stop)


class Bending_magnet(_Component):

    """
    """

    nx_class = 'NXbending_magnet'

registry.register(Bending_magnet)


class Collimator(_Component):

    """
    """

    nx_class = 'NXcollimator'

registry.register(Collimator)


class Crystal(_Component):

    """
    """

    nx_class = 'NXcrystal'

registry.register(Crystal)


class Disk_chopper(_Component):

    """
    """

    nx_class = 'NXdisk_chopper'

registry.register(Disk_chopper)


class Fermi_chopper(_Component):

    """
    """

    nx_class = 'NXfermi_chopper'

registry.register(Fermi_chopper)


class Filter(_Component):

    """
    """

    nx_class = 'NXfilter'

registry.register(Filter)


class Flipper(_Component):

    """
    """

    nx_class = 'NXflipper'

registry.register(Flipper)


class Guide(_Component):

    """
    """

    nx_class = 'NXguide'

registry.register(Guide)


class Insertion_device(_Component):

    """
    """

    nx_class = 'NXinsertion_device'

registry.register(Insertion_device)


class Mirror(_Component):

    """
    """

    nx_class = 'NXmirror'

registry.register(Mirror)


class Moderator(_Component):

    """
    """

    nx_class = 'NXmoderator'

registry.register(Moderator)


class Monochromator(_Component):

    """
    """

    nx_class = 'NXmonochromator'

registry.register(Monochromator)


class Polarizer(_Component):

    """
    """

    nx_class = 'NXpolarizer'

registry.register(Polarizer)


class Positioner(_Component):

    """
    """

    nx_class = 'NXpositioner'

registry.register(Positioner)


class Source(_Component):

    """
    """

    nx_class = 'NXsource'

registry.register(Source)


class Velocity_selector(_Component):

    """
    """

    nx_class = 'NXvelocity_selector'

registry.register(Velocity_selector)
