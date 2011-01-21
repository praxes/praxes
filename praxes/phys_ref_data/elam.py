# -*- coding: utf-8 -*-
'''
The elam module is an interface to a database of fundamental X-ray fluorescence
parameters compiled by W.T. Elam, B.D. Ravel and J.R. Sieber, and published in
Radiation Physics and Chemistry, 63 (2), 121 (2002). The database is published
by NIST at http://www.nist.gov/mml/analytical/inorganic/xrf.cfm.
'''

from collections import OrderedDict
import json
import os
import sqlite3
import textwrap

import numpy as np
import quantities as pq

from praxes.decorators import memoize


class _DictCompat(object):

    def __contains__(self, item):
        return item in self.keys()

    def __getitem__(self, item):
        raise NotImplementedError

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def get(self, item, default=None):
        "Return the value for *key*, or return *default*"
        return self[item] if item in self else None

    def items(self):
        "Return a new view of the (key, value) pairs"
        return zip(self.keys(), self.values())

    def keys(self):
        raise NotImplementedError

    def values(self):
        "return a new view of the values"
        return [self[i] for i in self.keys()]


class AtomicData(_DictCompat):

    "A dict-like interface to the Elam database"

    __slots__ = ['__db', '_keys']

    @property
    def db(self):
        """
        A new cursor to the sqlite database connection, providing access to the
        underlying sql database. For example::

           >>> atomic_data.db.execute(
               '''select element from elements where atomic_number<20'''
               ).fetchall()

        The database provides the following tables:

        elements
           #. atomic_number (integer)
           #. element (text)
           #. molar_mass (real, g/mol)
           #. density (real, g/cm^3)

        xray_levels
           #. id (integer)
           #. element (text)
           #. iupac_symbol (text)
           #. absoprtion_edge (real, eV)
           #. fluorescence_yield (real)
           #. jump_ratio (real)

        xray_transitions
           #. id (integer)
           #. element (text)
           #. iupac_symbol (text)
           #. siegbahn_symbol (text)
           #. initial_level (text)
           #. final_level (text)
           #. emission_energy (real, eV)
           #. intensity (real)

        Coster_Kronig
           #. id (integer)
           #. element (text)
           #. intitial_level (text)
           #. final_level (text)
           #. transition_probability (real)
           #. total_transition_probability (real)

        photoabsorption
           #. id (integer)
           #. element (text)
           #. log_energy (text, eV when exponentiated) [#f1]_
           #. log_photoabsorption (text, cm^2/g when exponentiated) [#f1]_
           #. log_photoabsorption_spline (text) [#f1]_

        scattering
           #. id (integer)
           #. element (text)
           #. log_energy (text, eV when exponentiated) [#f1]_
           #. log_coherent_scatter (text, cm^2/g when exponentiated) [#f1]_
           #. log_coherent_scatter_spline (text) [#f1]_
           #. log_incoherent_scatter (text, cm^2/g when exponentiated) [#f1]_
           #. log_incoherent_scatter_spline (text) [#f1]_

        .. rubric:: Footnotes

        .. [#f1] use json.loads() to recover a list of numerical values
        """
        return self.__db.cursor()

    def __init__(self):
        self.__db = sqlite3.connect(
            os.path.join(os.path.split(__file__)[0], 'elam.db')
            )

    def __getitem__(self, item):
        if item not in self.keys():
            raise KeyError('Element "%s" not recognized' % item)
        return Element(item, self.__db)

    def keys(self):
        "return a new view of the keys"
        try:
            return list(self._keys)
        except AttributeError:
            cursor = self.__db.cursor()
            results = cursor.execute(
                '''select element from elements order by atomic_number'''
                )
            self._keys = tuple(i[0] for i in results)
            return list(self._keys)

atomic_data = AtomicData()


