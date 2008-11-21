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
import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.io.hdf5file')
DEBUG = False

#filters = tables.Filters(complib='zlib', complevel=9)


class XpaxsH5File(QtCore.QObject):

    def __init__(self, filename, mode='a', parent=None):
        super(XpaxsH5File, self).__init__(parent)

        self.__mutex = QtCore.QMutex(QtCore.QMutex.Recursive)

        self.__h5file = h5py.File(filename, mode)

        self.h5File.attrs['format'] = 'h5py transitional'

    mutex = property(lambda self: self.__mutex)
    h5File = property(lambda self: self.__h5file)

    def close(self):
        try:
            self.mutex.lock()
            print 'closing', self.name
            self.h5File.flush()
            self.h5File.close()
        finally:
            self.mutex.unlock()

    def createEntry(self, scanParams):
        try:
            self.mutex.lock()

            scanEntry = XpaxsH5Scan(self, scanParams)

        finally:
            self.mutex.unlock()

        self.emit(QtCore.SIGNAL('newEntry'), scanEntry)
        return scanEntry

    def iterobjects(self):
        for group in self.h5File.iterobjects():
            yield XpaxsH5Scan(self, group)

#    def flush(self):
#        try:
#            self.mutex.lock()
#            self.h5File.flush()
#        finally:
#            self.mutex.unlock()

#    def getFileName(self):
#        try:
#            self.mutex.lock()
#            return self.h5File.name
#        finally:
#            self.mutex.unlock()

    def __getattr__(self, attr):
        try:
            self.mutex.lock()
            return getattr(self.h5File, attr)
        finally:
            self.mutex.unlock()

    def __getitem__(self, item):
        try:
            self.mutex.lock()
            return self.h5File[item]
        finally:
            self.mutex.unlock()

    def __setitem__(self, item, val):
        try:
            self.mutex.lock()
            self.h5File[item] = val
        finally:
            self.mutex.unlock()

    def __contains__(self, item):
        return item in self.h5File

#    def getNode(self, where, name=None):
#        node = self.h5File.getNode(where, name)
#        # TODO: these checks should eventually look for nexus classes
#        # for now just use the pytables classes
#        if isinstance(node, tables.Group):
#            return XpaxsH5Scan(self, node)
#
#    def getNodes(self, where='/'):
#        return [self.getNode(child) for child in self.h5File.getNode(where)]


