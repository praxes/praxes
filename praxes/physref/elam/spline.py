import numpy as np
import quantities as pq

from praxes.lib.decorators import memoize
from praxes.physref.lib.spline import splint


class SplineInterpolable(object):

    __slots__ = ['_db', '_element']

    @property
    def element(self):
        return self._element

    @property
    @memoize
    def _log_independant_value(self):
        return self._get_data('log_energy')

    def __init__(self, element, db):
        self._db = db
        self._element = element

    def __call__(self, energy):
        log_energy = np.log(energy.rescale('eV').magnitude)
        log_xa = self._log_independant_value
        log_ya = self._log_dependant_value
        log_yspline = self._log_dependant_value_spline

        log_res = splint(log_xa, log_ya, log_yspline, log_energy)
        return np.exp(log_res) * pq.cm**2 / pq.g
