"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
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

from xpaxs.instrumentation.spec.scan import QtSpecScanA
from xpaxs.instrumentation.spec.runner import SpecRunner
#from xpaxs.instrumentation.spec.scancontrols import ScanControls
from xpaxs.instrumentation.spec.specinterface import SpecConnect, SpecInterface

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


logger = logging.getLogger('XPaXS.frontends.xfs.spec')
DEBUG = False


class SmpSpecRunner(SpecRunner):

    def __init__(self, specVersion=None, timeout=None, parent=None):
        super(SmpSpecRunner, self).__init__(specVersion, timeout, parent)

        # load the clientutils macros before creating the scan:
        self.runMacro('clientutils_sxfm.mac')
        self.clientdataon()
        self.clientploton()
        self.runMacro('skipmode.mac')
#        self.scan = SmpSpecScanA(specVersion, parent=self)

    def close(self):
        self.clientdataoff()
        self.clientplotoff()
        SpecRunner.close(self)


class SmpSpecScanA(QtSpecScanA):

    def __init__(self, specVersion, parent=None):
        super(SmpSpecScanA, self).__init__(specVersion, parent)

        self.fileInterface = None
        self.smpEntry = None
        # TODO: wire events to the file interface and the data objects

    def newScan(self, scanParams):
        QtSpecScanA.newScan(self, scanParams)
        if DEBUG: print scanParams

        specFileName = scanParams['fileName'].split('/')[-1]
        filename = os.path.abspath('%s.h5'%(scanParams['fileName'].split('/')[-1]))
        self.smpEntry = self.fileInterface.createEntry(filename, scanParams)
        if DEBUG: print 'newScan:', self.smpEntry
        # This signal gets connected to a MainWindow.newScanWindow:
        self.emit(QtCore.SIGNAL("newSmpScan"), self.smpEntry, True)

    def newScanData(self, scanData):
        if DEBUG: print 'scanData:', scanData
        self.smpEntry.appendDataPoint(scanData)
        self.emit(QtCore.SIGNAL("newScanIndex(int)"), scanData['i'])

    def scanAborted(self):
        try:
            self.smpEntry.setNumExpectedScanLines(self.smpEntry.getNumScanLines())
        except AttributeError:
            # for testing purposes, shouldnt need this try
            pass
        QtSpecScanA.scanAborted(self)


class SmpSpecInterface(SpecInterface):

    def _connectToSpec(self):
        return SmpSpecConnect(self.mainWindow)


class SmpSpecConnect(SpecConnect):

    def _connectToSpec(self):
        self.specRunner = SmpSpecRunner(self.getSpecVersion(), timeout=500)

    def defineInterface(self):
        self.getSpecRunner = SmpSpecRunner
        self.getSpecInterface = SmpSpecInterface
