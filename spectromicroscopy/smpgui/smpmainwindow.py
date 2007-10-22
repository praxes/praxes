"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from PyMca import McaAdvancedFit

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy import smpConfig
from spectromicroscopy.smpgui import configuresmp, console, \
    smpprojectinterface, smptabwidget, ui_smpmainwindow
from spectromicroscopy.smpcore import configutils
from SpecClient import SpecClientError
#from testinterface import MyUI

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SmpMainWindow(ui_smpmainwindow.Ui_Main, QtGui.QMainWindow):
    """Establishes a Experiment controls
    
    1) establishes week connection to specrunner
    2) creates ScanIO instance with Experiment Controls
    3) Connects Actions from Toolbar
    
    """

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.setupUi(self)
        self.mainTab = smptabwidget.SmpTabWidget(self)
        self.gridlayout.addWidget(self.mainTab,1,0,1,1)
        
        self.statusBar().showMessage('Ready', 2000)
        #TODO: added Consoles and motorViews 
        self.console = None 
        self.motorView = None
        
        self.pymcaConfigFile = configutils.getDefaultPymcaConfigFile()
        
        self.connect(self.actionConnect,
                     QtCore.SIGNAL("triggered()"),
                     self.connectToSpec)
        self.connect(self.actionDisconnect,
                     QtCore.SIGNAL("triggered()"),
                     self.disconnectFromSpec)
        self.connect(self.actionModify_SMP_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.configureSmpInteractive)
        self.connect(self.actionLoad_PyMca_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.getPymcaConfigFile)
        self.connect(self.actionLoad_Default_Pymca_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.getDefaultPymcaFile)

    def connectToSpec(self):
        if not self.configureSmpInteractive(): return
        try:
            self.projectInterface = \
                smpprojectinterface.SmpProjectInterface(self)
            self.mainTab.insertTab(0, self.projectInterface,
                                   "Experiment Controls")
        except SpecClientError.SpecClientTimeoutError:
            self.connectToSpec()
        self.actionConnect.setEnabled(False)
        self.actionDisconnect.setEnabled(True)

    def configureSmpInteractive(self):
        return configuresmp.ConfigureSmp(self).exec_()

    def disconnectFromSpec(self):
        self.mainTab.removeTab(0)
        self.projectInterface.close()
        self.actionConnect.setEnabled(True)
        self.actionDisconnect.setEnabled(False)

    def getPymcaConfigFile(self):
        dialog = QtGui.QFileDialog(self, 'Load PyMca Config File')
        dialog.setFilter('PyMca config files (*.cfg)')
        self.pymcaConfigFile = str(dialog.getOpenFileName())

    def getDefaultPymcaFile(self):
        self.pymcaConfigFile = configutils.getDefaultPymcaConfigFile()
        self.emit(QtCore.SIGNAL("pymcaConfigFileChanged(PyQt_PyObject)"),
                  self.pymcaConfigFile)
    
    # TODO: ability to change pymca config files, using PyMca Advanced Fit

#    # TODO: This interface needs attention
#    def newMotorView(self):
#        self.motorView = MyUI(self)
#        self.mainTab.addTab(self.Motor.centralWidget(), "Motor Controler")
#        self.connect(self.Motor.Closer,
#                     QtCore.SIGNAL("clicked()"),
#                     self.Del)
#
#    # TODO: update the console UI, use proper naming convention
#    # Dont make it a main window, no central widget.
#    def newConsole(self):
#        if self.console is None:
#            self.console = console.MyKon(self)
#        self.mainTab.addTab(self.console.centralWidget(), "Console")
#        self.connect(self.console.Closer,
#                     QtCore.SIGNAL("clicked()"),
#                     self.Del)
#
#    def Del(self):
#        self.mainTab.removeTab(self.Tabby.currentIndex())


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = SmpMainWindow()
    myapp.show()
    sys.exit(app.exec_())
