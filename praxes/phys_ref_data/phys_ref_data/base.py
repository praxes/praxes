# -*- coding: utf-8 -*-
'''
'''

from __future__ import absolute_import

import re

import h5py
import numpy as np
import quantities as pq

from ..decorators import memoize


class H5pyQuantitiesAdapter(object):

    def _get_h5data(self, filename, id): 
        def _get_data(item):
            if not isinstance(item, h5py.Dataset):
                return None 
            units = item.attrs.get('units', None)
            if units is not None:
                return pq.Quantity(item[...], units)
            return item[...]

        with h5py.File(filename, 'r') as f:
            item = f[id]

            if isinstance(item, h5py.Dataset):
                return _get_data(item)

            res = {}  
            for k, v in item.iteritems():   
                res[k] = _get_data(v)
            return res


class AtomicData:

    """
    """

    @property
    @memoize
    def atomic_mass(self):
        return (self.molar_mass / pq.constants.N_A).rescale('amu')

    @property
    @memoize
    def atomic_number(self):
        return _atomic_data[self.element]['atomic_number']

    @property
    @memoize
    def electrons(self):
        z = self.atomic_number
        if self.ionization_state:
            charge = int(self.ionization_state[:-1])
            sign = self.ionization_state[-1]
            if sign == '+':
                charge *= -1
            z += charge
        return z

    @property
    @memoize
    def element(self):
        return re.findall('[A-Z][a-z]?|\d*[+,-]?', self.symbol)[0].capitalize()

    @property
    @memoize
    def ionization_state(self):
        return re.findall('[A-Z][a-z]?|\d*[+,-]?', self.symbol)[1].capitalize()

    @property
    @memoize
    def molar_mass(self):
        return _atomic_data[self.element]['molar_mass']*pq.g/pq.mol

    @property
    def symbol(self):
        return self._symbol

    def __init__(self, symbol):
        """symbol is a string, like 'Ca' or 'Ca2+'
        """
        self._symbol = symbol.capitalize()


