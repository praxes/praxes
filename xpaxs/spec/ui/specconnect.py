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

from xpaxs.spec.client.runner import SpecRunner
from xpaxs.spec.ui import ui_specconnect,  configdialog, sshdialog
from xpaxs.spec.ui.scancontrols import ScanControls

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.spec.specconnect')

USESSH = False


class SpecConnect(ui_specconnect.Ui_SpecConnect, QtGui.QDialog):

    """This dialog allows the user to identify the spec server and port

    returns a SpecRunner instance
    """

    def __init__(self, fileInterface=None, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.fileInterface = fileInterface
        self.defineInterface()

        self.specRunner = None
        self.ssh=None

        self.restore()

    def defineInterface(self):
        # The following should be redefined in subclasses of SpecConnect:
        self.getSpecRunner = SpecRunner
        self.getSpecInterface = SpecInterface

    def accept(self):
        self.save()
        QtGui.QDialog.accept(self)

    def connectionError(self):
        logger.error('Unabel to connect to the "%s" spec instance at "%s".',
                     tuple(self.getSpecVersion().split(':')))
        error = QtGui.QErrorMessage()
        error.showMessage('''\
        Unabel to connect to the "%s" spec instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%tuple(self.getSpecVersion().split(':')))
        error.exec_()

    def connectToSpec(self):
        try:
            self.specRunner = self.getSpecRunner(self.getSpecVersion(),
                                timeout=500, fileInterface=self.fileInterface)
            logger.debug('Connected to spec, specrunner created')
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError()
            self.specRunner = None

    def exec_(self):
        if QtGui.QDialog.exec_(self):
            if USESSH:
                self.startSSH()
                if self.ssh: self.connectToSpec()
            else:
                self.connectToSpec()
            if self.specRunner is None: self.exec_()

        if self.specRunner:
            return self.getSpecInterface(self.specRunner, self.parent())
        else:
            return None

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

    def __init__(self, specRunner=None, parent=None):
        super(SpecInterface, self).__init__(parent)

        self.specRunner = specRunner
        self.dockWidgets = {}

        self.mainWindow = parent
        self.name = "spec"

        self._configure()

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

