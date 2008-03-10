"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



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

    def __init__(self, scan, mutex, *args, **kwargs):
        QtCore.QObject.__init__(self)

        self.mutex = mutex

        self.scan = scan

        self.h5file = scan._v_file
        self.h5filters = tables.Filters(complib='zlib', complevel=9)

        self.dirty = False

    def appendDataPoint(self, index, data):
        raise NotImplementedError
        # TODO: use this for acquisition

    def getDataFileName(self):
        return self.scan._v_attrs.fileName

    def getExpectedScanLines(self):
        return self.scan._v_attrs.scanLines

    def getNormalizationChannels(self):
        raise NotImplementedError

    def getNumScanLines(self):
        return len(self.scan.data)

    def getScanAxes(self):
        return self.scan._v_attrs.scanAxes

    def getScanAxis(self, axis=0, index=0):
        """some scans have multiple axes, some axes have multiple components"""
        # TODO: this is confusing and needs to be improved, probably when
        # we adopt the nexus format
        try:
            return self.scan._v_attrs.scanAxes[axis][index]
        except IndexError, KeyError:
            return ''

    def getScanRange(self, axis):
        return self.scan._v_attrs.scanRange[axis]

    def getScanShape(self):
        return self.scan._v_attrs.scanShape

    def getScanType(self):
        return self.scan._v_attrs.scanType

    def getScanDimensions(self):
        return len(self.scan._v_attrs.scanAxes)

    def saveData(self):
        try:
            self.mutex.lock()
            self.h5file.flush()
        finally:
            self.mutex.unlock()
