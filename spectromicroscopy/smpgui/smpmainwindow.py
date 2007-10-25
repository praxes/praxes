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

from spectromicroscopy import smpConfig, __version__
from spectromicroscopy.smpgui import configuresmp, console, \
    smpspecinterface, smptabwidget, ui_smpmainwindow
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
        
        self.connect(self.actionConnect,
                     QtCore.SIGNAL("triggered()"),
                     self.connectToSpec)
        self.connect(self.actionDisconnect,
                     QtCore.SIGNAL("triggered()"),
                     self.disconnectFromSpec)
        self.connect(self.actionConfigure_SMP,
                     QtCore.SIGNAL("triggered()"),
                     self.configureSmpInteractive)
        self.connect(self.actionLoad_PyMca_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.getPymcaConfigFile)
        self.connect(self.actionLoad_Default_Pymca_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.getDefaultPymcaFile)
        self.connect(self.actionAbout_Qt,
                     QtCore.SIGNAL("triggered()"),
                     QtGui.qApp,
                     QtCore.SLOT("aboutQt()"))
        self.connect(self.actionAbout_SMP,
                     QtCore.SIGNAL("triggered()"),
                     self.about)
        self.connect(self.actionOpen,
                     QtCore.SIGNAL("triggered()"),
                     self.open)
        self.connect(self.actionSave,
                     QtCore.SIGNAL("triggered()"),
                     self.save)
        self.connect(self.actionSave_All,
                     QtCore.SIGNAL("triggered()"),
                     self.saveAll)
        self.connect(self.actionClose,
                     QtCore.SIGNAL("triggered()"),
                     self.close)
        self.connect(self.actionClose_All,
                     QtCore.SIGNAL("triggered()"),
                     self.closeAll)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About SMP"),
            self.tr("SMP Application, version %s\n\n"
                    "SMP is a user interface for controlling synchrotron "
                    "experiments and analyzing data. SMP depends on several "
                    "programs and libraries:\n\n"
                    "    spec: for controlling hardware and data acquisition\n"
                    "    SpecClient: a python interface to the spec server\n"
                    "    PyMca: a set of programs and libraries for analyzing "
                    "X-ray fluorescence spectra"%__version__))

    def close(self):
        NotImplementedError

    def closeAll(self):
        NotImplementedError

    def open(self):
        NotImplementedError

    def save(self):
        raise NotImplementedError

    def saveAll(self):
        NotImplementedError

    def connectToSpec(self):
        if not self.configureSmpInteractive(): return
        try:
            self.projectInterface = \
                smpspecinterface.SmpSpecInterface(self)
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
