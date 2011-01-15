from numpy.testing import *
import numpy as np
import quantities as pq

from .. import AtomicData
from .. import waasmaier

def test_symbol():
    def test_symbol(key):
        x = AtomicData(key)
        assert_equal(x.symbol, key)

    for key in ('Si', 'Si4+', 'O2-'):
        yield test_symbol, key

def test_element():
    def test_element(key, val):
        x = AtomicData(key)
        assert_equal(x.element, val)

    for key, val in (('Si', 'Si'), ('Si4+', 'Si'), ('O2-', 'O')):
        yield test_element, key, val

def test_ionization_state():
    def test_ionization_state(key, val):
        x = AtomicData(key)
        assert_equal(x.ionization_state, val)

    for key, val in (('Si', ''), ('Si4+', '4+'), ('O2-', '2-')):
        yield test_ionization_state, key, val

def test_electrons():
    def test_electrons(key, val):
        x = AtomicData(key)
        assert_equal(x.electrons, val)

    for key, val in (('Si', 14), ('Si4+', 10), ('O', 8), ('O2-', 10)):
        yield test_electrons, key, val

def test_atomic_mass():
    def test_atomic_mass(key, val):
        x = AtomicData(key)
        assert_almost_equal(x.atomic_mass, val)

    for key, val in (
        ('Si', 28.0855 * pq.u), ('Si4+', 28.0855 * pq.u),
        ('O', 15.9994 * pq.u), ('O2-', 15.9994 * pq.u)
        ):
        yield test_atomic_mass, key, val

def test_f0_0():
    def test_f0_0(key):
        try:
            x = AtomicData(key)
            assert_almost_equal(x.f0(0/pq.angstrom), x.electrons, decimal=1)
        except NotImplementedError:
            pass

    for key in waasmaier.keys():
        if key in ('Cval', 'MGIN', 'OOIN'):
            continue
        yield test_f0_0, key
