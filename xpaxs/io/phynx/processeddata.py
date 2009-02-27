"""
"""

from __future__ import absolute_import

from .dataset import Dataset
from .group import Group
from .registry import registry
from .utils import sync


class ProcessedData(Group):

    """
    """

    @property
    @sync
    def fits(self):
        return dict(
            [(s.name.rstrip('_fit'), s) for s in self.iterobjects()
                if isinstance(s, Fit)]
        )

    @property
    @sync
    def fit_errors(self):
        return dict(
            [(s.name.rstrip('_fit_error'), s) for s in self.iterobjects()
                if isinstance(s, FitError)]
        )

registry.register(ProcessedData)


class ElementMaps(ProcessedData):

    """
    """

    @property
    @sync
    def mass_fractions(self):
        return dict(
            [(s.name.rstrip('_mass_fraction'), s)
                for s in self.iterobjects() if isinstance(s, MassFraction)]
        )

registry.register(ElementMaps)


class FitResult(Dataset):

    """
    """

    @sync
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

