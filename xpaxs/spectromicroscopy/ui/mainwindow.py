"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import configutils
from xpaxs import __version__
from xpaxs.spectromicroscopy.ui import ui_mainwindow

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):
    """Establishes a Experiment controls

    1) establishes week connection to specrunner
    2) creates ScanIO instance with Experiment Controls
    3) Connects Actions from Toolbar

    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.mdi = QtGui.QMdiArea()
        self.setCentralWidget(self.mdi)

        self.expInterface = None
        self.fileInterface = None

        self.statusBar.showMessage('Ready', 2000)
        self.progressBar = QtGui.QProgressBar(self.statusBar)
        self.progressBar.hide()

        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self.restoreGeometry(settings.value('Geometry').toByteArray())

        self.connectSignals()

    def connectSignals(self):
        self.connect(self.actionOpen,
                     QtCore.SIGNAL("triggered()"),
                     self.openDatafile)
        self.connect(self.actionImportSpecFile,
                     QtCore.SIGNAL("triggered()"),
                     self.importSpecFile)
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
        if self.expInterface:
            self.expInterface.close()
        return event.accept()

    def connectToSpec(self):
        from xpaxs.spec.ui.specconnect import SpecConnect

        dlg = SpecConnect(self)
        self.expInterface = dlg.exec_()
        if self.expInterface:
            self.actionConnect.setEnabled(False)
            self.actionDisconnect.setEnabled(True)

            for key, (item, area, action) in self.expInterface.dockWidgets.iteritems():
                self.menuSpec.addAction(action)
                self.addDockWidget(area, item)

    def disconnectFromSpec(self):
        for key, (item, area, action) in self.expInterface.dockWidgets.iteritems():
            self.removeDockWidget(item)
            self.menuSpec.removeAction(action)
            self.expInterface.close()
        self.expInterface = None
        self.actionConnect.setEnabled(True)
        self.actionDisconnect.setEnabled(False)

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
        if self.fileInterface is None:
            from xpaxs.datalib.hdf5 import FileInterface
            self.fileInterface = FileInterface()
            self.connect(self.fileInterface.fileModel,
                         QtCore.SIGNAL('scanActivated'),
                         self.newScanWindow)
            for key, (area, item) in self.fileInterface.dockWidgets.iteritems():
                viewAction = item.toggleViewAction()
                viewAction.setText(key)
                self.menuView.addAction(viewAction)
                self.addDockWidget(area, item)

        self.fileInterface.openFile(filename)

    def newScanWindow(self, scan):
        from xpaxs.spectromicroscopy.ui import scananalysis
        from xpaxs.spectromicroscopy import analysisController
        controller = analysisController.AnalysisController(scan)
        scanView = scananalysis.ScanAnalysis(controller)
        self.mdi.addSubWindow(scanView)
        scanView.show()
        # TODO: this next line is just for convenience during development
        # needs to be implemented elsewhere
        controller.processData()


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    form = SmpMainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
