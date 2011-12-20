"""
"""
#import logging
import sys
import os

from PyQt4 import QtCore, QtGui

import praxes
from .ui import ui_mainwindow
from .phynx import FileModel, FileView, ExportRawCSV, ExportCorrectedCSV
from .notifications import NotificationsDialog


#logger = logging.getLogger(__file__)


class AnalysisWindow(QtGui.QMainWindow):

    """
    """

    def __init__(self, parent=None):
        super(AnalysisWindow, self).__init__(parent)
        praxes.application.openViews.append(self)

    def _setupDockWindows(self):
        pass

    def _restoreSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup(str(self.__class__))
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

    @QtCore.pyqtSignature("")
    def on_actionAboutQt_triggered(self):
        QtGui.qApp.aboutQt()

    @QtCore.pyqtSignature("")
    def on_actionAboutPraxes_triggered(self):
        QtGui.QMessageBox.about(self, self.tr("About Praxes"),
            self.tr("Praxes Application, version %s\n\n"
                    "Praxes is a user interface for controlling synchrotron "
                    "experiments and analyzing data.\n\n"
                    "Praxes depends on several programs and libraries:\n\n"
                    "    spec: for controlling hardware and data acquisition\n"
                    "    SpecClient: a python interface to the spec server\n"
                    "    PyMca: a set of programs and libraries for analyzing "
                    "X-ray fluorescence spectra"%praxes.__version__))

    def closeEvent(self, event):
        try:
            praxes.application.openViews.remove(self)
        except ValueError:
            # subclass may have already removed it
            pass
        settings = QtCore.QSettings()
        settings.beginGroup(str(self.__class__))
        settings.setValue('Geometry', QtCore.QVariant(self.saveGeometry()))
        settings.setValue('State', QtCore.QVariant(self.saveState()))
        event.accept()

    @classmethod
    def offersService(cls, h5Node):
        """
        inspect an hdf5 node and return true or false depending on whether
        the analysis tool will accept it for processing.
        """
        raise NotImplementedError(
            'class method "offersService" has not been implemented'
            )

#def main():
#    import sys
#    app = QtGui.QApplication(sys.argv)
#    app.setOrganizationName('Praxes')
#    form = AnalysisWindow()
#    form.show()
#    sys.exit(app.exec_())
#
#
#if __name__ == "__main__":
#    main()
