from unittest import TestCase

import numpy as np
import quantities as pq

from ... import elam


class TestCompositions(TestCase):

    def test_mass_fraction_to_stoichiometry(self):
        self.assertEqual(
            elam.mass_fraction_to_stoichiometry('H0.2He0.8')[:10],
            'H1He1.0072'
            )

    def test_stoichiometry_to_mass_fraction(self):
        self.assertEqual(
            elam.stoichiometry_to_mass_fraction('H4He'), 'H0.501805He0.498195'
            )

    def test_transmission_coefficient(self):
        self.assertEqual(
            elam.transmission_coefficient('Fe2O3', 20*pq.keV, 0*pq.mm), 1
            )
        self.assertAlmostEqual(
            elam.transmission_coefficient(
                'Si3N4', 30*pq.keV, 0.5*pq.mm, by_mass=False,
                mass_density=3.44*pq.g/pq.cm**3
                ),
            0.8809,
            places=4
            )

    def test_absorption_coefficient(self):
        self.assertEqual(
            elam.absorption_coefficient('Fe2O3', 20*pq.keV, 0*pq.mm), 0
            )
        self.assertAlmostEqual(
            elam.absorption_coefficient(
                'Si3N4', 30*pq.keV, 0.5*pq.mm, by_mass=False,
                mass_density=3.44*pq.g/pq.cm**3
                ),
            0.1191,
            places=4
            )

    def test_photoabsorption_cross_section(self):
        self.assertAlmostEqual(
            elam.photoabsorption_cross_section(
                'Si3N4', 30*pq.keV, 0.5*pq.mm, mass_density=3.44*pq.g/pq.cm**3
                ),
            1.9099 * pq.cm**-1,
            places=4
            )
