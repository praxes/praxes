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
        
        specVersion = self.getSpecVersion()
        self.specrunner = specrunner.SpecRunner(specVersion, timeout=500)

        self.scanIO=scanio2.ScanIO(self)
        self.mainTab.addTab(self.scanIO, "Experiment Controls")
        self.mainTab.removeTab(0)

        self.console = None
        self.motorView = None
        
        self.newConsole()

#        self.Opener = QtGui.QMenu("New", self.Bar)
#        self.Opener.addAction("Motor Control", self.newMotorView)
#        self.Opener.addAction("Console", self.newConsole)
#
#    def newMotorView(self):
#        self.motorView = MyUI(self)
#        self.mainTab.addTab(self.Motor.centralWidget(), "Motor Controler")
#        QtCore.QObject.connect(self.Motor.Closer,
#                               QtCore.SIGNAL("clicked()"),
#                               self.Del)

    # TODO: update the console UI, use proper naming convention
    # Dont make it a main window, no central widget.
    def newConsole(self):
        if self.console is None:
            self.console = console.MyKon(self)
        self.mainTab.addTab(self.console.centralWidget(), "Console")
        QtCore.QObject.connect(self.console.Closer,
                               QtCore.SIGNAL("clicked()"),
                               self.Del)

    def Del(self):
        self.mainTab.removeTab(self.Tabby.currentIndex())

#    def set_config_file(self):
#        try:
#            fd = QtGui.QFileDialog(self)
#            self.pymcaConfigFile = "%s"%fd.getOpenFileName()
#            config = getPymcaConfig(self.pymcaConfigFile)
#            self.__peaks = config["peaks"]
#            self.ElementSelect.clear()
#            for peak in self.__peaks:
#                self.ElementSelect.addItem(peak)
#        except:
#            print "come on now"

    def getSpecVersion(self):
        smpConfig = configutils.getSmpConfig()
        try:
            return ':'.join([smpConfig['session']['server'],
                             smpConfig['session']['port']])
        except KeyError:
            editor = configuresmp.ConfigureSmp(self)
            editor.exec_()
            self.getSpecVersion()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = SmpMainWindow()
    myapp.show()
    sys.exit(app.exec_())
