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
from xpaxs.io import phynx


logger = logging.getLogger(__file__)


class QtSpecScanA(SpecScan.SpecScanA, QtCore.QObject):

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

        import xpaxs
        fileInterface = xpaxs.application.getService('FileInterface')

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
            if 'shape' in kwargs and 'dtype' in kwargs:
                # these are empty datasets, lets start small and grow
                kwargs['maxshape'] = kwargs['shape']
                kwargs['shape'] = (1, ) + tuple(kwargs['shape'][1:])
            measurement.create_group(k, t, **kwargs)

        # make a few links:
        if 'masked' in measurement['scalar_data']:
            for k, val in measurement.mcas:
                val['masked'] = measurement['scalar_data/masked']

        self._scanData = entry

        ScanView = xpaxs.application.getService('ScanView')
        view = ScanView(entry)
        if view:

            self.connect(
                self,
                QtCore.SIGNAL('beginProcessing'),
                view.processData
            )

        self.emit(QtCore.SIGNAL("newScanLength"), info['npoints'])

    def newScanData(self, scanData):
#        logger.debug( 'scanData: %s', scanData)

        i = scanData['scalar_data/i']

        if self._scanData:
            with self._scanData.plock:
                m = self._scanData['measurement']
                for k, val in scanData.iteritems():
                    try:
                        m[k][i] = val
                    except ValueError:
                        m[k].resize(i+1, axis=0)
                        m[k][i] = val
                    except:
                        print m.listitems(), k

        self._lastPoint = i
        if i == 0:
            self.emit(QtCore.SIGNAL("beginProcessing"))
        self.emit(QtCore.SIGNAL("newScanData"), i)


    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
#        logger.debug( "newScanPoint: %s", i)
        self.emit(QtCore.SIGNAL("newScanPoint"), i)

    def scanAborted(self):
#        logger.info('Scan Aborted')
        try:
            self._scanData.npoints = self._lastPoint
        except (AttributeError, h5py.h5.H5Error, TypeError):
            pass
        self.emit(QtCore.SIGNAL("scanAborted()"))
        self.scanFinished()

    def scanFinished(self):
#        logger.info( 'scan finished')
        self._scanData = None
        self.emit(QtCore.SIGNAL("scanFinished()"))

    def scanPaused(self):
        self.emit(QtCore.SIGNAL("scanPaused()"))

    def scanResumed(self):
        self.emit(QtCore.SIGNAL("scanResumed()"))

    def scanStarted(self):
#        logger.info('scan started')
        self.emit(QtCore.SIGNAL("scanStarted()"))
