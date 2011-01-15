# -*- coding: utf-8 -*-
"""
Parameters for calculating the atomic scattering factors for free
atoms and ions, as reported by D. Waasmaier and A. Kirfel, Acta.
Cryst. A, v 51, p 416-431 (1995)
 ┌ ┐ ┌              ┐
 │a│ │a₁ a₂ a₃ a₄ a₅│
 │b│=│b₁ b₂ b₃ b₄ b₅│
 │c│ │c₁ 0  0  0  0 │
 └ ┘ └              ┘
"""

from __future__ import absolute_import

import h5py
import numpy as np

from . import base
from ..decorators import memoize

@memoize
def _get_filename():
    import pkg_resources
    return pkg_resources.resource_filename(__name__, 'waasmaierdb.h5')

@memoize
def keys():
    with h5py.File(_get_filename(), 'r') as f:
        return f.keys()

class AtomicData(base.AtomicData):

    """
    NondispersiveScatterer('Si')

    NondispersiveScatterer instances are elements with methods to
    calculate nondispersive scattering factors and properties based
    on these values.

    Parameters for calculating the nondispersive scattering factors
    for free atoms and ions, as reported by D. Waasmaier and A.
    Kirfel, Acta. Cryst. A, v 51, p 416-431 (1995)
    ┌ ┐ ┌              ┐
    │a│ │a₁ a₂ a₃ a₄ a₅│
    │b│=│b₁ b₂ b₃ b₄ b₅│
    │c│ │c₁ 0  0  0  0 │
    └ ┘ └              ┘
    """

    def __init__(self, symbol):
        """symbol is a string, like 'Ca' or 'Ca2+'"""
        base.AtomicData.__init__(self, symbol)
        try:
            with h5py.File(_get_filename(), 'r') as f:
                self._a = f[self.symbol]['a'][...]
                self._b = f[self.symbol]['b'][...]
                self._c = f[self.symbol]['c'][...]
        except KeyError:
            raise exceptions.RuntimeError(
                'The form factor cannot be approximated for %s.'%symbol
                )

    def f(self, Q):
        """
        Calculate the Q-dependent, energy-independent, scattering
        factors:

        f = f₀(Q)

        Q-dependence is appproximated as reported by D. Waasmaier and
        A. Kirfel, Acta. Cryst. A, v 51, p 416-431 (1995):

        f₀(Q) = ∑_i a_i exp[-b_i(|Q|/4π)²] + c

        This approximation is valid for |Q| ≤ 75 Å⁻¹
        """
        Q = Q.rescale('1/angstrom').magnitude
        f = Q * 0.0 + self._c
        for a, b in np.array([self._a, self._b]).transpose():
            f += a * np.exp(-b * (Q / (4 * np.pi))**2)
        return f

    def f0(self, Q):
        """
        Calculate the Q-dependent, energy-independent scattering
        factors using the appproximation reported by D. Waasmaier and
        A. Kirfel, Acta. Cryst. A, v 51, p 416-431 (1995):

        f₀(Q) = ∑_i a_i exp[-b_i(|Q|/4π)²] + c

        This approximation is valid for |Q| ≤ 75 Å⁻¹
        """
        return self.f(Q)
