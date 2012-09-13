from unittest import TestCase

import numpy as np
import quantities as pq

from ..atomicdata import AtomicData
atomic_data = AtomicData()


class TestFormFactors(TestCase):

    def test_keys(self):
        self.assertEqual(atomic_data.keys()[0], 'H')

    def test_contains(self):
        self.assertTrue('H' in atomic_data)

    def test_len(self):
        self.assertEqual(len(atomic_data), 211)

    def test_iter(self):
        self.assertEqual([i for i in atomic_data][0], 'H')

    def test_creation(self):
        for key in ('Si', 'O'):
            self.assertEqual(atomic_data[key].symbol, key)
            self.assertEqual(atomic_data.get(key).symbol, key)
        self.assertEqual(atomic_data.get('Z', None), None)
        with self.assertRaises(KeyError):
            for key in ('Z'):
                atomic_data[key]

    def test_values(self):
        self.assertEqual(atomic_data.values()[0].symbol, 'H')

    def test_items(self):
        self.assertEqual(atomic_data.items()[0][0], 'H')

    def test_Q0(self):
        self.Q0('Cu', 29)
        self.Q0('H', 1)
        self.Q0('H1-', 2)
        self.Q0('He', 2)
        self.Q0('O', 8)
        self.Q0('O2-', 10)
        self.Q0('C', 6)
        self.Q0('Cval', 6)
        self.Q0('Cu', 29)
        self.Q0('U', 92)

    def Q0(self, element, electrons, delta=2e-2):
        self.assertAlmostEqual(
            atomic_data[element](0 / pq.angstrom),
            electrons,
            delta=delta
            )