class Transition(object):

    """
    The following is quoted verbatim from the elamdb source file:

       Relative emission rates, fits to low-order polynomials, low-Z
       extrapolations by hand and eye data from Salem, Panossian, and
       Krause, Atomic Data and Nuclear Data Tables Vol. 14 No.2 August
       1974, pp92-109. M shell data is from T. P. Schreiber and A. M.
       Wims, X-ray Spectrometry Vol. 11, No. 2, 1982, pp42-45. Small,
       arbitrary intensities assigned to Mgamma and Mzeta lines.
    """

    __slots__ = ['__db', '_element_symbol', '_iupac_symbol']

    def _get_data(self, id):
        cursor = self.__db.cursor()
        result = cursor.execute(
            '''select %s from xray_transitions
            where element=? and iupac_symbol=?''' % id,
            (self._element_symbol, self._iupac_symbol)
            ).fetchone()
        return result[0]

    @property
    def final_level(self):
        "x-ray level after transition"
        return XrayLevel(
            self._element_symbol, self._get_data('final_level'), self.__db
            )

    @property
    def initial_level(self):
        "x-ray level before transition"
        return XrayLevel(
            self._element_symbol, self._get_data('initial_level'), self.__db
            )

    @property
    def element(self):
        "The element in which the x-ray transition occurs"
        return Element(self._element_symbol, self.__db)

    @property
    @memoize
    def emission_energy(self):
        "The energy of the emitted x ray, in eV"
        return self._get_data('emission_energy') * pq.eV

    @property
    @memoize
    def intensity(self):
        "The relative intensity of the emission line"
        return self._get_data('intensity')

    @property
    def iupac_symbol(self):
        "The IUPAC symbol for the transition"
        return self._iupac_symbol

    @property
    @memoize
    def siegbahn_symbol(self):
        "The Siegbahn symbol for the transition"
        return self._get_data('Siegbahn_symbol')

    def __init__(self, element, iupac, db):
        self.__db = db
        self._element_symbol = element
        self._iupac_symbol = iupac

    @memoize
    def __repr__(self):
        return "<Transition(%s, %s)>" % (
            self._element_symbol, self._iupac_symbol
            )

    @memoize
    def __str__(self):
        return textwrap.dedent(
            """\
            Transition(%s, %s)
              emission energy: %s
              intensity: %s
              Siegbahn symbol: %s""" % (
                self._element_symbol,
                self._iupac_symbol,
                self.emission_energy,
                self.intensity,
                self.siegbahn_symbol,
                )
            )


class XrayLevel(_DictCompat):

    """
    The following is quoted verbatim from the elamdb source file:

       K-shell fluorescence yield below Z=11 from new fits in J. H.
       Hubbell et. al., J. Chem. Phys. Ref. Data, Vol. 23, No. 2, 1994,
       pp339-364. Fluorescence yields and Coster-Kronig transition
       rates for K and L shells Krause, J. Phys. Chem. Ref. Data, Vol.
       8, No. 2, 1979, pp307-327. Values for wK, wL2,and f23 are from
       Table 1. (values for light atoms in condensed matter) (note that
       this produces a large step in f23 values at z=30, see discussion
       in reference section 5.3 L2 Subshell and section 7 last
       paragraph)

       Values of wL1 for Z=85-110 and f12 for Z=72-96 from Krause were
       modified as suggested by W. Jitschin, "Progress in Measurements
       of L-Subshell Fluorescence, Coster-Kronig, and Auger Values", AIP
       Conference Proceedings 215, X-ray and Inner-Shell Processes,
       Knoxville, TN, 1990. T. A. Carlson, M. O. Krause, and S. T.
       Manson, Eds. (American Institute of Physics, 1990).

       Fluorescence yields and Coster-Kronig transition rates for M
       shells Eugene J. McGuire, "Atomic M-Shell Coster-Kronig, Auger,
       and Radiative Rates, and Fluorescence Yields for Ca-Th", Physical
       Review A, Vol. 5, No. 3, March 1972, pp1043-1047.

       Fluorescence yields and Coster-Kronig transition rates for N
       shells Eugene J. McGuire, "Atomic N-shell Coster-Kronig, Auger,
       and Radiative Rates and Fluorescence Yields for 38 <= Z <= 103",
       Physical Review A 9, No. 5, May 1974, pp1840-1851. Values for
       Z=38 to 50 were adjusted according to instructions on page 1845,
       at the end of Section IV.a., and the last sentence of the
       conclusions.
    """

    __slots__ = [
        '__db', '_element_symbol', '_iupac_symbol', '_ck_probabilities',
        '_ck_total_probabilities', '_keys'
        ]

    def _get_data(self, id):
        cursor = self.__db.cursor()
        result = cursor.execute('''select %s from xray_levels
            where element=? and iupac_symbol=?''' % id,
            (self._element_symbol, self._iupac_symbol)
            ).fetchone()
        return result[0]

    @property
    def ck_probabilities(self):
        """A dictionary containing the probabilities of Coster Kronig
        transitions to the given final state
        """
        try:
            return OrderedDict(self._ck_probabilities)
        except AttributeError:
            c = self.__db.cursor()
            items = c.execute(
                '''select final_level, transition_probability from Coster_Kronig
                where element=? and initial_level=? order by final_level''',
                (self._element_symbol, self._iupac_symbol)
                )
            self._ck_probabilities = tuple(items)
            return OrderedDict(self._ck_probabilities)


    @property
    def ck_total_probabilities(self):
        """A dictionary containing the probabilities of Coster Kronig
        transitions to the given final state, including pathways through
        intermediate states
        """
        try:
            return OrderedDict(self._ck_total_probabilities)
        except AttributeError:
            c = self.__db.cursor()
            items = c.execute(
                '''select final_level, total_transition_probability
                from Coster_Kronig
                where element=? and initial_level=? order by final_level''',
                (self._element_symbol, self._iupac_symbol)
                )
            self._ck_total_probabilities = tuple(items)
            return OrderedDict(self._ck_total_probabilities)

    @property
    def element(self):
        "The element to which this x-ray level applies"
        return Element(self._element_symbol, self.__db)

    @property
    @memoize
    def absorption_edge(self):
        "The absorption edge for the x-ray level, in eV"
        return self._get_data('absorption_edge') * pq.eV

    @property
    @memoize
    def fluorescence_yield(self):
        "The fluorescence yield for the x-ray level"
        return self._get_data('fluorescence_yield')

    @property
    @memoize
    def jump_ratio(self):
        "The jump ratio for the x-ray level"
        return self._get_data('jump_ratio')

    @property
    def iupac_symbol(self):
        "The IUPAC symbol for the x-ray level"
        return self._iupac_symbol

    def __init__(self, element, iupac_symbol, db):
        self.__db = db
        self._element_symbol = element
        self._iupac_symbol = iupac_symbol

    def __getitem__(self, item):
        iupac = '-'.join([self.iupac_symbol, item])
        if not item in self.keys():
            raise KeyError('Transition "%s" not recognized' % item)
        return Transition(self._element_symbol, iupac, self.__db)

    def get(self, item, default=None):
        "Return the value for *key*, or return *default*"
        return self[item] if item in self else None

    def keys(self):
        "return a new view of the keys for reported transitions"
        try:
            return list(self._keys)
        except AttributeError:
            cursor = self.__db.cursor()
            results = cursor.execute(
                '''select iupac_symbol from xray_transitions
                where element=? and initial_level=? order by iupac_symbol''',
                (self._element_symbol, self._iupac_symbol)
                )
            self._keys = tuple(i[0].split('-')[1] for i in results)
            return list(self._keys)

    @memoize
    def __repr__(self):
        return "<XrayLevel(%s, %s)>" % (
            self._element_symbol, self._iupac_symbol
            )

    @memoize
    def __str__(self):
        return textwrap.dedent(
            """\
            XrayLevel(%s, %s)
              absorption edge: %s
              flourescence yield: %s
              jump ratio: %s
              Coster Kronig probabilities: %s
              Coster Kronig total probabilities: %s
              transitions: %s""" % (
                self._element_symbol,
                self._iupac_symbol,
                self.absorption_edge,
                self.fluorescence_yield,
                self.jump_ratio,
                self.ck_probabilities.items(),
                self.ck_total_probabilities.items(),
                self.keys()
                )
            )


