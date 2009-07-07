"""
"""

from __future__ import absolute_import

from .group import Group


class _Component(Group):

    """
    """


class Aperture(_Component):

    """
    """

    nx_class = 'NXaperture'


class Attenuator(_Component):

    """
    """

    nx_class = 'NXattenuator'


class Beam_stop(_Component):

    """
    """

    nx_class = 'NXbeam_stop'


class Bending_magnet(_Component):

    """
    """

    nx_class = 'NXbending_magnet'


class Collimator(_Component):

    """
    """

    nx_class = 'NXcollimator'


class Crystal(_Component):

    """
    """

    nx_class = 'NXcrystal'


class Disk_chopper(_Component):

    """
    """

    nx_class = 'NXdisk_chopper'


class Fermi_chopper(_Component):

    """
    """

    nx_class = 'NXfermi_chopper'


class Filter(_Component):

    """
    """

    nx_class = 'NXfilter'


class Flipper(_Component):

    """
    """

    nx_class = 'NXflipper'


class Guide(_Component):

    """
    """

    nx_class = 'NXguide'


class Insertion_device(_Component):

    """
    """

    nx_class = 'NXinsertion_device'


class Mirror(_Component):

    """
    """

    nx_class = 'NXmirror'


class Moderator(_Component):

    """
    """

    nx_class = 'NXmoderator'


class Monochromator(_Component):

    """
    """

    nx_class = 'NXmonochromator'


class Polarizer(_Component):

    """
    """

    nx_class = 'NXpolarizer'


class Positioner(_Component):

    """
    """

    nx_class = 'NXpositioner'


class Source(_Component):

    """
    """

    nx_class = 'NXsource'


class Velocity_selector(_Component):

    """
    """

    nx_class = 'NXvelocity_selector'
