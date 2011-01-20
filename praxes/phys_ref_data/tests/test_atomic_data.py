import numpy as np
import quantities as pq

from praxes import testing
from ..elam import AtomicData, elamdb
#from .. import waasmaier


class TestElements(testing.TestCase):

    def test_symbol(self):
        for key in ('Si', 'Si4+', 'O2-'):
            self.assertEqual(AtomicData(key).symbol, key)

    def test_element(self):
        for key, val in (('Si', 'Si'), ('Si4+', 'Si'), ('O2-', 'O')):
            self.assertEqual(AtomicData(key).element, val)

    def test_ionization_state(self):
        for key, val in (('Si', ''), ('Si4+', '4+'), ('O2-', '2-')):
            self.assertEqual(AtomicData(key).ionization_state, val)

    def test_electrons(self):
        for key, val in (('Si', 14), ('Si4+', 10), ('O', 8), ('O2-', 10)):
            self.assertEqual(AtomicData(key).electrons, val)

    def test_atomic_mass(self):
        for key, val in (
            ('Si', 28.0855 * pq.u), ('Si4+', 28.0855 * pq.u),
            ('O', 15.9994 * pq.u), ('O2-', 15.9994 * pq.u)
            ):
            self.assertAlmostEqual(AtomicData(key).atomic_mass, val)

    def test_photoabsorption(self):
        self.assertAlmostEqual(
            AtomicData('Cu').photoabsorption_cross_section(10 * pq.keV),
            214.459 * pq.cm**2/pq.g,
            delta=1e-3
            )

    def test_coherent_scattering(self):
        self.assertAlmostEqual(
            AtomicData('Cu').coherent_scattering_cross_section(10 * pq.keV),
            1.45 * pq.cm**2/pq.g,
            delta=1e-3
            )

    def test_incoherent_scattering(self):
        self.assertAlmostEqual(
            AtomicData('Cu').incoherent_scattering_cross_section(10 * pq.keV),
            0.077 * pq.cm**2/pq.g,
            delta=1e-3
            )

    def test_levels(self):
        self.assertEqual(
            AtomicData('U').xray_levels['K'].absorption_edge, 115606.0 * pq.eV
            )
        self.assertEqual(
            AtomicData('Pb').xray_levels['L1'].ck_probabilities['L3'], 0.58
            )
        self.assertEqual(
            AtomicData('Pb').xray_levels['L1'].ck_total_probabilities['L3'],
            0.58464
            )

    def test_transitions(self):
        self.assertEqual(
            AtomicData('U').xray_levels['K'].\
                transitions['K-L3'].emission_energy,
            98440 * pq.eV
            )
