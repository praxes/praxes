"""
"""
from __future__ import absolute_import

import gc
import logging

from PyQt4 import QtCore, QtGui
from SpecClient import SpecClientError

from .ui import ui_specconnect
from .scancontrols import ScanControls
from .runner import SpecRunner

USESSH = False


logger = logging.getLogger(__file__)


class ConnectionAborted(Exception):

    def __init__(self, specVersion):
        self.label = specVersion
        return

    def __str__(self):
        str = "Connection to '%s' aborted." % \
              (self.label)
        return str


class SpecConnect(ui_specconnect.Ui_SpecConnect, QtGui.QDialog):

    """This dialog allows the user to identify the spec server and port

    returns a SpecRunner instance
    """

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = None
        self.ssh = None

        self.restore()

    def accept(self):
        self.save()
        QtGui.QDialog.accept(self)

    def connectionError(self):
        host,port = self.getSpecVersion().split(':')
#        logger.error('Unabel to connect to the "%s" instance at "%s".',
#                     port, host)
        error = QtGui.QErrorMessage()
        error.showMessage('''\
        Unabel to connect to the "%s" instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%(port,host))
        error.exec_()

    def _connectToSpec(self):
        self.specRunner = SpecRunner(self.getSpecVersion(), timeout=500)

    def connectToSpec(self):
        if USESSH and not self.ssh:
            try:
                from . import sshdialog
                self.ssh = sshdialog.SshDialog(self.parent()).exec_()
            except ImportError:
                pass
            if not self.ssh: return
        try:
            self._connectToSpec()
#            logger.debug('Connected to spec, specrunner created')
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError()

    def getSpecRunner(self):
        self.connectToSpec()
        return self.specRunner

    def getSpecVersion(self):
        settings = QtCore.QSettings()
        settings.beginGroup('SpecConnect')
        server = "%s"% settings.value('Server').toString()
        port = "%s"% settings.value('Port').toString()
        return ':'.join([server, port])

    def restore(self):
        settings = QtCore.QSettings()
        settings.beginGroup('SpecConnect')
        server = settings.value('Server').toString()
        port = settings.value('Port').toString()
        self.serverEdit.setText(server)
        self.portEdit.setText(port)

    def startSSH(self):
        if not self.ssh:
#            logger.debug('Starting SSH')
            sshdlg = sshdialog.SshDialog(self.parent())
            self.ssh = sshdlg.exec_()

    def save(self):
        settings = QtCore.QSettings()
        settings.beginGroup('SpecConnect')
        settings.setValue('Port', QtCore.QVariant(self.portEdit.text()))
        settings.setValue('Server', QtCore.QVariant(self.serverEdit.text()))


class SpecInterface(QtCore.QObject):

    """
    This is a container for all the spec related stuff, it creates the dock
    widgets and keeps track of the specrunner
    """

    def __init__(self, parent=None):
        super(SpecInterface, self).__init__(parent)

        self._specRunner = None
        self.dockWidgets = {}

        self.mainWindow = parent
        self.name = "spec"

        self.connectToSpec()
        self._configure()

    @property
    def specRunner(self):
        return self._specRunner

    def _connectToSpec(self):
        return SpecConnect(self.mainWindow)

    def connectToSpec(self):
        dlg = self._connectToSpec()
        if dlg.exec_():
            self._specRunner = dlg.getSpecRunner()
            if self._specRunner is None: self.connectToSpec()
        elif self._specRunner is None:
            raise ConnectionAborted(dlg.getSpecVersion())

    def getDatafile(self):
        return self.specRunner.datafile.getValue()

    def _configureInterfaceWidget(self):
        self.interfaceWidget = SpecInterfaceWidget(self.specRunner)
        self.addDockWidget(self.interfaceWidget, 'Spec Interface',
                   QtCore.Qt.LeftDockWidgetArea|
                   QtCore.Qt.RightDockWidgetArea|
                   QtCore.Qt.TopDockWidgetArea|
                   QtCore.Qt.BottomDockWidgetArea,
                   QtCore.Qt.RightDockWidgetArea,
                   'SpecInterfaceWidget')

    def _configure(self):
        from . import configdialog

        self.connect(
            self.mainWindow.actionConfigure,
            QtCore.SIGNAL("triggered()"),
            lambda : configdialog.ConfigDialog(self.specRunner, self.mainWindow)
        )
        self.connect(
            self.specRunner.datafile,
            QtCore.SIGNAL("datafileChanged"),
            self,
            QtCore.SIGNAL("datafileChanged")
        )

        self._configureInterfaceWidget()

    def addDockWidget(
        self, widget, title, allowedAreas, defaultArea, name=None
    ):
        dock = QtGui.QDockWidget(title)
        if name: dock.setObjectName(name)
        dock.setAllowedAreas(allowedAreas)
        dock.setWidget(widget)
        action = dock.toggleViewAction()
        action.setText(title)
        self.dockWidgets[title] = (dock, defaultArea, action)

    def close(self):
        self.interfaceWidget.close()
        self.dockWidgets = {}
        self.specRunner.close()
        self._specRunner = None


class SpecInterfaceWidget(QtGui.QTabWidget):

    def __init__(self, specRunner, parent=None):
        QtGui.QTabWidget.__init__(self, parent)

        from xpaxs.instrumentation.spec.gamepad import GamePad
        from xpaxs.instrumentation.spec.scancontrolsinterface import \
            ScanControlsInterface

        self.gamepad = GamePad(specRunner, self)
        self.addTab(self.gamepad, 'Gamepad')

        self.scanControls = ScanControlsInterface(specRunner, self)
        self.addTab(self.scanControls, 'Scan Controls')


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    dlg = SpecConnect()
    interface = dlg.exec_()
#    print interface
    interface.close()

