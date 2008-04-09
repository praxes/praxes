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

from xpaxs.datalib.hdf5 import XpaxsFile, XpaxsScan

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class SmpFile(XpaxsFile):

    def getNode(self, where, name=None):
        node = self.h5File.getNode(where, name)
        # TODO: these checks should eventually look for nexus classes
        # for now just use the pytables classes
        if isinstance(node, tables.Group):
            return SmpScan(node, self)


class SmpScan(XpaxsScan):

    def initializeElementMaps(self, elements):
        shape = self.getScanShape()
        filters = self.getH5Filters()
        try:
            self.mutex.lock()
            try:
                self.h5Node._v_file.removeNode(self.h5Node, 'elementMaps',
                                       recursive=True)
                self.flush()
            except tables.NoSuchNodeError:
                pass
            elementMaps = self.h5Node._v_file.createGroup(self.h5Node,
                                                          'elementMaps')
            for mapType in ['fitArea', 'massFraction', 'sigmaArea']:
                self.h5Node._v_file.createGroup(elementMaps, mapType)
                for element in elements:
                    node = self.h5Node._v_file.getNode(self.h5Node.elementMaps,
                                               mapType)
                    self.h5Node._v_file.createCArray(node,
                                             element.replace(' ', ''),
                                             tables.Float32Atom(),
                                             shape,
                                             filters=filters)
            self.flush()
        finally:
            self.mutex.unlock()

    def getAvailableElements(self):
        try:
            self.mutex.lock()
            elements = self.h5Node.elementMaps.fitArea._v_leaves.keys()
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
                elementMap = self.h5Node._v_file.getNode(self.h5Node, dataPath)[:]
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
                    norm = getattr(self.h5Node.data.cols, 'Dead')[:]
                finally:
                    self.mutex.unlock()
                norm = 1-norm/100
            else:
                try:
                    self.mutex.lock()
                    norm = getattr(self.h5Node.data.cols, normalization)[:]
                finally:
                    self.mutex.unlock()
            elementMap.flat[:len(norm)] /= norm
        return elementMap

    def getMcaSpectrum(self, index, id='MCA'):
        try:
            self.mutex.lock()
            return self.h5Node.data[index][id]
        finally:
            self.mutex.unlock()

    def getMcaChannels(self, id='MCA'):
        try:
            self.mutex.lock()
            mcaMetaData = getattr(self.h5Node, id)
            return mcaMetaData.channels[:]
        finally:
            self.mutex.unlock()

    def getNormalizationChannels(self):
        try:
            self.mutex.lock()
            channels = [i for i in self.h5Node.data.colnames
                        if not i in self.h5Node._v_attrs]
        finally:
            self.mutex.unlock()
        channels.insert(0, 'Dead time %')
        return channels

    def getPymcaConfig(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.pymcaConfig
        finally:
            self.mutex.unlock()

    def setPymcaConfig(self, config):
        try:
            self.mutex.lock()
            self.h5Node._v_attrs.pymcaConfig = config
        finally:
            self.mutex.unlock()

    def getSkipmode(self):
        try:
            self.mutex.lock()
            mon = self.h5Node._v_attrs.skipmodeMonitor
            thresh = self.h5Node._v_attrs.skipmodeThresh
            return (mon, thresh)
        except AttributeError:
            return (None, 0)
        finally:
            self.mutex.unlock()

    def getValidDataPoints(self, indices=None):
        mon, thresh = self.getSkipmode()
        try:
            self.mutex.lock()
            if mon and thresh:
                temp = getattr(self.h5Node.data.cols, mon)[:]
                valid = numpy.nonzero(temp > thresh)[0]
            else:
                valid = range(len(self.h5Node.data))
        finally:
            self.mutex.unlock()

        if indices: return [i for i in indices if i in valid]
        else: return valid

    def setSkipmode(self, monitor=None, thresh=0):
        try:
            self.mutex.lock()
            self.h5Node._v_attrs.skipmodeMonitor = monitor
            self.h5Node._v_attrs.skipmodeThresh = thresh
        finally:
            self.mutex.unlock()

    def updateElementMap(self, mapType, element, index, val):
        node = '/'.join(['elementMaps', mapType, element])
        try:
            self.mutex.lock()
            try:
                self.h5Node._v_file.getNode(self.h5Node, node)[index] = val
            except ValueError:
                print index, node
        finally:
            self.mutex.unlock()
