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

from spectromicroscopy import configutils
from spectromicroscopy import __version__
from spectromicroscopy.smpgui import configuresmp, console, scananalysis, \
    smpspecfileview, smpspecinterface, ui_smpmainwindow
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
#        self.mainTab = smptabwidget.SmpTabWidget(self)
#        self.gridlayout.addWidget(self.mainTab,1,0,1,1)
        self.mdi = QtGui.QMdiArea()
        self.setCentralWidget(self.mdi)
        
        self.statusBar.showMessage('Ready', 2000)
        self.progressBar = QtGui.QProgressBar(self.statusBar)
        self.progressBar.hide()
        
        self.specInterface = None
        self.specfileView = None
        self.specfileInterface = None
        #TODO: added Consoles and motorViews 
        self.console = None 
        self.motorView = None
        
        self.connect(self.actionOpen,
                     QtCore.SIGNAL("triggered()"),
                     self.openDatafile)
        self.connect(self.actionConnect,
                     QtCore.SIGNAL("triggered()"),
                     self.connectToSpec)
        self.connect(self.actionDisconnect,
                     QtCore.SIGNAL("triggered()"),
                     self.disconnectFromSpec)
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
                     self.closeScan)
        self.connect(self.actionClose_All,
                     QtCore.SIGNAL("triggered()"),
                     self.closeAllScans)

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

    def closeEvent(self, event):
        if self.specInterface: self.specInterface.close()
        configutils.saveConfig()
        return event.accept()

    def closeScan(self):
        NotImplementedError

    def closeAllScans(self):
        NotImplementedError

    def open(self):
        NotImplementedError

    def save(self):
        raise NotImplementedError

    def saveAll(self):
        NotImplementedError

    def connectToSpec(self):
        if not configuresmp.ConfigureSmp(self).exec_(): return
        try:
            self.specInterface = \
                smpspecinterface.SmpSpecInterface(statusBar=self.statusBar)
            self.specDockWidget = QtGui.QDockWidget('spec', self)
            self.specDockWidget.setObjectName('SpecDockWidget')
            self.specDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|
                                                QtCore.Qt.RightDockWidgetArea)
            self.specDockWidget.setWidget(self.specInterface)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                               self.specDockWidget)
            
#            self.connect(self.specInterface,
#                         QtCore.SIGNAL("newScanAnalysis(PyQt_PyObject)"),
#                         self.mdi.addSubWindow)
#            self.mainTab.insertTab(0, self.specInterface,
#                                   "Experiment Controls")
        except SpecClientError.SpecClientTimeoutError:
            self.connectToSpec()
        self.actionConnect.setEnabled(False)
        self.actionDisconnect.setEnabled(True)

    def disconnectFromSpec(self):
#        self.mainTab.removeTab(0)
        
        self.specDockWidget.close()
        self.actionConnect.setEnabled(True)
        self.actionDisconnect.setEnabled(False)

    def showProgressBar(self):
        self.statusBar.addWidget(self.progressBar)
        self.progressBar.show()

    def hideProgressBar(self):
        self.statusBar.removeWidget(self.progressBar)
        self.progressBar.hide()

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

    def openDatafile(self):
        f = '%s'% QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.', 
                "Spec datafiles (*.dat *.mca);;All files (*.*)")
        if not f: return
        if self.specfileView is None:
            self.specfileInterface = smpspecfileview.SpecFileModel()
            self.connect(self.specfileInterface,
                         QtCore.SIGNAL('specFileScanActivated'),
                         self.newScanWindow)
            self.specfileView = QtGui.QTreeView()
            self.specfileView.setModel(self.specfileInterface)
            self.specfileView.connect(self.specfileView,
                                      QtCore.SIGNAL('activated(QModelIndex)'),
                                      self.specfileInterface.itemActivated)
            self.specfileDockWidget = QtGui.QDockWidget('specfile', self)
            self.specfileDockWidget.setObjectName('SpecFileDockWidget')
            self.specfileDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|
                                                    QtCore.Qt.RightDockWidgetArea)
            self.specfileDockWidget.setWidget(self.specfileView)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                               self.specfileDockWidget)
        self.specfileInterface.appendSpecFile(f)
        self.specfileView.doItemsLayout()
        row = self.specfileInterface.rowCount(QtCore.QModelIndex())-1
        index = self.specfileInterface.index(row, 0, QtCore.QModelIndex())
        self.specfileView.expand(index)
        self.specfileView.resizeColumnToContents(0)
        self.specfileView.resizeColumnToContents(1)
        self.specfileView.resizeColumnToContents(2)

    def newScanWindow(self, scan):
        scanView = scananalysis.ScanAnalysis(scan)
        self.mdi.addSubWindow(scanView)
        scanView.show()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = SmpMainWindow()
    myapp.show()
    sys.exit(app.exec_())
