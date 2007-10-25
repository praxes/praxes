"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import sys
import time
import weakref

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy import smpConfig
from spectromicroscopy.smpgui.ui_smpspecinterface import Ui_SmpSpecInterface
from spectromicroscopy.smpgui import configuresmp, pymcafitparams, \
    scananalysis, scancontrols
from spectromicroscopy.smpcore import specrunner, configutils, qtspecscan, \
    qtspecvariable
from SpecClient import SpecClientError

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SmpSpecInterface(Ui_SmpSpecInterface, QtGui.QWidget):
    """Establishes a Experimenbt controls 
    Generates Control and Feedback instances
   Addes Scan atributes to specRunner instance 
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self.parent = parent
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        
        self.connectToSpec()
        
        pymcaConfigFile = configutils.getDefaultPymcaConfigFile()
        self.pymcaConfig = configutils.getPymcaConfig(pymcaConfigFile)
        self.pymcaConfigWidget = pymcafitparams.PyMcaFitParams(self)
        self.pymcaConfigWidget.setParameters(self.pymcaConfig)
        self.toolBox.insertItem(1, self.pymcaConfigWidget, 'PyMca configuration')

        self.scanControls = scancontrols.ScanControls(self)
        self.gridlayout.addWidget(self.scanControls, 0,0)
        self.gridlayout.addWidget(self.toolBox, 0,1,1,1)

        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("newMesh(PyQt_PyObject)"),
                     self.newScanAnalysis2D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newTseries(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newAscan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newA2scan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newA3scan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                     self.setTabLabel)
        self.connect(self.pymcaConfigWidget,
                     QtCore.SIGNAL("configChanged(PyQt_PyObject)"),
                     self.changedPyMcaConfig)

    def changedPyMcaConfig(self):
        self.pymcaConfig = self.pymcaConfigWidget.getParameters()
        self.emit(QtCore.SIGNAL("changedPyMcaConfig(PyQt_PyObject)"),
                  self.pymcaConfig)

    def close(self):
        self.specRunner.close()
        return QtGui.QWidget.close(self)

    def connectToSpec(self):
        specVersion = self.getSpecVersion()
        try:
            self.window().statusBar().showMessage('Connecting')
            QtGui.qApp.processEvents()
            self.specRunner = specrunner.SpecRunner(specVersion, timeout=500)
            self.specRunner.scan = \
                qtspecscan.QtSpecScanMcaA(self.specRunner.specVersion)
            self.window().statusBar().clearMessage()
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError(specVersion)
            raise SpecClientError.SpecClientTimeoutError

    def connectionError(self, specVersion):
        error = QtGui.QErrorMessage()
        server, port = specVersion.split(':')
        error.showMessage('''\
        SMP was unabel to connect to the "%s" spec instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%(port, server))
        error.exec_()

    def getSpecVersion(self):
        return ':'.join([smpConfig['session']['server'],
                         smpConfig['session']['port']])

    def newScanAnalysis(self, newAnalysis):
        self.parent.mainTab.addTab(newAnalysis, '')
        self.parent.mainTab.setCurrentWidget(newAnalysis)

    def newScanAnalysis1D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis1D(self, scanParams))

    def newScanAnalysis2D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis2D(self, scanParams))

    def setTabLabel(self, scanParams):
        i = self.parent.mainTab.currentIndex()
        self.parent.mainTab.setTabText(i, scanParams['title'])


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = SmpProjectInterface()
    myapp.show()
    sys.exit(app.exec_())