_atomic_data = {
    'Ac': {
        'atomic_number': 89,
        'molar_mass': 227.028,
        'name': '',
        'symbol': 'Ac'
        },
    'Ag': {
        'atomic_number': 47,
        'molar_mass': 107.868,
        'name': '',
        'symbol': 'Ag'
        },
    'Al': {
        'atomic_number': 13,
        'molar_mass': 26.9815,
        'name': '',
        'symbol': 'Al'
        },
    'Am': {
        'atomic_number': 95,
        'molar_mass': 243.061,
        'name': '',
        'symbol': 'Am'
        },
    'Ar': {
        'atomic_number': 18,
        'molar_mass': 39.948,
        'name': '',
        'symbol': 'Ar'
        },
    'As': {
        'atomic_number': 33,
        'molar_mass': 74.9216,
        'name': '',
        'symbol': 'As'
        },
    'At': {
        'atomic_number': 85,
        'molar_mass': 209.987,
        'name': '',
        'symbol': 'At'},
    'Au': {
        'atomic_number': 79,
        'molar_mass': 196.967,
        'name': '',
        'symbol': 'Au'
        },
    'B': {
        'atomic_number': 5,
        'molar_mass': 10.81,
        'name': '',
        'symbol': 'B'
        },
    'Ba': {
        'atomic_number': 56,
        'molar_mass': 137.33,
        'name': '',
        'symbol': 'Ba'
        },
    'Be': {
        'atomic_number': 4,
        'molar_mass': 9.0122,
        'name': '',
        'symbol': 'Be'
        },
    'Bi': {
        'atomic_number': 83,
        'molar_mass': 208.98,
        'name': '',
        'symbol': 'Bi'
        },
    'Bk': {
        'atomic_number': 97,
        'molar_mass': 247.07,
        'name': '',
        'symbol': 'Bk'
        },
    'Br': {
        'atomic_number': 35,
        'molar_mass': 79.904,
        'name': '',
        'symbol': 'Br'
        },
    'C': {
        'atomic_number': 6,
        'molar_mass': 12.011,
        'name': '',
        'symbol': 'C'
        },
    'Ca': {
        'atomic_number': 20,
        'molar_mass': 40.08,
        'name': '',
        'symbol': 'Ca'
        },
    'Cd': {
        'atomic_number': 48,
        'molar_mass': 112.41,
        'name': '',
        'symbol': 'Cd'},
    'Ce': {
        'atomic_number': 58,
        'molar_mass': 140.12,
        'name': '',
        'symbol': 'Ce'
        },
    'Cf': {
        'atomic_number': 98,
        'molar_mass': 251.08,
        'name': '',
        'symbol': 'Cf'},
    'Cl': {
        'atomic_number': 17,
        'molar_mass': 35.453,
        'name': '',
        'symbol': 'Cl'
        },
    'Cm': {
        'atomic_number': 96,
        'molar_mass': 247.07,
        'name': '',
        'symbol': 'Cm'
        },
    'Co': {
        'atomic_number': 27,
        'molar_mass': 58.9332,
        'name': '',
        'symbol': 'Co'
        },
    'Cr': {
        'atomic_number': 24,
        'molar_mass': 51.996,
        'name': '',
        'symbol': 'Cr'
        },
    'Cs': {
        'atomic_number': 55,
        'molar_mass': 132.905,
        'name': '',
        'symbol': 'Cs'
        },
    'Cu': {
        'atomic_number': 29,
        'molar_mass': 63.546,
        'name': '',
        'symbol': 'Cu'
        },
    'Dy': {
        'atomic_number': 66,
        'molar_mass': 162.5,
        'name': '',
        'symbol': 'Dy'
        },
    'Er': {
        'atomic_number': 68,
        'molar_mass': 167.26,
        'name': '',
        'symbol': 'Er'
        },
    'Eu': {
        'atomic_number': 63,
        'molar_mass': 151.96,
        'name': '',
        'symbol': 'Eu'
        },
    'F': {
        'atomic_number': 9,
        'molar_mass': 18.9984,
        'name': '',
        'symbol': 'F'
        },
    'Fe': {
        'atomic_number': 26,
        'molar_mass': 55.847,
        'name': '',
        'symbol': 'Fe'
        },
    'Fr': {
        'atomic_number': 87,
        'molar_mass': 223.02,
        'name': '',
        'symbol': 'Fr'
        },
    'Ga': {
        'atomic_number': 31,
        'molar_mass': 69.72,
        'name': '',
        'symbol': 'Ga'
        },
    'Gd': {
        'atomic_number': 64,
        'molar_mass': 157.25,
        'name': '',
        'symbol': 'Gd'
        },
    'Ge': {
        'atomic_number': 32,
        'molar_mass': 72.59,
        'name': '',
        'symbol': 'Ge'
        },
    'H': {
        'atomic_number': 1,
        'molar_mass': 1.0079,
        'name': '',
        'symbol': 'H'
        },
    'He': {
        'atomic_number': 2,
        'molar_mass': 4.0026,
        'name': '',
        'symbol': 'He'
        },
    'Hf': {
        'atomic_number': 72,
        'molar_mass': 178.49,
        'name': '',
        'symbol': 'Hf'
        },
    'Hg': {
        'atomic_number': 80,
        'molar_mass': 200.59,
        'name': '',
        'symbol': 'Hg'
        },
    'Ho': {
        'atomic_number': 67,
        'molar_mass': 164.93,
        'name': '',
        'symbol': 'Ho'
        },
    'I': {
        'atomic_number': 53,
        'molar_mass': 126.905,
        'name': '',
        'symbol': 'I'
        },
    'In': {
        'atomic_number': 49,
        'molar_mass': 114.82,
        'name': '',
        'symbol': 'In'
        },
    'Ir': {
        'atomic_number': 77,
        'molar_mass': 192.22,
        'name': '',
        'symbol': 'Ir'
        },
    'K': {
        'atomic_number': 19,
        'molar_mass': 39.0983,
        'name': '',
        'symbol': 'K'
        },
    'Kr': {
        'atomic_number': 36,
        'molar_mass': 83.80,
        'name': '',
        'symbol': 'Kr'},
    'La': {
        'atomic_number': 57,
        'molar_mass': 138.906,
        'name': '',
        'symbol': 'La'
        },
    'Li': {
        'atomic_number': 3,
        'molar_mass': 6.941,
        'name': '',
        'symbol': 'Li'
        },
    'Lu': {
        'atomic_number': 71,
        'molar_mass': 174.967,
        'name': '',
        'symbol': 'Lu'
        },
    'Mg': {
        'atomic_number': 12,
        'molar_mass': 24.305,
        'name': '',
        'symbol': 'Mg'
        },
    'Mn': {
        'atomic_number': 25,
        'molar_mass': 54.938,
        'name': '',
        'symbol': 'Mn'
        },
    'Mo': {
        'atomic_number': 42,
        'molar_mass': 95.94,
        'name': '',
        'symbol': 'Mo'
        },
    'N': {
        'atomic_number': 7,
        'molar_mass': 14.0067,
        'name': '',
        'symbol': 'N'
        },
    'Na': {
        'atomic_number': 11,
        'molar_mass': 22.9898,
        'name': '',
        'symbol': 'Na'
        },
    'Nb': {
        'atomic_number': 41,
        'molar_mass': 92.9064,
        'name': '',
        'symbol': 'Nb'
        },
    'Nd': {
        'atomic_number': 60,
        'molar_mass': 144.24,
        'name': '',
        'symbol': 'Nd'
        },
    'Ne': {
        'atomic_number': 10,
        'molar_mass': 20.179,
        'name': '',
        'symbol': 'Ne'
        },
    'Ni': {
        'atomic_number': 28,
        'molar_mass': 58.69,
        'name': '',
        'symbol': 'Ni'
        },
    'Np': {
        'atomic_number': 93,
        'molar_mass': 237.048,
        'name': '',
        'symbol': 'Np'
        },
    'O': {
        'atomic_number': 8,
        'molar_mass': 15.9994,
        'name': '',
        'symbol': 'O'
        },
    'Os': {
        'atomic_number': 76,
        'molar_mass': 190.20,
        'name': '',
        'symbol': 'Os'
        },
    'P': {
        'atomic_number': 15,
        'molar_mass': 30.9738,
        'name': '',
        'symbol': 'P'
        },
    'Pa': {
        'atomic_number': 91,
        'molar_mass': 231.036,
        'name': '',
        'symbol': 'Pa'
        },
    'Pb': {
        'atomic_number': 82,
        'molar_mass': 207.20,
        'name': '',
        'symbol': 'Pb'
        },
    'Pd': {
        'atomic_number': 46,
        'molar_mass': 106.42,
        'name': '',
        'symbol': 'Pd'
        },
    'Pm': {
        'atomic_number': 61,
        'molar_mass': 144.913,
        'name': '',
        'symbol': 'Pm'
        },
    'Po': {
        'atomic_number': 84,
        'molar_mass': 208.982,
        'name': '',
        'symbol': 'Po'
        },
    'Pr': {
        'atomic_number': 59,
        'molar_mass': 140.908,
        'name': '',
        'symbol': 'Pr'
        },
    'Pt': {
        'atomic_number': 78,
        'molar_mass': 195.08,
        'name': '',
        'symbol': 'Pt'
        },
    'Pu': {
        'atomic_number': 94,
        'molar_mass': 239.052,
        'name': '',
        'symbol': 'Pu'
        },
    'Ra': {
        'atomic_number': 88,
        'molar_mass': 226.025,
        'name': '',
        'symbol': 'Ra'
        },
    'Rb': {
        'atomic_number': 37,
        'molar_mass': 85.4678,
        'name': '',
        'symbol': 'Rb'
        },
    'Re': {
        'atomic_number': 75,
        'molar_mass': 186.207,
        'name': '',
        'symbol': 'Re'
        },
    'Rh': {
        'atomic_number': 45,
        'molar_mass': 102.906,
        'name': '',
        'symbol': 'Rh'
        },
    'Rn': {
        'atomic_number': 86,
        'molar_mass': 222.018,
        'name': '',
        'symbol': 'Rn'
        },
    'Ru': {
        'atomic_number': 44,
        'molar_mass': 101.07,
        'name': '',
        'symbol': 'Ru'
        },
    'S': {
        'atomic_number': 16,
        'molar_mass': 32.06,
        'name': '',
        'symbol': 'S'
        },
    'Sb': {
        'atomic_number': 51,
        'molar_mass': 121.75,
        'name': '',
        'symbol': 'Sb'
        },
    'Sc': {
        'atomic_number': 21,
        'molar_mass': 44.9559,
        'name': '',
        'symbol': 'Sc'
        },
    'Se': {
        'atomic_number': 34,
        'molar_mass': 78.96,
        'name': '',
        'symbol': 'Se'
        },
    'Si': {
        'atomic_number': 14,
        'molar_mass': 28.0855,
        'name': '',
        'symbol': 'Si'
        },
    'Sm': {
        'atomic_number': 62,
        'molar_mass': 150.36,
        'name': '',
        'symbol': 'Sm'
        },
    'Sn': {
        'atomic_number': 50,
        'molar_mass': 118.69,
        'name': '',
        'symbol': 'Sn'
        },
    'Sr': {
        'atomic_number': 38,
        'molar_mass': 87.620,
        'name': '',
        'symbol': 'Sr'
        },
    'Ta': {
        'atomic_number': 73,
        'molar_mass': 180.948,
        'name': '',
        'symbol': 'Ta'
        },
    'Tb': {
        'atomic_number': 65,
        'molar_mass': 158.925,
        'name': '',
        'symbol': 'Tb'
        },
    'Tc': {
        'atomic_number': 43,
        'molar_mass': 97.907,
        'name': '',
        'symbol': 'Tc'
        },
    'Te': {
        'atomic_number': 52,
        'molar_mass': 127.60,
        'name': '',
        'symbol': 'Te'
        },
    'Th': {
        'atomic_number': 90,
        'molar_mass': 232.038,
        'name': '',
        'symbol': 'Th'
        },
    'Ti': {
        'atomic_number': 22,
        'molar_mass': 47.88,
        'name': '',
        'symbol': 'Ti'
        },
    'Tl': {
        'atomic_number': 81,
        'molar_mass': 204.383,
        'name': '',
        'symbol': 'Tl'
        },
    'Tm': {
        'atomic_number': 69,
        'molar_mass': 168.934,
        'name': '',
        'symbol': 'Tm'
        },
    'U': {
        'atomic_number': 92,
        'molar_mass': 238.051,
        'name': '',
        'symbol': 'U'
        },
    'V': {
        'atomic_number': 23,
        'molar_mass': 50.9415,
        'name': '',
        'symbol': 'V'
        },
    'W': {
        'atomic_number': 74,
        'molar_mass': 183.85,
        'name': '',
        'symbol': 'W'
        },
    'Xe': {
        'atomic_number': 54,
        'molar_mass': 131.29,
        'name': '',
        'symbol': 'Xe'
        },
    'Y': {
        'atomic_number': 39,
        'molar_mass': 88.9059,
        'name': '',
        'symbol': 'Y'
        },
    'Yb': {
        'atomic_number': 70,
        'molar_mass': 173.04,
        'name': '',
        'symbol': 'Yb'
        },
    'Zn': {
        'atomic_number': 30,
        'molar_mass': 65.38,
        'name': '',
        'symbol': 'Zn'
        },
    'Zr': {
        'atomic_number': 40,
        'molar_mass': 91.22,
        'name': '',
        'symbol': 'Zr'
        }
    }
