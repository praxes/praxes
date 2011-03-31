import os
import sqlite3

from .base import Mapping

class AtomicData(Mapping):

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
        from .element import Element
        return Element(item, self.__db)

    def __hash__(self):
        return hash((type(self), self.__db))

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
