import textwrap

import quantities as pq

from praxes.lib.decorators import memoize
from praxes.physref.lib.mapping import Mapping


class XrayLevel(Mapping):

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

    @Mapping._keys.getter
    @memoize
    def _keys(self):
        cursor = self.__db.cursor()
        res = cursor.execute(
            '''select iupac_symbol from xray_transitions
            where element=? and initial_level=? order by iupac_symbol''',
            (self._element_symbol, self._iupac_symbol)
            )
        return tuple(i[0].split('-')[1] for i in res)

    @property
    def ck_probabilities(self):
        """A dictionary containing the probabilities of Coster Kronig
        transitions to the given final state
        """
        try:
            return collections.OrderedDict(self._ck_probabilities)
        except AttributeError:
            c = self.__db.cursor()
            items = c.execute(
                '''select final_level, transition_probability from Coster_Kronig
                where element=? and initial_level=? order by final_level''',
                (self._element_symbol, self._iupac_symbol)
                )
            self._ck_probabilities = tuple(items)
            return collections.OrderedDict(self._ck_probabilities)


    @property
    def ck_total_probabilities(self):
        """A dictionary containing the probabilities of Coster Kronig
        transitions to the given final state, including pathways through
        intermediate states
        """
        try:
            return collections.OrderedDict(self._ck_total_probabilities)
        except AttributeError:
            c = self.__db.cursor()
            items = c.execute(
                '''select final_level, total_transition_probability
                from Coster_Kronig
                where element=? and initial_level=? order by final_level''',
                (self._element_symbol, self._iupac_symbol)
                )
            self._ck_total_probabilities = tuple(items)
            return collections.OrderedDict(self._ck_total_probabilities)

    @property
    def element(self):
        "The element to which this x-ray level applies"
        from .element import Element
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

    def __hash__(self):
        return hash((type(self), self._iupac_symbol))

    def __getitem__(self, item):
        iupac = '-'.join([self.iupac_symbol, item])
        if not item in self.keys():
            raise KeyError('Transition "%s" not recognized' % item)
        from .transition import Transition
        return Transition(self._element_symbol, iupac, self.__db)

    def get(self, item, default=None):
        "Return the value for *key*, or return *default*"
        return self[item] if item in self else None

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
