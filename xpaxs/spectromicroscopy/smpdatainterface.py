"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy
import Queue

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore, QtGui # gui for testing only
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.datalib.hdf5 import XpaxsScanInterface

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class SmpScanInterface(XpaxsScanInterface):

    def __init__(self, h5Entry, mutex, parent=None):
        super(SmpScanInterface, self).__init__(h5Entry, mutex, parent)

    def initializeElementMaps(self, elements):
        shape = self.getScanShape()
        filters = self.getH5Filters()
        try:
            self.mutex.lock()
            try:
                self.h5File.removeNode(self.h5Entry, 'elementMaps',
                                       recursive=True)
                self.h5File.flush()
            except tables.NoSuchNodeError:
                pass
            elementMaps = self.h5File.createGroup(self.h5Entry, 'elementMaps')
            for mapType in ['fitArea', 'massFraction', 'sigmaArea']:
                self.h5File.createGroup(elementMaps, mapType)
                for element in elements:
                    node = self.h5File.getNode(self.h5Entry.elementMaps,
                                               mapType)
                    self.h5File.createCArray(node,
                                             element.replace(' ', ''),
                                             tables.Float32Atom(),
                                             shape,
                                             filters=filters)
            self.h5File.flush()
        finally:
            self.mutex.unlock()

    def getAvailableElements(self):
        try:
            self.mutex.lock()
            elements = [el for el in self.h5Entry.elementMaps.fitArea._v_leaves.keys()]
        except tables.NoSuchNodeError:
            return []
        finally:
            self.mutex.unlock()
        elements.sort()
        return elements

    def getElementMap(self, mapType, element, normalization=None):
        dataPath = '/'.join(['elementMaps', mapType, element])
        try:
            self.mutex.lock()
            try:
                elementMap = self.h5File.getNode(self.h5Entry,
                                                          dataPath)[:]
            except tables.NoSuchNodeError:
                print dataPath
                return numpy.zeros(self.getScanShape())
        finally:
            self.mutex.unlock()
        if normalization:
            # TODO: this if is a wart:
            if normalization == 'Dead time %':
                try:
                    self.mutex.lock()
                    norm = getattr(self.h5Entry.data.cols, 'Dead')[:]
                finally:
                    self.mutex.unlock()
                norm = 1-norm/100
            else:
                try:
                    self.mutex.lock()
                    norm = getattr(self.h5Entry.data.cols, normalization)[:]
                finally:
                    self.mutex.unlock()
            elementMap.flat[:len(norm)] /= norm
        return elementMap

    def getMcaSpectrum(self, index, id='MCA'):
        try:
            self.mutex.lock()
            return self.h5Entry.data[index][id][:]
        finally:
            self.mutex.unlock()

    def getMcaChannels(self, id='MCA'):
        try:
            self.mutex.lock()
            mcaMetaData = getattr(self.h5Entry, id)
            return mcaMetaData.channels[:]
        finally:
            self.mutex.unlock()

    def getNormalizationChannels(self):
        try:
            self.mutex.lock()
            channels = [i for i in self.h5Entry.data.colnames
                        if not i in self.h5Entry._v_attrs]
        finally:
            self.mutex.unlock()
        channels.insert(0, 'Dead time %')
        return channels

    def getPymcaConfig(self):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.pymcaConfig
        finally:
            self.mutex.unlock()

    def setPymcaConfig(self, config):
        try:
            self.mutex.lock()
            self.h5Entry._v_attrs.pymcaConfig = config
        finally:
            self.mutex.unlock()

    def getSkipmode(self):
        try:
            self.mutex.lock()
            mon = self.h5Entry._v_attrs.skipmodeMonitor
            thresh = self.h5Entry._v_attrs.skipmodeThresh
            return (mon, thresh)
        except AttributeError:
            return (None, 0)
        finally:
            self.mutex.unlock()

    def setSkipmode(self, monitor=None, thresh=0):
        try:
            self.mutex.lock()
            self.h5Entry._v_attrs.skipmodeMonitor = monitor
            self.h5Entry._v_attrs.skipmodeThresh = thresh
        finally:
            self.mutex.unlock()

    def updateElementMap(self, mapType, element, index, val):
        node = '/'.join(['elementMaps', mapType, element])
        try:
            self.mutex.lock()
            try:
                self.h5File.getNode(self.h5Entry, node)[index] = val
            except ValueError:
                print index, node
        finally:
            self.mutex.unlock()
