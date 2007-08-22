"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import weakref

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import configuresmp, console, scanio, \
    ui_smpmainwindow
from spectromicroscopy.smpcore import specrunner, configutils
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
        
        self.configureSmp()
        
        self.pymcaConfigFile = configutils.getDefaultPymcaConfigFile()
        
        self.connect(self.actionModify_SMP_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.configureSmpInteractive)
        self.connect(self.actionLoad_PyMca_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.getPymcaConfigFile)
        self.connect(self.actionLoad_Default_Pymca_Config,
                     QtCore.SIGNAL("triggered()"),
                     self.getDefaultPymcaFile)

    def configureSmp(self):
        self.smpConfig = configutils.getSmpConfig()
        specVersion = self.getSpecVersion()
        try:
            self.__specRunner = specrunner.SpecRunner(specVersion, timeout=500)
            # when we reconfigure, we need to remove all references to
            # the old specRunner. An easy way to do this is to make the
            # public interface to specRunner a weak reference:
            self.specRunner = weakref.proxy(self.__specRunner)
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError(specVersion)
            self.configureSmpInteractive()
        
        self.setupUi(self)
        self.scanIO = scanio.ScanIO(self)
        self.mainTab.addTab(self.scanIO, "Experiment Controls")
        self.mainTab.removeTab(0)
    #TODO: added Consoles and motorViews 
        self.console = None #console.MyKon()
##        self.mainTab.addTab(self.console, "Console")
        self.motorView = None

    def connectionError(self, specVersion):
        error = QtGui.QErrorMessage()
        server, port = specVersion.split(':')
        error.showMessage('''\
        SMP was unabel to connect to the "%s" spec instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%(port, server))
        error.exec_()

    def configureSmpInteractive(self):
        configuresmp.ConfigureSmp(self).exec_()
        self.configureSmp()

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