class XpaxsH5Scan(QtCore.QObject):

    def __init__(self, xpaxsFile, scanParams):
        super(XpaxsH5Scan, self).__init__(xpaxsFile)

        self.__xpaxsFile = xpaxsFile
        self.__mutex = xpaxsFile.mutex

        self._columnNames = []

        if isinstance(scanParams, h5py.Group):
            self.__h5Node = scanParams
            return

        try:
            self.mutex.lock()

            scanName = scanParams['title'].lower().replace(' ', '')
            # It is possible for a scan number to appear multiple times in a
            # spec file. Booo!
            scanOrder = ''
            i = 0
            while (scanName + scanOrder) in self.xpaxsFile:
                i += 1
                scanOrder = '.%d'%i
            scanName = scanName + scanOrder

            self.__h5Node = self.xpaxsFile.create_group(scanName)

        finally:
            self.mutex.unlock()

        self._initializeEntry(scanParams)

    @property
    def xpaxsFile(self):
        return self.__xpaxsFile

    @property
    def h5Node(self):
        return self.__h5Node

    @property
    def mutex(self):
        return self.__mutex

    @property
    def dataFileName(self):
        try:
            self.mutex.lock()
            return self.h5Node.attrs['filename']
        finally:
            self.mutex.unlock()

    @property
    def normalizationChannels(self):
        return self._getNormalizationChannels()

    @property
    def numExpectedPoints(self):
        try:
            self.mutex.lock()
            return self.h5Node.attrs['scan points']
        finally:
            self.mutex.unlock()

    @property
    def numScanDimensions(self):
        try:
            self.mutex.lock()
            return len(eval(self.h5Node.attrs['scan axes']))
        finally:
            self.mutex.unlock()

    @property
    def numPoints(self):
        try:
            self.mutex.lock()
            return len(self.h5Node['data']['i'])
        finally:
            self.mutex.unlock()

    @property
    def scanAxes(self):
        try:
            self.mutex.lock()
            return eval(self.h5Node.attrs['scan axes'])
        finally:
            self.mutex.unlock()

    @property
    def scanCommand(self):
        try:
            self.mutex.lock()
            return self.h5Node.attrs['scan command']
        finally:
            self.mutex.unlock()

    @property
    def scanNumber(self):
        try:
            self.mutex.lock()
            return self.h5Node.attrs['scan number']
        finally:
            self.mutex.unlock()

    @property
    def scanShape(self):
        try:
            self.mutex.lock()
            return eval(self.h5Node.attrs['scan shape'])
        finally:
            self.mutex.unlock()

    @property
    def scanType(self):
        try:
            self.mutex.lock()
            return self.h5Node.attrs['scanType']
        finally:
            self.mutex.unlock()

    def saveData(self):
        print "use flush instead of saveData"
        self.flush()

    def _initializeEntry(self, scanParams):
        try:
            self.mutex.lock()

            attrs = self.h5Node.attrs
            attrs['scanNumber'] = scanParams['scanNumber']
            attrs['scanCommand'] = scanParams['scanCommand']
            attrs['scanLines'] = scanParams['scanLines']

            h5Entry.create_group('data')

        finally:
            self.mutex.unlock()

    def __getattr__(self, attr):
        try:
            self.mutex.lock()
            return getattr(self.h5Node, attr)
        finally:
            self.mutex.unlock()

    def __getitem__(self, item):
        try:
            self.mutex.lock()
            return self.h5Node[item]
        finally:
            self.mutex.unlock()

    def __setitem__(self, item, val):
        try:
            self.mutex.lock()
            self.h5Node[item] = val
        finally:
            self.mutex.unlock()

    def appendDataPoint(self, data):
        if DEBUG: print "appending data point:", data['i']
        try:
            self.mutex.lock()
            index = data['i']
            data = self.h5Node['data']
            for key, val in data.iteritems():
                if isinstance(val, dict):
                    for k, v in val.iteritems():
                        ds = data.require_dataset(k)
                        ds[index] = v
                else:
                    ds = data.require_dataset(key)
                    ds[index] = val
                row[key] = val

        finally:
            self.mutex.unlock()

    def flush(self):
        self.xpaxsFile.flush()

#    def getH5Filters(self):
#        try:
#            self.mutex.lock()
#            return copy.deepcopy(self.h5Node._v_filters)
#        finally:
#            self.mutex.unlock()

    def _getNormalizationChannels(self):
        raise NotImplementedError

    def getScanAxis(self, axis=0, index=0):
        """some scans have multiple axes, some axes have multiple components"""
        # TODO: this is confusing and needs to be improved, probably when
        # we adopt the nexus format
        try:
            self.mutex.lock()
            scanAxes = eval(self.h5Node.attrs['scan axes'])
            return scanAxes[axis][index]
        except IndexError, KeyError:
            return ''
        finally:
            self.mutex.unlock()

    def getScanRange(self, axis):
        try:
            self.mutex.lock()
            scanRange = eval(self.h5Node.attrs['scan range'])
            return scanRange[axis]
        finally:
            self.mutex.unlock()

    def setNumExpectedPoints(self, val=None):
        try:
            self.mutex.lock()
            if val is None:
                val = len(self.h5Node['data']['i'])

            self.h5Node.attrs['scan points'] = val

        finally:
            self.mutex.unlock()

#    def setQueue(self, queue):
#        try:
#            self.mutex.lock()
#            self.queue = queue
#        finally:
#            self.mutex.unlock()