class Element(object):

    """
    """

    __slots__ = ['__db', '_symbol', '_keys']

    def _get_data(self, id):
        cursor = self.__db.cursor()
        result = cursor.execute('''select %s from elements
            where element=?''' % id, (self._symbol, )
            ).fetchone()
        assert result is not None
        return result[0]

    @property
    @memoize
    def atomic_mass(self):
        "The average atomic mass of the element, in atomic mass units"
        return (self.molar_mass / pq.constants.N_A).rescale('amu')

    @property
    @memoize
    def atomic_number(self):
        "The atomic number"
        return self._get_data('atomic_number')

    @property
    @memoize
    def _coherent_scatter(self):
        return CoherentScatter(self._symbol, self.__db)

    @property
    @memoize
    def _incoherent_scatter(self):
        return IncoherentScatter(self._symbol, self.__db)

    @property
    @memoize
    def mass_density(self):
        """
        The theoretical solid mass density at standard temperature and
        pressure, regardless of state, in g/cm^3.
        """
        return self._get_data('density') * pq.g / pq.cm**3

    @property
    @memoize
    def molar_mass(self):
        "The molar mass of the element"
        return self._get_data('molar_mass') * pq.g / pq.mol

    @property
    @memoize
    def _photoabsorption(self):
        return Photoabsorption(self._symbol, self.__db)

    @property
    def symbol(self):
        return self._symbol

    def __init__(self, symbol, db):
        """
        symbol is a string, like 'Ca' or 'S'
        """
        self.__db = db
        self._symbol = symbol

    def __getitem__(self, item):
        if not item in self.keys():
            raise KeyError('x-ray level "%s" not recognized' % item)
        return XrayLevel(self._symbol, item, self.__db)

    def keys(self):
        "return a new view of the keys for the reported x-ray levels"
        try:
            return list(self._keys)
        except AttributeError:
            cursor = self.__db.cursor()
            results = cursor.execute(
                '''select iupac_symbol from xray_levels where element=?
                order by absorption_edge desc''',
                (self._symbol,)
                )
            self._keys = tuple(i[0] for i in results)
            return list(self._keys)

    @memoize
    def __repr__(self):
        return "<Element(%s)>" % self.symbol

    @memoize
    def __str__(self):
        return textwrap.dedent(
            """\
            Element(%s)
              mass density: %s
              molar mass: %s
              x-ray levels: %s""" % (
                self.symbol,
                self.mass_density,
                self.molar_mass,
                self.keys()
                )
            )

    def photoabsorption_cross_section(self, energy, mass=True):
        """
        Return the photoabsorption cross section as a function of
        energy. The energy must be within the range 100 < E < 8e5 eV.

        Cross-sections at energies below 250 eV should not be considered
        reliable.

        If *mass* is True, return the cross-section per gram in cm^2/g.
        If *mass* is False, return the cross-section per atom in cm^2.
        """
        res = self._photoabsorption(energy)
        if not mass:
            res *= self.atomic_mass.rescale('g')
        return res

    def coherent_scattering_cross_section(self, energy, mass=True):
        """
        Return the coherent-scattering cross section in cm^2/g as a function of
        energy. The energy must be within the range 100 < E < 8e5 eV.

        Cross-sections at energies below 250 eV should not be considered
        reliable.

        If *mass* is True, return the cross-section per gram in cm^2/g.
        If *mass* is False, return the cross-section per atom in cm^2.
        """
        res = self._coherent_scatter(energy)
        if not mass:
            res *= self.atomic_mass.rescale('g')
        return res

    def incoherent_scattering_cross_section(self, energy, mass=True):
        """
        Return the incoherent-scattering cross section in cm^2/g as a function
        of energy. The energy must be within the range 100 < E < 8e5 eV.

        Cross-sections at energies below 250 eV should not be considered
        reliable.

        If *mass* is True, return the cross-section per gram in cm^2/g.
        If *mass* is False, return the cross-section per atom in cm^2.
        """
        res = self._incoherent_scatter(energy)
        if not mass:
            res *= self.atomic_mass.rescale('g')
        return res


