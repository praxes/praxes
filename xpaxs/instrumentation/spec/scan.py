"""
"""

import logging
import os

import numpy as np
from PyQt4 import QtCore
from SpecClient import SpecScan, SpecCommand, SpecConnectionsManager, \
    SpecEventsDispatcher, SpecWaitObject
import h5py

from xpaxs.instrumentation.spec import TEST_SPEC


logger = logging.getLogger(__file__)


class QtSpecScanA(SpecScan.SpecScanA, QtCore.QObject):

    def __init__(self, specVersion, parent=None):
        QtCore.QObject.__init__(self, parent)
        SpecScan.SpecScanA.__init__(self, specVersion)

        self._resume = SpecCommand.SpecCommandA('scan_on', specVersion)
        self._scan_aborted = SpecCommand.SpecCommandA('_SC_NEWSCAN = 0', specVersion)

        self._scanData = None
        self._lastPoint = None

    def __call__(self, cmd):
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd(cmd)

    def abort(self):
        if self.isScanning():
            self.connection.abort()
            self._scan_aborted()
            try:
                self._scanData.npoints = self._lastPoint
            except (AttributeError, h5py.h5.H5Error):
                pass
            self.scanAborted()

    def connected(self):
        pass

    def disconnected(self):
        pass

    def newScan(self, scanParameters):
        logger.debug('newScan: %s', scanParameters)

        import xpaxs
        fileInterface = xpaxs.application.getService('FileInterface')

        if fileInterface:
            specFile = scanParameters['scan_desc']['filename']
            h5File = fileInterface.getH5FileFromKey(specFile)
            # It is possible for a scan number to appear multiple times in a
            # spec file. Booo!
            acq_order = ''
            i = 0
            while (name + acq_order) in self:
                i += 1
                acq_order = '.%d'%i
            name = name + acq_order

            self._scanData = fileInterface.createEntry(h5File, scanParameters)

            if self._scanData:
                ScanView = xpaxs.application.getService('ScanView')
                if ScanView:
                    ScanView(self._scanData, beginProcessing=True)

        self.emit(
            QtCore.SIGNAL("newScanLength"),
            scanParameters['scan_desc']['scan points']
        )

    def newScanData(self, scanData):
        logger.debug( 'scanData: %s', scanData)

        if self._scanData:
            self._scanData.appendDataPoint(scanData)

        i = int(scanData['i'])
        self._lastPoint = i
        self.emit(QtCore.SIGNAL("newScanData"), i)


    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
        logger.debug( "newScanPoint: %s", i)
        self.emit(QtCore.SIGNAL("newScanPoint"), i)

    def pause(self):
        logger.info('Scan Paused')
        self.connection.abort()

    def resume(self):
        logger.info('Scan Resumed')
        self._resume()

    def scanAborted(self):
        logger.info('Scan Aborted')
        self.emit(QtCore.SIGNAL("scanAborted()"))

    def scanFinished(self):
        logger.info( 'scan finished')
        self._scanData = None
        self.emit(QtCore.SIGNAL("scanFinished()"))

    def scanStarted(self):
        logger.info( 'scan started')
        self.emit(QtCore.SIGNAL("scanStarted()"))
