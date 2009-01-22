"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .dataset import Dataset
from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ProcessedData(Group):

    """
    """

    @property
    def fits(self):
        with self._lock:
            return dict(
                [(s.name.rstrip('_fit'), s) for s in self.iterobjects()
                    if isinstance(s, Fit)]
            )

    @property
    def fit_errors(self):
        with self._lock:
            return dict(
                [(s.name.rstrip('_fit_error'), s) for s in self.iterobjects()
                    if isinstance(s, FitError)]
            )

registry.register(ProcessedData)


class ElementMaps(ProcessedData):

    """
    """

    @property
    def mass_fractions(self):
        with self._lock:
            return dict(
                [(s.name.rstrip('_mass_fraction'), s)
                    for s in self.iterobjects() if isinstance(s, MassFraction)]
            )

registry.register(ElementMaps)


class FitResult(Dataset):

    """
    """

    def __cmp__(self, other):
        return cmp(self.name, other.name)


class Fit(FitResult):

    """
    """

    pass

registry.register(Fit)


class FitError(FitResult):

    """
    """

    pass

registry.register(FitError)


class MassFraction(FitResult):

    """
    """

    pass

registry.register(MassFraction)

