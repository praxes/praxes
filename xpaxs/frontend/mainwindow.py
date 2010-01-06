"""
"""

from __future__ import absolute_import

import logging
import sys
import os

from PyQt4 import QtCore, QtGui

import xpaxs
from .ui import ui_mainwindow
from .phynx import FileModel, FileView, ExportRawCSV, ExportCorrectedCSV
import phynx


logger = logging.getLogger(__file__)


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):

    """
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.BottomDockWidgetArea)
        self.setDockNestingEnabled(True)

        self._specFileRegistry = {}
        self.fileModel = FileModel(self)
        self.fileView = FileView(self.fileModel, self)

        self.setCentralWidget(self.fileView)

        # TODO: will acquisition work on other platforms?
        if sys.platform != 'linux2':
            self.menuAcquisition.setEnabled(False)

        self.expInterface = None

        self.statusBar.showMessage('Ready', 2000)

        self._currentItem = None
        self._toolActions = {}
        self._setupToolActions()

        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self.restoreGeometry(settings.value('Geometry').toByteArray())
        self.restoreState(settings.value('State').toByteArray())

        import xpaxs
        # TODO: this should be a factory function, not a method of the main win:
        xpaxs.application.registerService('ScanView', self.newScanWindow)
        xpaxs.application.registerService('FileInterface', self)

    def _createToolAction(
        self, name, target, helptext=None, icon=None
    ):
        assert hasattr(target, 'offersService')
        action = QtGui.QAction(name, self)
        action.setVisible(False)
        self._toolActions[action] = target
        self.connect(
            action,
            QtCore.SIGNAL('triggered()'),
            self.toolActionTriggered
        )
        return action

    def _setupToolActions(self):
        try:
            from xpaxs.core.fluorescence.mcaanalysiswindow import McaAnalysisWindow
            self.menuTools.addAction(
                self._createToolAction("Analyze MCA", McaAnalysisWindow)
            )
        except ImportError:
            pass

        self.menuExport.addAction(
            self._createToolAction("Raw data", ExportRawCSV)
        )
        self.menuExport.addAction(
            self._createToolAction("Corrected data", ExportCorrectedCSV)
        )

    @QtCore.pyqtSignature("")
    def on_actionAboutQt_triggered(self):
        QtGui.qApp.aboutQt()

    @QtCore.pyqtSignature("")
    def on_actionAboutXpaxs_triggered(self):
        QtGui.QMessageBox.about(self, self.tr("About XPaXS"),
            self.tr("XPaXS Application, version %s\n\n"
                    "XPaXS is a user interface for controlling synchrotron "
                    "experiments and analyzing data.\n\n"
                    "XPaXS depends on several programs and libraries:\n\n"
                    "    spec: for controlling hardware and data acquisition\n"
                    "    SpecClient: a python interface to the spec server\n"
                    "    PyMca: a set of programs and libraries for analyzing "
                    "X-ray fluorescence spectra"%xpaxs.__version__))

    @QtCore.pyqtSignature("")
    def on_actionImportSpecFile_triggered(self, force=False):
        f = '%s'% QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.',
                    "Spec datafiles (*.dat *.mca);;All files (*)")
        if f:
            while 1:
                h5_filename = str(
                    QtGui.QFileDialog.getSaveFileName(
                        self,
                        'Save HDF5 File',
                        './'+f+'.h5',
                        'HDF5 files (*.h5 *.hdf5 *.hdf *.nxs)'
                    )
                )
                if h5_filename and os.path.isfile(h5_filename):
                    res = QtGui.QMessageBox.question(
                        self,
                        'overwrite?',
                        'Do you want to overwrite the existing file?',
                        QtGui.QMessageBox.Yes,
                        QtGui.QMessageBox.No
                    )
                    if res == QtGui.QMessageBox.Yes:
                        os.remove(h5_filename)
                    else:
                        continue
                break
            if h5_filename:
                self.statusBar.showMessage('Converting spec data...')
                QtGui.qApp.processEvents()
                from xpaxs.io.spec import convert_to_phynx
                f = convert_to_phynx(f, h5_filename=h5_filename, force=True)
                f.close()
                del f
                self.statusBar.clearMessage()
                self.openFile(h5_filename)

    @QtCore.pyqtSignature("")
    def on_menuTools_aboutToShow(self):
        index = self.fileView.currentIndex()
        self._currentItem = self.fileModel.getNodeFromIndex(index)
        if self._currentItem is not None:
            for action, tool in self._toolActions.iteritems():
                action.setVisible(tool.offersService(self._currentItem))

    @QtCore.pyqtSignature("")
    def on_actionOffline_triggered(self):
        if self.expInterface is None: return
        if self.expInterface.name == 'spec':
            self.connectToSpec(False)

    @QtCore.pyqtSignature("")
    def on_actionOpen_triggered(self):
        self.openFile()

    @QtCore.pyqtSignature("bool")
    def on_actionSpec_toggled(self, bool):
        self.connectToSpec(bool)

    def connectToSpec(self, bool):
        if bool:
            from xpaxs.instrumentation.spec.specinterface import ConnectionAborted

            try:
                from xpaxs.instrumentation.spec.specinterface import SpecInterface
                self.expInterface = SpecInterface(self)

            except ConnectionAborted:
                return

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

    def closeEvent(self, event):
        for view in xpaxs.application.openViews:
            view.close()

        if xpaxs.application.openViews:
            event.ignore()
            return

        self.connectToSpec(False)
        settings = QtCore.QSettings()
        settings.beginGroup("MainWindow")
        settings.setValue('Geometry', QtCore.QVariant(self.saveGeometry()))
        settings.setValue('State', QtCore.QVariant(self.saveState()))
        self.fileModel.close()
        return event.accept()

    def getH5FileFromKey(self, key):
        h5File = self._specFileRegistry.get(key, None)

        if not h5File:
            default = key.split(os.path.sep)[-1] + '.h5'
            h5File = self.saveFile(default)
            if h5File:
                self._specFileRegistry[key] = h5File

        return h5File

## TODO: The following two methods needs to be generalized
## given a scan, offer analyses options
    def getScanView(self, scan):
        # this is a shortcut for now, in the future the view would be
        # an overview of the entry with ability to open different analyses
        if isinstance(scan, phynx.registry['Entry']):
            from .mcaanalysiswindow import McaAnalysisWindow
            if len(scan['measurement'].mcas) > 0:
                return McaAnalysisWindow(scan, self)
            else:
                msg = QtGui.QErrorMessage(self)
                msg.showMessage(
                    'The entry you selected has no MCA data to process'
                )

    def newScanWindow(self, scan):
        self.statusBar.showMessage('Configuring New Analysis Window ...')
        scanView = self.getScanView(scan)
        if scanView is None:
            self.statusBar.clearMessage()
            return

        scanView.show()
        self.statusBar.clearMessage()

        return scanView
##
##

    def openFile(self, filename=None):
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(
                self,
                'Open File',
                '.',
                "hdf5 files (*.h5 *.hdf5 *.hdf *.nxs)"
            )
        if filename:
            self.fileModel.openFile(str(filename))

    def saveFile(self, filename=None):
        if os.path.isfile(filename):
            return self.fileModel.openFile(filename)
        else:
            newfilename = QtGui.QFileDialog.getSaveFileName(
                self,
                "Save File",
                filename,
                "hdf5 files (*.h5 *.hdf5 *.hdf *.nxs)"
            )
            if newfilename:
                newfilename = str(newfilename)
                if newfilename.split('.')[-1] not in ('h5', 'hdf5', 'hdf', 'nxs'):
                    newfilename = newfilename + '.h5'
                return self.fileModel.openFile(newfilename)

    def toolActionTriggered(self):
        self.statusBar.showMessage('Configuring...')
        action = self.sender()
        if action is not None and isinstance(action, QtGui.QAction):
            tool = self._toolActions[action](self._currentItem, self)
            if isinstance(tool, QtGui.QWidget):
                tool.show()
            self.statusBar.clearMessage()


def main():
    import sys
    from .application import XpaxsApplication

    app = XpaxsApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    app.setApplicationName('xpaxs')
    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
