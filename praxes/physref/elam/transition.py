import textwrap

import quantities as pq

from .base import memoize


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
        from .xraylevel import XrayLevel
        return XrayLevel(
            self._element_symbol, self._get_data('final_level'), self.__db
            )

    @property
    def initial_level(self):
        "x-ray level before transition"
        from .xraylevel import XrayLevel
        return XrayLevel(
            self._element_symbol, self._get_data('initial_level'), self.__db
            )

    @property
    def element(self):
        "The element in which the x-ray transition occurs"
        from .element import Element
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

    def __hash__(self):
        return hash((type(self), self._iupac_symbol))

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
