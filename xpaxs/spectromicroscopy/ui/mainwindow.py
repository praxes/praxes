"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyMca import McaAdvancedFit
from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import configutils
from xpaxs import __version__
from xpaxs.spectromicroscopy.ui import ui_mainwindow
from xpaxs.datalib.hdf5 import H5FileModel, H5FileView
from xpaxs.spectromicroscopy.ui.mcaspectrum import McaSpectrum
from xpaxs.spectromicroscopy.ui.scananalysis import ScanAnalysis
from xpaxs.spectromicroscopy.smpdatainterface import SmpScanInterface

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


USE_PYMCA_ADVANCEDFIT = True
McaAdvancedFit.USE_BOLD_FONTS = False


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):
    """Establishes a Experiment controls

    1) establishes week connection to specrunner
    2) creates ScanIO instance with Experiment Controls
    3) Connects Actions from Toolbar

    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.__configureDockArea()

        self.mdi = QtGui.QMdiArea()
        self.setCentralWidget(self.mdi)

        self.spectrumAnalysisDock = self.__createDockWindow('SpectrumAnalysisDock')
        if USE_PYMCA_ADVANCEDFIT:
            self.spectrumAnalysis = McaAdvancedFit.McaAdvancedFit(top=False)
            self.spectrumAnalysis.headerLabel.hide()
            self.spectrumAnalysis.dismissButton.hide()
        else:
            self.spectrumAnalysis = McaSpectrum()
        self.__setupDockWindow(self.spectrumAnalysisDock,
                               QtCore.Qt.BottomDockWidgetArea,
                               self.spectrumAnalysis, 'Spectrum Analysis')

        self.logRead = QtGui.QTextEdit(self)
        self.logRead.setReadOnly(True)
        self.logRead.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.logReadDock = self.__createDockWindow('Log Dock')
        self.__setupDockWindow(self.logReadDock,
                               QtCore.Qt.RightDockWidgetArea,
                               self.logRead, 'System Log')

        self.fileViewDock = self.__createDockWindow('FileViewDock')
        self.fileModel = H5FileModel()
        self.fileView = H5FileView(self.fileModel)
        self.connect(self.fileModel,
                     QtCore.SIGNAL('fileAppended'),
                     self.fileView.appendItem)
        self.connect(self.fileModel,
                     QtCore.SIGNAL('scanActivated'),
                     self.newScanWindow)
        self.__setupDockWindow(self.fileViewDock,
                               QtCore.Qt.LeftDockWidgetArea,
                               self.fileView, 'File View')

        acquisitionGroup = QtGui.QActionGroup(self)
        acquisitionGroup.addAction(self.actionOffline)
        acquisitionGroup.addAction(self.actionSpec)
        self.actionOffline.setChecked(True)

        self.expInterface = None
        self.fileInterface = None
        self.advancedFitWidget = None
    
        self.SSH=None

        self.statusBar.showMessage('Ready', 2000)
        self.progressBar = QtGui.QProgressBar(self.statusBar)
        self.progressBar.hide()

        self.connectSignals()

        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self.restoreGeometry(settings.value('Geometry').toByteArray())
        self.restoreState(settings.value('State').toByteArray())

    def __configureDockArea(self):
        """
        Private method to configure the usage of the dockarea corners.
        """
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.BottomDockWidgetArea)
        self.setDockNestingEnabled(True)

    def __createDockWindow(self, name):
        """
        Private method to create a dock window with common properties.

        @param name object name of the new dock window (string or QString)
        @return the generated dock window (QDockWindow)
        """
        dock = QtGui.QDockWidget()
        dock.setObjectName(name)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetFeatures(\
                                    QtGui.QDockWidget.AllDockWidgetFeatures))
        return dock

    def __setupDockWindow(self, dock, where, widget, caption):
        """
        Private method to configure the dock window created with __createDockWindow().

        @param dock the dock window (QDockWindow)
        @param where dock area to be docked to (Qt.DockWidgetArea)
        @param widget widget to be shown in the dock window (QWidget)
        @param caption caption of the dock window (string or QString)
        """
        if caption is None:
            caption = QtCore.QString()
        self.addDockWidget(where, dock)
        dock.setWidget(widget)
        dock.setWindowTitle(caption)
        action = dock.toggleViewAction()
        action.setText(caption)
        self.menuView.addAction(action)
        dock.show()

    def connectSignals(self):
        self.connect(self.actionOpen,
                     QtCore.SIGNAL("triggered()"),
                     self.openDatafile)
        self.connect(self.actionImportSpecFile,
                     QtCore.SIGNAL("triggered()"),
                     self.importSpecFile)
        self.connect(self.actionSpec,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.connectToSpec)
        self.connect(self.actionAbout_Qt,
                     QtCore.SIGNAL("triggered()"),
                     QtGui.qApp,
                     QtCore.SLOT("aboutQt()"))
        self.connect(self.actionAbout_SMP,
                     QtCore.SIGNAL("triggered()"),
                     self.about)
        self.connect(self.menuTools,
                     QtCore.SIGNAL("aboutToShow()"),
                     self.updateToolsMenu)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About SMP"),
            self.tr("SMP Application, version %s\n\n"
                    "SMP is a user interface for controlling synchrotron "
                    "experiments and analyzing data. SMP is a part of xpaxs "
                    "and depends on several programs and libraries:\n\n"
                    "    spec: for controlling hardware and data acquisition\n"
                    "    SpecClient: a python interface to the spec server\n"
                    "    PyMca: a set of programs and libraries for analyzing "
                    "X-ray fluorescence spectra"%__version__))

    def closeEvent(self, event):
        settings = QtCore.QSettings()
        settings.beginGroup("MainWindow")
        settings.setValue('Geometry', QtCore.QVariant(self.saveGeometry()))
        settings.setValue('State', QtCore.QVariant(self.saveState()))
        if self.expInterface: self.expInterface.close()
        return event.accept()

    def connectToSpec(self, bool):
        if bool:
            from xpaxs.spec.ui.specconnect import SpecConnect

            dlg = SpecConnect(self)
            self.expInterface = dlg.exec_()
            if self.expInterface:
                self.actionConfigure.setEnabled(True)
                for key, (item, area, action) in \
                        self.expInterface.dockWidgets.iteritems():
                    self.menuView.addAction(action)
                    self.addDockWidget(area, item)
            else:
                self.actionOffline.setChecked(True)
        else:
            if self.expInterface:
                self.actionConfigure.setEnabled(False)
                for key, (item, area, action) in \
                        self.expInterface.dockWidgets.iteritems():
                    self.removeDockWidget(item)
                    self.menuView.removeAction(action)
                    self.expInterface.close()
                self.expInterface = None


    def importSpecFile(self, force=False):
        f = '%s'% QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.',
                    "Spec datafiles (*.dat *.mca);;All files (*.*)")
        if f:
            h5filename = '%s'% QtGui.QFileDialog.getSaveFileName(self,
                    'Save HDF5 File', '.', 'HDF5 files (*.h5 *.hdf5)', f+'.h5')
            if h5filename:
                from xpaxs.datalib import specfile
                specfile.spec2hdf5(f, hdf5Filename=h5filename, force=True)
                self.openDatafile(h5filename)

    def openDatafile(self, filename=None):
        if filename is None:
            filename = '%s'% QtGui.QFileDialog.getOpenFileName(self,
                            'Open File', '.', "hdf5 files (*.h5 *.hdf5)")
        if not filename: return

        self.fileModel.appendFile(filename)

    def newScanWindow(self, scan, mutex):
        smpScan = SmpScanInterface(scan, mutex)
        if USE_PYMCA_ADVANCEDFIT:
            scanView = ScanAnalysis(smpScan, advancedFit=self.spectrumAnalysis)
        else:
            scanView = ScanAnalysis(smpScan)
            self.connect(scanView, QtCore.SIGNAL("analyzeSpectrum"),
                         self.spectrumAnalysis.analyzeSpectrum)

        subWindow = self.mdi.addSubWindow(scanView)
        title = '%s: Scan %s'%(smpScan.getDataFileName(),
                               smpScan.getScanNumber())
        subWindow.setWindowTitle(title)
        subWindow.showMaximized()
        self.menuTools.setEnabled(True)

    def updateToolsMenu(self):
        self.menuTools.clear()
        try:
            window = self.mdi.currentSubWindow().widget()
            actions = window.getMenuToolsActions()
            for action in actions:
                self.menuTools.addAction(action)
        except AttributeError:
            pass


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    form = SmpMainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
