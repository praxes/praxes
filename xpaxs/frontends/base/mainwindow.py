"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
import sys
import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import __version__
from xpaxs.frontends.base.ui import ui_mainwindow
from xpaxs.frontends.base.fileinterface import H5FileInterface
from xpaxs.frontends.base.ppjobstats import PPJobStats
from xpaxs.frontends.base.emailDlg import EmailDialog


#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.frontends.xfs.mainwindow')


class MainWindowBase(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):
    """Establishes a Experiment controls

    1) establishes week connection to specrunner
    2) creates ScanIO instance with Experiment Controls
    3) Connects Actions from Toolbar

    """

    def __init__(self, parent=None):
        super(MainWindowBase, self).__init__(parent)

        self.setupUi(self)

        self._configureDockArea()

        self.mdi = QtGui.QMdiArea()
        self.setCentralWidget(self.mdi)


        self.expInterface = None
        self.openScans = []

        self.statusBar.showMessage('Ready', 2000)

        self._setupDockWindows()
        self._connectSignals()
        self._restoreSettings()

        import xpaxs
        xpaxs.application.registerService('ScanView', self.newScanWindow)

    def _setupDockWindows(self):
        self._setupPPJobStats()
        self._setFileInterface()
        self._setupEmailDlg()

    def _setupPPJobStats(self):
        self.ppJobStats = PPJobStats()
        self.ppJobStatsDock = self._createDockWindow('PPJobStatsDock')
        self._setupDockWindow(self.ppJobStatsDock,
                               QtCore.Qt.RightDockWidgetArea,
                               self.ppJobStats, 'Analysis Server Stats')

    def _setFileInterface(self):
        self.fileInterface = H5FileInterface(self)
        for key, (item, area, action) in \
                self.fileInterface.dockWidgets.iteritems():
            self.menuView.addAction(action)
            self.addDockWidget(area, item)


    def _setupEmailDlg(self):
        self.menuSettings.addAction("Email Settings",self._startEmailDlg )

    def _startEmailDlg(self):
        email = EmailDialog(self).show()

    def _restoreSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self.restoreGeometry(settings.value('Geometry').toByteArray())
        self.restoreState(settings.value('State').toByteArray())



    def _configureDockArea(self):
        """
        Private method to configure the usage of the dockarea corners.
        """
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.BottomDockWidgetArea)
        self.setDockNestingEnabled(True)

    def _createDockWindow(self, name):
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

    def _setupDockWindow(self, dock, where, widget, caption):
        """
        Private method to configure the dock window created with _createDockWindow().

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

    def _connectSignals(self):
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
        self.connect(self.menuAcquisition,
                     QtCore.SIGNAL("aboutToShow()"),
                     self.updateAcquisitionMenu)
        self.connect(self.actionOffline,
                     QtCore.SIGNAL("triggered()"),
                     self.setOffline)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About XPaXS"),
            self.tr("XPaXS Application, version %s\n\n"
                    "XPaXS is a user interface for controlling synchrotron "
                    "experiments and analyzing data.\n\n"
                    "XPaXS depends on several programs and libraries:\n\n"
                    "    spec: for controlling hardware and data acquisition\n"
                    "    SpecClient: a python interface to the spec server\n"
                    "    PyMca: a set of programs and libraries for analyzing "
                    "X-ray fluorescence spectra"%__version__))

    def closeEvent(self, event):
        self.mdi.closeAllSubWindows()
        if len(self.mdi.subWindowList()) > 0:
            return event.ignore()
        self.connectToSpec(False)
        settings = QtCore.QSettings()
        settings.beginGroup("MainWindow")
        settings.setValue('Geometry', QtCore.QVariant(self.saveGeometry()))
        settings.setValue('State', QtCore.QVariant(self.saveState()))
        self.fileInterface.close()
        if self.expInterface: self.expInterface.close()
        return event.accept()

    def connectToSpec(self, bool):
        if bool:
            from xpaxs.instrumentation.spec.specconnect import ConnectionAborted

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

    def getScanView(self, *args, **kwargs):
        raise NotImplementedError

    def importSpecFile(self, force=False):
        f = '%s'% QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.',
                    "Spec datafiles (*.dat *.mca);;All files (*)")
        if f:
            h5filename = '%s'% QtGui.QFileDialog.getSaveFileName(self,
                    'Save HDF5 File', '.', 'HDF5 files (*.h5 *.hdf5)', f+'.h5')
            if h5filename:
                from xpaxs.io import specfile
                specfile.spec2hdf5(f, hdf5Filename=h5filename, force=True)
                self.openDatafile(h5filename)

    def newScanWindow(self, scan, beginProcessing=False, **kwargs):
        print scan, self.openScans
        if scan in self.openScans:
            return

        scanView, title = self.getScanView(scan, **kwargs)

        self.connect(scanView, QtCore.SIGNAL("scanClosed"), self.scanClosed)
        self.connect(scanView, QtCore.SIGNAL("addStatusBarWidget"),
                     self.statusBar.addPermanentWidget)
        self.connect(scanView, QtCore.SIGNAL("removeStatusBarWidget"),
                     self.statusBar.removeWidget)
        self.connect(scanView, QtCore.SIGNAL("ppJobStats"),
                     self.ppJobStats.updateTable)

        subWindow = self.mdi.addSubWindow(scanView)
        subWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        subWindow.setWindowTitle(title)
        subWindow.showMaximized()
        self.openScans.append(scan)

        self.menuTools.setEnabled(True)
        if beginProcessing: scanView.processData()

    def openDatafile(self, filename=None):
        if filename is None:
            filename = '%s'% QtGui.QFileDialog.getOpenFileName(self,
                            'Open File', '.', "hdf5 files (*.h5 *.hdf5)")
        if not filename: return

        self.fileInterface.openFile(filename)

    def scanClosed(self, scan):
        self.openScans.remove(scan)

    def setOffline(self):
        if self.expInterface is None: return
        if self.expInterface.name == 'spec':
            self.connectToSpec(False)

    def updateAcquisitionMenu(self):
        self.menuAcquisition.clear()
        acquisitionGroup = QtGui.QActionGroup(self)
        acquisitionGroup.addAction(self.actionOffline)
        self.menuAcquisition.addAction(self.actionOffline)
        # TODO: will acquisition work on other platforms?
        if sys.platform == 'linux2':
            acquisitionGroup.addAction(self.actionSpec)
            self.menuAcquisition.addAction(self.actionSpec)
        if self.expInterface is None:
            self.actionOffline.setChecked(True)
        elif self.expInterface.name == 'spec':
            self.actionSpec.setChecked(True)

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
    form = MainWindowBase()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
