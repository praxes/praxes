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

#from __future__ import absolute_import

import json
import os
import sqlite3

import numpy as np

from praxes.physref.lib.mapping import Mapping
from praxes.lib.decorators import memoize

class AtomicData(Mapping):

    @Mapping._keys.getter
    def _keys(self):
        cursor = self.__db.cursor()
        res = cursor.execute(
            '''select ion from f0 order by id'''
            )
        return tuple(i[0] for i in res)

    def __init__(self):
        self.__db = sqlite3.connect(
            os.path.join(os.path.split(__file__)[0], 'waasmaier_kirfel.db')
            )

    def __hash__(self):
        hash(type(self))

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(
                'Form factor approximations not reported for %s' % key
                )
        return FormFactor(key, self.__db)


class FormFactor(object):
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

    def _get_data(self, id):
        cursor = self.__db.cursor()
        result = cursor.execute('''select %s from f0
            where ion=?''' % id, (self._symbol, )
            ).fetchone()
        assert result is not None
        return result[0]

    @property
    @memoize
    def _a(self):
        return tuple(json.loads(self._get_data('scale')))

    @property
    @memoize
    def _b(self):
        return tuple(json.loads(self._get_data('exponent')))

    @property
    @memoize
    def _c(self):
        return self._get_data('offset')

    def __init__(self, symbol, db):
        """symbol is a string, like 'Ca' or 'Ca2+'"""
        self._symbol = symbol
        self.__db = db

    def __call__(self, Q):
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
