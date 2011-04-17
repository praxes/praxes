"""
"""

from __future__ import absolute_import, with_statement

import copy
import logging
import os

import numpy as np
from PyQt4 import QtCore
from SpecClient import SpecScan, SpecCommand, SpecConnectionsManager, \
    SpecEventsDispatcher, SpecWaitObject
import h5py

from . import TEST_SPEC


logger = logging.getLogger(__file__)


class QtSpecScanA(SpecScan.SpecScanA, QtCore.QObject):

    scanLength = QtCore.pyqtSignal(int)
    beginProcessing = QtCore.pyqtSignal()
    scanData = QtCore.pyqtSignal(int)
    scanPoint = QtCore.pyqtSignal(int)
    aborted = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    paused = QtCore.pyqtSignal()
    resumed = QtCore.pyqtSignal()
    started = QtCore.pyqtSignal()

    def __init__(self, specVersion, parent=None):
        QtCore.QObject.__init__(self, parent)
        SpecScan.SpecScanA.__init__(self, specVersion)

        self._scanData = None
        self._lastPoint = -1

    def __call__(self, cmd):
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd(cmd)

    def connected(self):
        pass

    def disconnected(self):
        pass

    def newScan(self, scanParameters):
#        logger.debug('newScan: %s', scanParameters)

        tree = scanParameters.pop('phynx', None)
        if tree is None:
            return

        from praxes.io.phynx import registry
        info = tree.pop('info')

        import praxes
        fileInterface = praxes.application.getService('FileInterface')

        specFile = info['source_file']
        h5File = fileInterface.getH5FileFromKey(specFile)
        if h5File is None:
            return

        # It is possible for a scan number to appear multiple times in a
        # spec file. Booo!
        name = str(info['acquisition_id'])
        acq_order = ''
        i = 0
        while (name + acq_order) in h5File:
            i += 1
            acq_order = '.%d'%i
        name = name + acq_order

        # create the entry and measurement groups
        self._scanData = h5File.create_group(name, 'Entry', **info)
        measurement = self._scanData.create_measurement(**tree)
        # create all the groups under measurement, defined by clientutils:

        ScanView = praxes.application.getService('ScanView')
        view = ScanView(self._scanData)
        if view:
            self.beginProcessing.connect(view.processData)

        self.scanLength.emit(info['npoints'])

    def newScanData(self, scanData):
#        logger.debug( 'scanData: %s', scanData)

        if self._scanData is None:
            return

        self._scanData.update_measurement(**scanData)
        self._lastPoint += 1
        if self._lastPoint == 0:
            self.beginProcessing.emit()
        self.scanData.emit(self._lastPoint)
#        print 'exiting newScanData'

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
#        logger.debug( "newScanPoint: %s", i)
        self.scanPoint.emit(i)

    def scanAborted(self):
#        logger.info('Scan Aborted')
        if self._scanData is not None:
            self._scanData.npoints = self._lastPoint + 1
            self.aborted.emit()
            self.scanFinished()

    def scanFinished(self):
#        logger.info( 'scan finished')
        self._scanData = None
        self.finished.emit()

    def scanPaused(self):
        self.paused.emit()

    def scanResumed(self):
        self.resumed.emit()

    def scanStarted(self):
#        logger.info('scan started')
        self.started.emit()
