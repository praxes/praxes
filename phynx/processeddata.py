"""
"""

from __future__ import absolute_import

import posixpath

from .dataset import Dataset
from .group import Group
from .utils import sync


class ProcessedData(Group):

    """
    """

    @property
    @sync
    def fits(self):
        return dict(
            [(posixpath.split(s.name)[-1].rstrip('_fit'), s)
                for s in self.iterobjects() if isinstance(s, Fit)]
        )

    @property
    @sync
    def fit_errors(self):
        return dict(
            [(posixpath.split(s.name)[-1].rstrip('_fit_error'), s)
                for s in self.iterobjects() if isinstance(s, FitError)]
        )


class ElementMaps(ProcessedData):

    """
    """

    @property
    @sync
    def mass_fractions(self):
        return dict(
            [(posixpath.split(s.name)[-1].rstrip('_mass_fraction'), s)
                for s in self.iterobjects() if isinstance(s, MassFraction)]
        )


class FitResult(Dataset):

    """
    """

    @sync
    def __cmp__(self, other):
        return cmp(
            posixpath.split(self.name)[-1], posixpath.split(other.name)[-1]
        )


class Fit(FitResult):

    """
    """

    pass


class FitError(FitResult):

    """
    """

    pass


class MassFraction(FitResult):

    """
    """

    pass
