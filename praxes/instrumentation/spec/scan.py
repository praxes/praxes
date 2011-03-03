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
from praxes.io import phynx


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
        self._lastPoint = None

    def __call__(self, cmd):
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd(cmd)

    def connected(self):
        pass

    def disconnected(self):
        pass

    def newScan(self, scanParameters):
#        logger.debug('newScan: %s', scanParameters)

        tree = scanParameters['phynx']
        info = tree.pop('info')

        import praxes
        fileInterface = praxes.application.getService('FileInterface')

        specFile = info['source_file']
        while 1:
            h5File = fileInterface.getH5FileFromKey(specFile)
            if h5File:
                break

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
        entry = h5File.create_entry(name, **info)
        measurement = entry.measurement
        # create all the groups under measurement, defined by clientutils:
        keys = sorted(tree.keys())
        for k in keys:
            t, kwargs = tree.pop(k)
#            if 'shape' in kwargs and 'dtype' in kwargs:
#                # these are empty datasets, lets start small and grow
#                kwargs['shape'] = (1, ) + tuple(kwargs['shape'][1:])
            phynx.registry[t](measurement, k, create=True, **kwargs)
#            measurement.create_group(k, t, **kwargs)

        # make a few links:
        if 'masked' in measurement['scalar_data']:
            for k, val in measurement.mcas.iteritems():
                val['masked'] = measurement['scalar_data/masked']

        self._scanData = entry

        ScanView = praxes.application.getService('ScanView')
        view = ScanView(entry)
        if view:
            self.beginProcessing.connect(view.processData)

        self.scanLength.emit(info['npoints'])

    def newScanData(self, scanData):
#        logger.debug( 'scanData: %s', scanData)

        try:
            with self._scanData.plock:
                i = scanData['scalar_data/i']
#                print 'received point', i

                m = self._scanData.measurement
                for k, val in scanData.iteritems():
                    try:
                        m[k][i] = val
                        m[k].acquired = i + 1
                    except ValueError:
                        m[k].resize(i+1, axis=0)
                        m[k][i] = val
                        m[k].acquired = i + 1
#                    except:
#                        print m.items(), k
#                print 'updated data for point', i

                self._lastPoint = i
            if i == 0:
                self.beginProcessing.emit()
            self.scanData.emit(i)
#            print 'exiting newScanData'
        except AttributeError:
            pass

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
#        logger.debug( "newScanPoint: %s", i)
        self.scanPoint.emit(i)

    def scanAborted(self):
#        logger.info('Scan Aborted')
        try:
            self._scanData.npoints = self._lastPoint + 1
        except (AttributeError, h5py.h5.H5Error, TypeError):
            pass
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
