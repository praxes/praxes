import json

import numpy as np

from .base import memoize
from .spline import SplineInterpolable


class Photoabsorption(SplineInterpolable):

    def _get_data(self, id):
        cursor = self._db.cursor()
        result = cursor.execute('''select %s from photoabsorption
            where element=?''' % id, (self.element, )
            ).fetchone()
        return np.array(json.loads(result[0]))

    @property
    @memoize
    def _log_dependant_value(self):
        return self._get_data('log_photoabsorption')

    @property
    @memoize
    def _log_dependant_value_spline(self):
        return self._get_data('log_photoabsorption_spline')
