"""
Wrappers around the pytables interface to the hdf5 file.

The current interface is closely based on the tabular format of the native spec
ascii files. A new interface will be developed based on the NeXus standard.
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy
import logging

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

logger = logging.getLogger('XPaXS.datalib.hdf5.xpaxsdatainterface')
DEBUG = False

filters = tables.Filters(complib='zlib', complevel=9)


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

    def close(self):
        try:
            self.mutex.lock()
            self.h5File.close()
        finally:
            self.mutex.unlock()

    def createEntry(self, scanParams):
        # This should be reimplemented in subclasses
        scanParams = copy.deepcopy(scanParams)
        scanName = scanParams['title'].lower().replace(' ', '')
        try:
            self.mutex.lock()

            # It is possible for a scan number to appear multiple times in a
            # spec file. Booo!
            scanOrder = ''
            i = 0
            while (scanName + scanOrder) in self.h5File.root:
                i += 1
                scanOrder = '.%d'%i
            scanName = scanName + scanOrder

            h5Entry = self.h5File.createGroup('/', scanName, title=scanName,
                                              filters=filters)
            attrs = h5Entry._v_attrs
            attrs.scanNumber = scanParams['scanNumber']
            attrs.scanCommand = scanParams['scanCommand']
            attrs.scanLines = scanParams['scanLines']
        finally:
            self.mutex.unlock()
        scanEntry = XpaxsScan(self, h5Entry)
        self.emit(QtCore.SIGNAL('newEntry'), scanEntry)
        return scanEntry

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
            return XpaxsScan(self, node)

    def getNodes(self, where='/'):
        return [self.getNode(child) for child in self.h5File.getNode(where)]


class XpaxsNode(QtCore.QObject):

    def __init__(self, xpaxsFile, h5Node):
        super(XpaxsNode, self).__init__(xpaxsFile)

        self.__xpaxsFile = xpaxsFile
        self.__h5Node = h5Node
        self.__mutex = xpaxsFile.mutex

        self.queue = None

    xpaxsFile = property(lambda self: self.__xpaxsFile)
    h5Node = property(lambda self: self.__h5Node)
    mutex = property(lambda self: self.__mutex)


class XpaxsScan(XpaxsNode):

    """A thread-safe interface to the scan data"""

    def appendDataPoint(self, data):
        data = copy.deepcopy(data)
        if DEBUG: print "appending data point:", data['i']
        try:
            self.mutex.lock()
            row = self.h5Node.data.row
            for key, val in data.iteritems():
                row[key] = val
            row.append()
            self.h5Node.data.flush()
            self.queue.put(int(data['i']))
        finally:
            self.mutex.unlock()

    def flush(self):
        self.xpaxsFile.flush()

    def getDataFileName(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.fileName[:]
        finally:
            self.mutex.unlock()

    def getH5Filters(self):
        try:
            self.mutex.lock()
            return copy.deepcopy(self.h5Node._v_filters)
        finally:
            self.mutex.unlock()

    def getNormalizationChannels(self):
        raise NotImplementedError

    def getNumExpectedScanLines(self):
        try:
            self.mutex.lock()
            return copy.copy(self.h5Node._v_attrs.scanLines)
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
            return copy.deepcopy(self.h5Node._v_attrs.scanAxes)
        finally:
            self.mutex.unlock()

    def getScanAxis(self, axis=0, index=0):
        """some scans have multiple axes, some axes have multiple components"""
        # TODO: this is confusing and needs to be improved, probably when
        # we adopt the nexus format
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanAxes[axis][index][:]
        except IndexError, KeyError:
            return ''
        finally:
            self.mutex.unlock()

    def getScanCommand(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanCommand[:]
        finally:
            self.mutex.unlock()

    def getScanNumber(self):
        try:
            self.mutex.lock()
            return copy.copy(self.h5Node._v_attrs.scanNumber)
        finally:
            self.mutex.unlock()

    def getScanRange(self, axis):
        try:
            self.mutex.lock()
            return copy.deepcopy(self.h5Node._v_attrs.scanRange[axis])
        finally:
            self.mutex.unlock()

    def getScanShape(self):
        try:
            self.mutex.lock()
            return copy.deepcopy(self.h5Node._v_attrs.scanShape)
        finally:
            self.mutex.unlock()

    def getScanType(self):
        try:
            self.mutex.lock()
            return self.h5Node._v_attrs.scanType[:]
        finally:
            self.mutex.unlock()

    def saveData(self):
        print "use flush instead of saveData"
        self.flush()

    def setNumExpectedScanLines(self, val):
        val = copy.copy(val)
        try:
            self.mutex.lock()
            self.h5Node._v_attrs.scanLines = val
        finally:
            self.mutex.unlock()

    def setQueue(self, queue):
        try:
            self.mutex.lock()
            self.queue = queue
        finally:
            self.mutex.unlock()