class SplineInterpolable(object):

    __slots__ = ['_db', '_element']

    @property
    def element(self):
        return self._element

    @property
    @memoize
    def _log_independant_value(self):
        return self._get_data('log_energy')

    def _splint(self, xa, ya, y2a, x):
        '''spline interpolation'''
        try:
            len(x)
        except TypeError:
            x = np.array([x])

        try:
            klo, khi = np.array([
                (np.flatnonzero(xa < i)[-1], np.flatnonzero(xa > i)[0])
                for i in x
                ]).transpose()
        except IndexError:
            raise ValueError(
                'Input values must be between %s and %s'
                % (np.exp(xa[0]), np.exp(xa[-1]))
                )

        h = xa[khi] - xa[klo]
        if any(h <= 0):
            raise ValueError, 'xa input must be strictly increasing'
        a = (xa[khi] - x) / h
        b = (x - xa[klo]) / h

        res = (
            a * ya[klo]
            + b * ya[khi]
            + ((a**3 - a) * y2a[klo] + (b**3 - b) * y2a[khi]) * (h**2) / 6
            )
        return res


    def __init__(self, element, db):
        self._db = db
        self._element = element

    def __call__(self, energy):
        log_energy = np.log(energy.rescale('eV').magnitude)
        log_xa = self._log_independant_value
        log_ya = self._log_dependant_value
        log_yspline = self._log_dependant_value_spline

        log_res = self._splint(log_xa, log_ya, log_yspline, log_energy)
        return np.exp(log_res) * pq.cm**2 / pq.g


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


class Scatter(SplineInterpolable):

    def _get_data(self, id):
        cursor = self._db.cursor()
        result = cursor.execute('''select %s from scattering
            where element=?''' % id, (self.element, )
            ).fetchone()
        return np.array(json.loads(result[0]))


class CoherentScatter(Scatter):

    @property
    @memoize
    def _log_dependant_value(self):
        return self._get_data('log_coherent_scatter')

    @property
    @memoize
    def _log_dependant_value_spline(self):
        return self._get_data('log_coherent_scatter_spline')


class IncoherentScatter(Scatter):

    @property
    @memoize
    def _log_dependant_value(self):
        return self._get_data('log_incoherent_scatter')

    @property
    @memoize
    def _log_dependant_value_spline(self):
        return self._get_data('log_incoherent_scatter_spline')
