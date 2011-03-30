# -*- coding: utf-8 -*-
"""scatteringfactors defines a class for calculating the Q- and energy-dependent
scattering factors for the elements and ions:

f(Q,E) = f₀(Q)+f'(E)+f"(E)

Q-dependence is appproximated as reported by D. Waasmaier and A. Kirfel,
Acta. Cryst. A, v 51, p 416-431 (1995):

f₀ = ∑_i a_i exp[-b_i(|Q|/4π)²] + c

This approximation is valid for |Q| ≤ 75 Å⁻¹

The dispersion corrections will not be calculated if energy=None is passed to
the anomolous scattering factor method get_f.

Anomolous scattering factors are interpolated based on the values compiled by
the Center for X-Ray Optics (CXRO), at
http://www.cxro.lbl.gov/optical_constants/asf.html
"""

from __future__ import division

import numpy as np
import quantities as pq

from . import base
from ..decorators import memoize

class AtomicData(base.AtomicData):

    @property
    @memoize
    def _dispersive(self):
        from . import henke
        return henke.AtomicData(self.element)

    @property
    @memoize
    def _fluorescence(self):
        from . import elam
        return elam.AtomicData(self.element)

    @property
    @memoize
    def _nondispersive(self):
        from . import waasmaier
        return waasmaier.AtomicData(self.symbol)

    def __init__(self, symbol):
        base.AtomicData.__init__(self, symbol)

    def f(self, Q, energy=None):
        if energy is None:
            return self.f0(Q)
        return self.f0(Q) + self.fprime(energy) + 1j*self.fdoubleprime(energy)

    def f0(self, Q):
        return self._nondispersive.f0(Q)

    def fprime(self, energy):
        return self._dispersive.fprime(energy)

    def fdoubleprime(self, energy):
        return self._dispersive.fdoubleprime(energy)

    def photoabsorption_cross_section(self, energy):
        return self._fluorescence.photoabsorption_cross_section(energy)

    def coherent_scattering_cross_section(self, energy):
        return self._fluorescence.coherent_scattering_cross_section(energy)

    def incoherent_scattering_cross_section(self, energy):
        return self._fluorescence.incoherent_scattering_cross_section(energy)
