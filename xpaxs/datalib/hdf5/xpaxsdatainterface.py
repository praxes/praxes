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


class XpaxsFile(QtCore.QObject):

    def __init__(self, filename, mode='r+', parent=None):
        super(XpaxsFile, self).__init__(parent)

        self.__mutex = QtCore.QMutex()

        try:
            self.__h5file = tables.openFile(filename, mode)
        except IOError, err:
            if mode == 'r+': self.__h5file = tables.openFile(filename, 'w')
            else: raise err

    mutex = property(lambda self: self.__mutex)
    h5File = property(lambda self: self.__h5file)

    def flush(self):
        try:
            self.mutex.lock()
            self.h5File.flush()
        finally:
            self.mutex.unlock()

    def getFileName(self):
        try:
            self.mutex.lock()
            return self.h5File.filename
        finally:
            self.mutex.unlock()

    def getNode(self, where, name=None):
        node = self.h5File.getNode(where, name)
        # TODO: these checks should eventually look for nexus classes
        # for now just use the pytables classes
        if isinstance(node, tables.Group):
            return XpaxsScan(node, self)

    def getNodes(self, where='/'):
        return [self.getNode(child) for child in self.h5File.getNode(where)]


class XpaxsNode(QtCore.QObject):

    def __init__(self, h5Node, xpaxsFile):
        super(XpaxsNode, self).__init__(xpaxsFile)

        self.__xpaxsFile = xpaxsFile
        self.__h5Node = h5Node
        self.__mutex = xpaxsFile.mutex

    xpaxsFile = property(lambda self: self.__xpaxsFile)
    h5Node = property(lambda self: self.__h5Node)
    mutex = property(lambda self: self.__mutex)


class XpaxsScan(XpaxsNode):

    """A thread-safe interface to the scan data"""

    def appendDataPoint(self, index, data):
        raise NotImplementedError
        # TODO: use this for acquisition

    def getDataFileName(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.fileName
        finally:
            self.mutex.unlock()

    def getH5Filters(self):
        try:
            self.mutex.lock()
            return copy.deepcopy(self.__h5Node._v_filters)
        finally:
            self.mutex.unlock()

    def getNormalizationChannels(self):
        raise NotImplementedError

    def getNumExpectedScanLines(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanLines
        finally:
            self.mutex.unlock()

    def getNumScanDimensions(self):
        try:
            self.mutex.lock()
            return len(self.h5Node._v_attrs.scanAxes)
        finally:
            self.mutex.unlock()

    def getNumScanLines(self):
        try:
            self.mutex.lock()
            return len(self.h5Node.data)
        finally:
            self.mutex.unlock()

    def getScanAxes(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanAxes
        finally:
            self.mutex.unlock()

    def getScanAxis(self, axis=0, index=0):
        """some scans have multiple axes, some axes have multiple components"""
        # TODO: this is confusing and needs to be improved, probably when
        # we adopt the nexus format
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanAxes[axis][index]
        except IndexError, KeyError:
            return ''
        finally:
            self.mutex.unlock()

    def getScanCommand(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanCommand
        finally:
            self.mutex.unlock()

    def getScanNumber(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanNumber
        finally:
            self.mutex.unlock()

    def getScanRange(self, axis):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanRange[axis]
        finally:
            self.mutex.unlock()

    def getScanShape(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanShape
        finally:
            self.mutex.unlock()

    def getScanType(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanType
        finally:
            self.mutex.unlock()

    def saveData(self):
        print "use flush instead of saveData"
        self.flush()

    def flush(self):
        try:
            self.mutex.lock()
            self.xpaxsFile.flush()
        finally:
            self.mutex.unlock()
