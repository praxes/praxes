"""
"""

from __future__ import absolute_import

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .group import Group
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class AcquisitionIterator(object):

    def __init__(self, detector, dataset):
        self._currentIndex = 0
        self._totalSkipped = 0
        self._detector = detector
        self._dataset = dataset

    def __iter__(self):
        return self

    @property
    def currentIndex(self):
        return self._currentIndex

    @property
    def totalSkipped(self):
        return self._totalSkipped

    def next(self):
        if self._currentIndex >= self._dataset.npoints:
            raise StopIteration

        else:
            try:
                if self._detector.is_valid_index(self._currentIndex):
                    i = self._currentIndex
                    data = self._dataset[i]
                    try:
                        norm = self._detector.normalization_channel
                        data /= self._detector[norm][i]
                    except TypeError:
                        pass
                    self._currentIndex += 1

                    return i, data

                else:
                    self._currentIndex += 1
                    self._totalSkipped += 1
                    return self.next()

            except h5py.H5Error:
                raise IndexError


class Detector(Group):

    """
    """

    nx_class = 'NXdetector'

    @property
    def device_id(self):
        try:
            return self.attrs['id']
        except h5py.H5Error:
            return self.name

    @property
    def normalization(self):
        try:
            norm = self.attrs['normalization']
            if norm in ('', 'None'):
                return None
            return self[norm].value
        except h5py.H5Error:
            return None

    def _get_normalization_channel(self):
        try:
            return self.attrs['normalization']
        except h5py.H5Error:
            return None
    def _set_normalization_channel(self, norm):
        if norm in ('None', None):
            norm = ''
        try:
            if norm:
                assert norm in self
        except AssertionError:
            raise RuntimeError('Invalid normalization channel %s' % norm)
        self.attrs['normalization'] = norm
    normalization_channel = property(
        _get_normalization_channel, _set_normalization_channel
    )

    def itercounts(self):
        return AcquisitionIterator(self, self['counts'])

    def get_averaged_counts(self, indices=[]):
        with self._lock:
            if len(indices) > 0:
                result = numpy.zeros(len(self['counts'][indices[0]]), 'f')
                numIndices = len(indices)
                for index in indices:
                    if not self.is_valid_index(index):
                        continue
                    temp = self['counts'][index]
                    if self.normalization is not None:
                        norm = self.normalization[index]
                        temp /= numpy.where(norm==0, numpy.inf, norm)
                    result += temp
                return result / len(indices)

registry.register(Detector)
