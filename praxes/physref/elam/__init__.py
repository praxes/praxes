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

from ..stoichiometry import parse

from .atomicdata import AtomicData
atomic_data = AtomicData()


def _dict_to_comp(d):
    res = ''
    for k, v in d.items():
        res += k + str(v)
    return res

def mass_fraction_to_stoichiometry(mass_fraction):
    temp = parse(mass_fraction)
    for k in temp:
        temp[k] /= atomic_data[k].molar_mass.magnitude
    denom = min(temp.values())
    for k in temp:
        temp[k] /= denom
    return _dict_to_comp(temp)

#print mass_fraction_to_stoichiometry("C80.1H19.9")

def stoichiometry_to_mass_fraction(stoichiometry):
    temp = parse(stoichiometry)
    molar_mass = 0
    for k, v in temp.items():
        temp[k] = atomic_data[k].molar_mass.magnitude * v
        molar_mass += temp[k]
    for k in temp:
        temp[k] /= molar_mass
    return _dict_to_comp(temp)

#print stoichiometry_to_mass_fraction("CH2.96")


def estimate_mass_density(stoichiometry):
    temp = parse(stoichiometry)
    denom = sum(temp.values())
    density = 0 * pq.g/pq.cm**3
    for k, v in temp.items():
        density += v/denom * atomic_data[k].mass_density
    return density


def photoabsorption_cross_section(
        composition, energy, by_mass=True, mass_density=None
    ):
    if by_mass:
        mass_fraction = parse(composition)
        stoichiometry = parse(mass_fraction_to_stoichiometry(composition))
    if not by_mass:
        stoichiometry = parse(composition)
        mass_fraction = parse(stoichiometry_to_mass_fraction(composition))

    if mass_density is None:
        mass_density = estimate_mass_density(_dict_to_comp(stoichiometry))

    res = np.zeros(len(energy), 'd') * pq.cm**2/pq.g
    denom = sum(mass_fraction.values())
    for k,v in mass_fraction.items():
        res += v/denom * atomic_data[k].photoabsorption_cross_section(energy)
    return res * mass_density
