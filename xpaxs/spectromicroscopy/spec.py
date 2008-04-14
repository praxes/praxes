"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore
from SpecClient import SpecScan, SpecCommand, SpecConnectionsManager, \
    SpecEventsDispatcher, SpecWaitObject

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.spec.client.scan import QtSpecScanA
from xpaxs.spec.client.runner import SpecRunner
from xpaxs.spec.ui.scancontrols import ScanControls
from xpaxs.spec.ui.specconnect import SpecConnect, SpecInterface

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class SmpSpecRunner(SpecRunner):

    def __init__(self, specVersion=None, timeout=None, fileInterface=None):
        super(SmpSpecRunner, self).__init__(specVersion, timeout)

        # load the clientutils macros before creating the scan:
        self.runMacro('clientutils_sxfm.mac')
        self.clientdataon()
        self.clientploton()
        self.runMacro('skipmode.mac')
        self.scan = SmpSpecScanA(specVersion, fileInterface, parent=self)

    def close(self):
        self.clientdataoff()
        self.clientplotoff()
        SpecRunner.close(self)


class SmpSpecScanA(QtSpecScanA):

    def __init__(self, specVersion, fileInterface=None, parent=None):
        super(SmpSpecScanA, self).__init__(specVersion, parent)

        self.fileInterface = fileInterface
        self.smpEntry = None
        # TODO: wire events to the file interface and the data objects

    def connected(self):
        pass

    def disconnected(self):
        pass

    def newScan(self, scanParams):
        QtSpecScanA.newScan(self, scanParams)
        self.smpEntry = self.fileInterface.createEntry('temp.h5', scanParams)
        if DEBUG: print 'newScan:', self.smpEntry
        self.emit(QtCore.SIGNAL("newSmpScan"), self.smpEntry, True)

    def newScanData(self, scanData):
        if DEBUG: print 'scanData:', scanData
        self.smpEntry.appendDataPoint(scanData)

    def newScanPoint(self, i, x, y, scanData):
        scanData['i'] = i
        scanData['x'] = x
        scanData['y'] = y
#        if DEBUG: print "newScanPoint:", scanData
        self.emit(QtCore.SIGNAL("newScanIndex(int)"), i)
        self.emit(QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"), scanData)

    def resumeScan(self):
        self._resumeScan()

    def scanAborted(self):
        self.emit(QtCore.SIGNAL("scanAborted()"))

    def scanFinished(self):
        if DEBUG: print 'scan finished'
        # TODO: save data!
        self.emit(QtCore.SIGNAL("scanFinished()"))

    def scanStarted(self):
        if DEBUG: print 'scan started'
        self.emit(QtCore.SIGNAL("scanStarted()"))



class SmpScanControls(ScanControls):

    def __init__(self, specRunner, parent=None):
        super(SmpScanControls, self).__init__(specRunner, parent)

    def connectSignals(self):
        ScanControls.connectSignals(self)

    def startScan(self):
        # Do the dialog here
        ScanControls.startScan(self)

    def abort(self):
        ScanControls.abort(self)
        # do cleanup of file here


class SmpSpecInterface(SpecInterface):

    def _configure(self):
        self.scanControls = SmpScanControls(self.specRunner)
        self.addDockWidget(self.scanControls, 'Scan Controls',
                           QtCore.Qt.LeftDockWidgetArea|
                           QtCore.Qt.RightDockWidgetArea,
                           QtCore.Qt.LeftDockWidgetArea,
                           'SpecScanControlsWidget')
        self.connect(self.mainWindow.actionConfigure,
                     QtCore.SIGNAL("triggered()"),
                     lambda : configdialog.ConfigDialog(self.specRunner,
                                                        self.mainWindow))

        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newSmpScan"),
                     self.parent().newScanWindow)


class SmpSpecConnect(SpecConnect):

    def defineInterface(self):
        self.getSpecRunner = SmpSpecRunner
        self.getSpecInterface = SmpSpecInterface
