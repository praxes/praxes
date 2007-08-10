"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import glob
import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import configuresmp, console, scanio2, \
    ui_smpmainwindow
from spectromicroscopy.smpcore import specrunner, configutils
#from testinterface import MyUI

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SmpMainWindow(ui_smpmainwindow.Ui_Main, QtGui.QMainWindow):

    """Establishes a Experiment controls"""

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.smpConfig = configutils.getSmpConfig()
        specVersion = self.getSpecVersion()
        self.specrunner = specrunner.SpecRunner(specVersion, timeout=500)

        self.pymcaConfigFile = configutils.getDefaultPymcaConfigFile()

        self.scanIO=scanio2.ScanIO(self)
        self.mainTab.addTab(self.scanIO, "Experiment Controls")
        self.mainTab.removeTab(0)

        self.console = None
        self.motorView = None
        
        self.connect(self.actionModify_SMP_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.configureSmpInteractive)
        self.connect(self.actionLoad_PyMca_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.getPymcaConfigFile)

    def configureSmpInteractive(self):
        configuresmp.ConfigureSmp(self).exec_()

    def getSpecVersion(self):
        try:
            return ':'.join([self.smpConfig['session']['server'],
                             self.smpConfig['session']['port']])
        except KeyError:
            self.configureSmpInteractive()
            self.getSpecVersion()
    
    def getPymcaConfigFile(self):
        dialog = QtGui.QFileDialog(self, 'Load PyMca Config File')
        dialog.setFilter('PyMca config files (*.cfg)')
        self.pymcaConfigFile = '%s'%dialog.getOpenFileName()
        print configutils.getPymcaConfig(self.pymcaConfigFile)["peaks"]
    
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
    app = QtGui.QApplication(sys.argv)
    myapp = SmpMainWindow()
    myapp.show()
    sys.exit(app.exec_())
