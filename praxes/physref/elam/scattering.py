import json

import numpy as np

from .base import memoize
from .spline import SplineInterpolable


class Scattering(SplineInterpolable):

    def _get_data(self, id):
        cursor = self._db.cursor()
        result = cursor.execute('''select %s from scattering
            where element=?''' % id, (self.element, )
            ).fetchone()
        return np.array(json.loads(result[0]))


class CoherentScattering(Scattering):

    @property
    @memoize
    def _log_dependant_value(self):
        return self._get_data('log_coherent_scatter')

    @property
    @memoize
    def _log_dependant_value_spline(self):
        return self._get_data('log_coherent_scatter_spline')


class IncoherentScattering(Scattering):

    @property
    @memoize
    def _log_dependant_value(self):
        return self._get_data('log_incoherent_scatter')

    @property
    @memoize
    def _log_dependant_value_spline(self):
        return self._get_data('log_incoherent_scatter_spline')
