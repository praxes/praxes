import numpy as np
import quantities as pq

from .base import memoize


class SplineInterpolable(object):

    __slots__ = ['_db', '_element']

    @property
    def element(self):
        return self._element

    @property
    @memoize
    def _log_independant_value(self):
        return self._get_data('log_energy')

    def _splint(self, xa, ya, y2a, x):
        '''spline interpolation'''
        try:
            len(x)
        except TypeError:
            x = np.array([x])

        try:
            klo, khi = np.array([
                (np.flatnonzero(xa < i)[-1], np.flatnonzero(xa > i)[0])
                for i in x
                ]).transpose()
        except IndexError:
            raise ValueError(
                'Input values must be between %s and %s'
                % (np.exp(xa[0]), np.exp(xa[-1]))
                )

        h = xa[khi] - xa[klo]
        if any(h <= 0):
            raise ValueError, 'xa input must be strictly increasing'
        a = (xa[khi] - x) / h
        b = (x - xa[klo]) / h

        res = (
            a * ya[klo]
            + b * ya[khi]
            + ((a**3 - a) * y2a[klo] + (b**3 - b) * y2a[khi]) * (h**2) / 6
            )
        return res


    def __init__(self, element, db):
        self._db = db
        self._element = element

    def __call__(self, energy):
        log_energy = np.log(energy.rescale('eV').magnitude)
        log_xa = self._log_independant_value
        log_ya = self._log_dependant_value
        log_yspline = self._log_dependant_value_spline

        log_res = self._splint(log_xa, log_ya, log_yspline, log_energy)
        return np.exp(log_res) * pq.cm**2 / pq.g
