"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class XpaxsScanInterface(QtCore.QObject):

    """A thread-safe interface to the scan data"""

    def __init__(self, h5Entry, mutex, parent=None):
        super(XpaxsScanInterface, self).__init__()

        self.mutex = mutex

        self.h5Entry = h5Entry

        self.h5File = h5Entry._v_file
        self.h5Filters = tables.Filters(complib='zlib', complevel=9)

        self.dirty = False

    def appendDataPoint(self, index, data):
        raise NotImplementedError
        # TODO: use this for acquisition

    def dataUpdated(self):
        try:
            self.mutex.lock()
            self.dirty = True
        finally:
            self.mutex.unlock()

    def getDataFileName(self):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.fileName
        finally:
            self.mutex.unlock()

    def getH5Filters(self):
        try:
            self.mutex.lock()
            return copy.deepcopy(self.h5Filters)
        finally:
            self.mutex.unlock()

    def getNormalizationChannels(self):
        raise NotImplementedError

    def getNumExpectedScanLines(self):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.scanLines
        finally:
            self.mutex.unlock()

    def getNumScanDimensions(self):
        try:
            self.mutex.lock()
            return len(self.h5Entry._v_attrs.scanAxes)
        finally:
            self.mutex.unlock()

    def getNumScanLines(self):
        try:
            self.mutex.lock()
            return len(self.h5Entry.data)
        finally:
            self.mutex.unlock()

    def getScanAxes(self):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.scanAxes
        finally:
            self.mutex.unlock()

    def getScanAxis(self, axis=0, index=0):
        """some scans have multiple axes, some axes have multiple components"""
        # TODO: this is confusing and needs to be improved, probably when
        # we adopt the nexus format
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.scanAxes[axis][index]
        except IndexError, KeyError:
            return ''
        finally:
            self.mutex.unlock()

    def getScanNumber(self):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.scanNumber
        finally:
            self.mutex.unlock()

    def getScanRange(self, axis):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.scanRange[axis]
        finally:
            self.mutex.unlock()

    def getScanShape(self):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.scanShape
        finally:
            self.mutex.unlock()

    def getScanType(self):
        try:
            self.mutex.lock()
            return self.h5Entry._v_attrs.scanType
        finally:
            self.mutex.unlock()

    def saveData(self):
        try:
            self.mutex.lock()
            self.h5File.flush()
        finally:
            self.mutex.unlock()
