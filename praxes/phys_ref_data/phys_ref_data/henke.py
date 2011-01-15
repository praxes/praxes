# -*- coding: utf-8 -*-
'''
Anomolous scattering factors are interpolated based on the values
compiled by the Center for X-Ray Optics (CXRO), at
http://www.cxro.lbl.gov/optical_constants/asf.html
'''

from __future__ import absolute_import

import h5py
import numpy as np
import quantities as pq

from . import base
from .interpolate import interpolate
from ..decorators import memoize


@memoize
def _get_filename():
    import pkg_resources
    return pkg_resources.resource_filename(__name__, 'henkedb.h5')

@memoize
def keys():
    with h5py.File(_get_filename(), 'r') as f:
        return f.keys()


class AtomicData(base.AtomicData, base.H5pyQuantitiesAdapter):

    """
    AtomicData('Si')

    An adapter to provide dispersive scattering factors based on the
    values compiled by the Center for X-Ray Optics (CXRO), at
    http://www.cxro.lbl.gov/optical_constants/asf.html

    Dispersive scattering factors are defined as:

    f(Q=0, E) = f₀(Q=0, E=∞) + f'(Q=0, E) + if"(Q=0, E)
    or
    f(Q=0, E) = f₁(Q=0, E=∞) + if₂(Q=0, E)

    where Q is the magnitude of the scattering vector and E is energy
    in eV.
    """

    def _get_data(self, id):
        return self._get_h5data(_get_filename(), '%s/%s' % (self.element, id))

    @property
    @memoize
    def _energy(self):
        return self._get_data('energy')

    @property
    @memoize
    def _fprime(self):
        return self._get_data('f1') - self.atomic_number

    @property
    @memoize
    def _fdoubleprime(self):
        return self._get_data('f2')

    def __init__(self, symbol):
        """
        symbol is the element or ion symbol like 'Ca' or 'Ca2+'
        """
        base.AtomicData.__init__(self, symbol)
        try:
            assert self.element in keys()
        except AssertionError:
            raise NotImplementedError(
                'Anomolous scattering factors have not been reported for %s'
                % self.element
                )

    def photoabsorption_cross_section(self, energy):
        c = (pq.constants.h*pq.c*pq.constants.r_e/energy).rescale('cm**2')
        return c * self.fdoubleprime(energy)

    def f(self, energy):
        """
        Calculate the Q-independent, energy dependent, scattering
        factors:

        f(Q=0, E) = f₀(Q=0, E=∞) + f'(Q=0, E) + if"(Q=0, E)
        """
        return self.f0() + self.fprime(energy) + 1j * self.fdoubleprime(energy)

    def f0(self, *args):
        return self.atomic_number

    def fprime(self, energy):
        """return f₁ = f₀(Q=0)+f'(E)"""
        energy = energy.rescale('eV')
        return interpolate(
            energy.magnitude, self._energy.magnitude, self._fprime
            )

    def fdoubleprime(self, energy):
        """return f₂(Q=0, E) = f"(Q=0, E)"""
        energy = energy.rescale('eV')
        return interpolate(
            energy.magnitude, self._energy.magnitude, self._fdoubleprime
            )

    def f1(self, energy):
        """return f₁(Q=0, E) = f₀(Q=0, E=∞) + f'(Q=0, E)"""
        return self.f0() + self.fprime(energy)

    def f2(self, energy):
        """return f₂(Q=0, E) = f"(Q=0, E)"""
        return self.fdoubleprime(energy)
