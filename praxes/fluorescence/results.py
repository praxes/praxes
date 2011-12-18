from threading import RLock

import numpy as np


class XRFMapResultProxy(object):

    def __init__(self, storage, elements=None, shape=None):
        self._lock = RLock()
        self._storage = storage
        self._cache = {}

        if elements and shape:
            # we are overwriting an existing result:
            with self._storage:
                if 'element_maps' in self._storage:
                    del self._storage['element_maps']

                element_maps = self._storage.create_group(
                    'element_maps', type='ElementMaps'
                    )

                for map_type, cls in [
                    ('fit', 'Fit'),
                    ('fit_error', 'FitError'),
                    ('mass_fraction', 'MassFraction')
                    ]:
                    for element in elements:
                        data = np.zeros(shape, 'f')
                        entry = '%s_%s'%(element, map_type)
                        element_maps.create_dataset(entry, type=cls, data=data)

        with self._storage:
            if 'element_maps' in self._storage:
                shape = self._storage.entry.acquisition_shape
                for k, v in self._storage['element_maps'].items():
                    self._cache[k] = v[()].reshape(shape)

    def update_fit(self, element, index, value):
        with self._lock:
            self._cache['%s_fit' % element].flat[index] = value

    def update_fit_error(self, element, index, value):
        with self._lock:
            self._cache['%s_fit_error' % element].flat[index] = value

    def update_mass_fraction(self, element, index, value):
        with self._lock:
            self._cache['%s_mass_fraction' % element].flat[index] = value

    def flush(self):
        with self._lock:
            with self._storage:
                maps = self._storage['element_maps']
                for k, v in self._cache.items():
                    maps[k][()] = v.flatten()
                self._storage.file.flush()

    def get(self, element, map_type):
        with self._lock:
            return self._cache['%s_%s' % (element, map_type)].copy()
