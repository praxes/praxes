import operator as op
from unittest import TestCase

import numpy as np
import quantities as pq

from ..elam import atomic_data


class TestElements(TestCase):

    def test_keys(self):
        self.assertEqual(atomic_data.keys()[0], 'H')

    def test_contains(self):
        self.assertTrue('H' in atomic_data)

    def test_len(self):
        self.assertEqual(len(atomic_data), 98)

    def test_iter(self):
        self.assertEqual([i for i in atomic_data][0], 'H')

    def test_creation(self):
        for key in ('Si', 'O'):
            self.assertEqual(atomic_data[key].symbol, key)
            self.assertEqual(atomic_data.get(key).symbol, key)
        self.assertEqual(atomic_data.get('Z', None), None)
        with self.assertRaises(KeyError):
            for key in ('Z', 'O2-'):
                atomic_data[key]

    def test_values(self):
        self.assertEqual(atomic_data.values()[0].symbol, 'H')

    def test_items(self):
        self.assertEqual(atomic_data.items()[0][0], 'H')
        self.assertEqual(atomic_data.items()[0][1].symbol, 'H')

    def test_atomic_mass(self):
        for key, val in (('Si', 28.0855 * pq.u), ('O', 15.9994 * pq.u)):
            self.assertAlmostEqual(atomic_data[key].atomic_mass, val)

    def test_molar_mass(self):
        for key, val in (
            ('Si', 28.0855 * pq.g/pq.mol), ('O', 15.9994 * pq.g/pq.mol)
            ):
            self.assertAlmostEqual(atomic_data[key].molar_mass, val)

    def test_atomic_number(self):
        self.assertEqual(atomic_data['H'].atomic_number, 1)

    def test_mass_density(self):
        self.assertEqual(atomic_data['C'].mass_density, 2.26 * pq.g/pq.cm**3)

    def test_photoabsorption(self):
        self.assertAlmostEqual(
            atomic_data['Cu'].photoabsorption_cross_section(10 * pq.keV),
            214.459 * pq.cm**2/pq.g,
            delta=1e-3
            )

    def test_coherent_scattering(self):
        self.assertAlmostEqual(
            atomic_data['Cu'].coherent_scattering_cross_section(10 * pq.keV),
            1.45 * pq.cm**2/pq.g,
            delta=1e-3
            )

    def test_incoherent_scattering(self):
        self.assertAlmostEqual(
            atomic_data['Cu'].incoherent_scattering_cross_section(10 * pq.keV),
            0.077 * pq.cm**2/pq.g,
            delta=1e-3
            )


class TestLevels(TestCase):

    def test_keys(self):
        self.assertEqual(atomic_data['U'].keys()[0], 'K')

    def test_creation(self):
        self.assertEqual(atomic_data['U']['K'].iupac_symbol, 'K')

    def test_jump_ratio(self):
        self.assertEqual(atomic_data['U']['L2'].jump_ratio, 1.4)

    def test_fluorescence_yield(self):
        self.assertEqual(atomic_data['U']['L2'].fluorescence_yield, 0.467)

    def test_absorption_edge(self):
        self.assertEqual(atomic_data['U']['L2'].absorption_edge, 20.948*pq.keV)

    def test_element(self):
        self.assertEqual(atomic_data['U']['L2'].element.symbol, 'U')


class TestTransitions(TestCase):

    def test_keys(self):
        self.assertEqual(atomic_data['U']['K'].keys()[0], 'L1')

    def test_creation(self):
        self.assertEqual(atomic_data['U']['K']['L3'].iupac_symbol, 'K-L3')

    def test_initial_level(self):
        self.assertEqual(
            atomic_data['U']['K']['L3'].initial_level.iupac_symbol, 'K'
            )

    def test_final_level(self):
        self.assertEqual(
            atomic_data['U']['K']['L3'].final_level.iupac_symbol, 'L3'
            )

    def test_element(self):
        self.assertEqual(atomic_data['U']['K']['L3'].element.symbol, 'U')

    def test_emission_energy(self):
        self.assertEqual(
            atomic_data['U']['K']['L3'].emission_energy, 98.440 * pq.keV
            )

    def test_intensity(self):
        self.assertEqual(atomic_data['U']['K']['L3'].intensity, 0.473147)

    def test_siegbahn_symbol(self):
        self.assertEqual(atomic_data['U']['K']['L3'].siegbahn_symbol, 'Ka1')
