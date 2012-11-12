# -*- coding: utf-8 -*-
'''
The elam module is an interface to a database of fundamental X-ray fluorescence
parameters compiled by W.T. Elam, B.D. Ravel and J.R. Sieber, and published in
Radiation Physics and Chemistry, 63 (2), 121 (2002). The database is published
by NIST at http://www.nist.gov/mml/analytical/inorganic/xrf.cfm.
'''

import copy

import numpy as np
import quantities as pq

from .. import composition as _comp

from .atomicdata import AtomicData
atomic_data = AtomicData()


def mass_fraction_to_stoichiometry(mass_fraction):
    "Given a string representing mass fractions, return the stoichiometry"
    temp = _comp.load(mass_fraction)
    for k in temp:
        temp[k] /= atomic_data[k].molar_mass.magnitude
    denom = min(temp.values())
    for k in temp:
        temp[k] /= denom
    return str(temp)


def stoichiometry_to_mass_fraction(stoichiometry):
    "Given a string representing stoichiometry, return the mass fractions"
    temp = _comp.load(stoichiometry)
    molar_mass = 0
    for k, v in temp.items():
        temp[k] = atomic_data[k].molar_mass.magnitude * v
        molar_mass += temp[k]
    for k in temp:
        temp[k] /= molar_mass
    return str(temp)


def estimate_mass_density(stoichiometry):
    temp = _comp.load(stoichiometry)
    denom = sum(temp.values())
    density = 0 * pq.g/pq.cm**3
    for k, v in temp.items():
        density += v/denom * atomic_data[k].mass_density
    return density


def photoabsorption_cross_section(
        composition, energy, by_mass=True, mass_density=None
    ):
    """Given a string representing a composition, calculate the
    energy-dependent photoabsorption cross section
    """
    if by_mass:
        mass_fraction = _comp.load(composition)
        stoichiometry = _comp.load(
            mass_fraction_to_stoichiometry(composition)
            )
    if not by_mass:
        stoichiometry = _comp.load(composition)
        mass_fraction = _comp.load(
            stoichiometry_to_mass_fraction(composition)
            )

    if mass_density is None:
        mass_density = estimate_mass_density(str(stoichiometry))

    try:
        res = np.zeros(len(energy), 'd') * pq.cm**2/pq.g
    except TypeError:
        res = [0] * pq.cm**2/pq.g
    denom = sum(mass_fraction.values())
    for k,v in mass_fraction.items():
        res += v/denom * atomic_data[k].photoabsorption_cross_section(energy)
    return res * mass_density


def transmission_coefficient(
        composition, energy, thickness, by_mass=True, mass_density=None
    ):
    pac = photoabsorption_cross_section(
        composition, energy, by_mass=by_mass, mass_density=mass_density
        )
    return np.exp(-pac*thickness.rescale('cm'))


def absorption_coefficient(
        composition, energy, thickness, by_mass=True, mass_density=None
    ):
    return 1 - transmission_coefficient(
        composition, energy, thickness, by_mass=by_mass,
        mass_density=mass_density
        )
