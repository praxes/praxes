"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import gc
import logging

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from SpecClient import SpecClientError

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_specconnect
from xpaxs.instrumentation.spec import configdialog, sshdialog
from xpaxs.instrumentation.spec.scancontrols import ScanControls
from xpaxs.instrumentation.spec.runner import SpecRunner

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.instrumentation.spec.specconnect')

USESSH = False


class SpecConnect(ui_specconnect.Ui_SpecConnect, QtGui.QDialog):

    """This dialog allows the user to identify the spec server and port

    returns a SpecRunner instance
    """

    def __init__(self, SpecRunner=SpecRunner, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self._SpecRunner = SpecRunner
        self.specRunner = None
        self.ssh=None

        self.restore()

    def accept(self):
        self.save()
        QtGui.QDialog.accept(self)

    def connectionError(self):
        host,port = self.getSpecVersion().split(':')
        logger.error('Unabel to connect to the "%s" instance at "%s".',
                     port, host)
        error = QtGui.QErrorMessage()
        error.showMessage('''\
        Unabel to connect to the "%s" instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%(port,host))
        error.exec_()

    def connectToSpec(self):
        if USESSH and not self.ssh:
            self.ssh = sshdialog.SshDialog(self.parent()).exec_()
            if not self.ssh: return
        try:
            self._SpecRunner(self.getSpecVersion(), timeout=500)
            logger.debug('Connected to spec, specrunner created')
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError()
            self.specRunner = None

    def exec_(self):
        if QtGui.QDialog.exec_(self):
            self.connectToSpec()
            if self.specRunner is None: self.exec_()
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
            logger.debug('Starting SSH')
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

        self.specRunner = specRunner
        self.dockWidgets = {}

        self.mainWindow = parent
        self.name = "spec"

        self._configure()

    def _connectToSpec(self):
        self.specRunner = SpecConnect(SpecRunner, self.mainWindow)

    def _configure(self):
        logger.debug('configuring Spec Interface')
        # This method should be redefined in subclasses of SpecInterface
        self.scanControls = ScanControls(self.specRunner)
        self.addDockWidget(self.scanControls, 'Scan Controls',
                           QtCore.Qt.LeftDockWidgetArea|
                           QtCore.Qt.RightDockWidgetArea,
                           QtCore.Qt.LeftDockWidgetArea,
                           'SpecScanControlsWidget')
        self.connect(self.mainWindow.actionConfigure,
                     QtCore.SIGNAL("triggered()"),
                     lambda : configdialog.ConfigDialog(self.specRunner,
                                                        self.mainWindow))
        self.connect(self.scanControls, QtCore.SIGNAL("addStatusBarWidget"),
                     self.mainWindow.statusBar.addPermanentWidget)
        self.connect(self.scanControls, QtCore.SIGNAL("removeStatusBarWidget"),
                     self.mainWindow.statusBar.removeWidget)

    def addDockWidget(self, widget, title, allowedAreas, defaultArea,
                      name = None):
        dock = QtGui.QDockWidget(title)
        if name: dock.setObjectName(name)
        dock.setAllowedAreas(allowedAreas)
        dock.setWidget(widget)
        action = dock.toggleViewAction()
        action.setText(title)
        self.dockWidgets[title] = (dock, defaultArea, action)

    def close(self):
        self.scanControls = None
        self.dockWidgets = {}
        self.specRunner.close()
        self.specRunner = None


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    dlg = SpecConnect()
    interface = dlg.exec_()
#    print interface
    interface.close()

