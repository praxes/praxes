"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import gc

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from SpecClient import SpecClientError

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------


from xpaxs.spec.ui import ui_specconnect, configdialog
from xpaxs.spec.client import runner
from xpaxs.spec.ui.scancontrols import ScanControls

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class SpecConnect(ui_specconnect.Ui_SpecConnect, QtGui.QDialog):

    """This dialog allows the user to identify the spec server and port

    returns a SpecRunner instance
    """

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = None

        self.restore()

    def exec_(self):
        if QtGui.QDialog.exec_(self):
            self.connect()
            if self.specRunner is None: self.exec_()
            return SpecInterface(self.specRunner, self.parent())
        else:
            return None

    def connect(self):
        try:
            self.specRunner = runner.SpecRunner(self.getSpecVersion(),
                                                timeout=500)
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError()
            self.specRunner = None

    def connectionError(self):
        error = QtGui.QErrorMessage()
        error.showMessage('''\
        SMP was unabel to connect to the "%s" spec instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%tuple(self.getSpecVersion().split(':')))
        error.exec_()

    def getSpecVersion(self):
        settings = QtCore.QSettings()
        server = "%s"% settings.value('Server').toString()
        port = "%s"% settings.value('Port').toString()
        return ':'.join([server, port])

    def restore(self):
        settings = QtCore.QSettings()
        geometry = settings.value('SpecConnect/Geometry').toByteArray()
        self.restoreGeometry(geometry)
        server = settings.value('Server').toString()
        port = settings.value('Port').toString()
        self.serverEdit.setText(server)
        self.portEdit.setText(port)

    def save(self):
        settings = QtCore.QSettings()
        settings.setValue('Port', QtCore.QVariant(self.portEdit.text()))
        settings.setValue('Server', QtCore.QVariant(self.serverEdit.text()))
        settings.setValue('SpecConnect/Geometry',
                          QtCore.QVariant(self.saveGeometry()))

    def accept(self):
        self.save()
        QtGui.QDialog.accept(self)


class SpecInterface(QtCore.QObject):

    def __init__(self, specRunner=None, parent=None):
        super(SpecInterface, self).__init__(parent)

        QtCore.QObject.__init__(self)
        self.specRunner = specRunner
        self.dockWidgets = {}

        self.mainWindow = parent

        self.scanControls = ScanControls(specRunner)
        self.addDockWidget(self.scanControls, 'Scan Controls',
                           QtCore.Qt.LeftDockWidgetArea|
                           QtCore.Qt.RightDockWidgetArea,
                           QtCore.Qt.LeftDockWidgetArea,
                           'SpecScanControlsWidget')

        self.connect(self.mainWindow.actionConfigure,
                     QtCore.SIGNAL("triggered()"),
                     lambda : configdialog.ConfigDialog(self.specRunner,
                                                        self.mainWindow))

    def addDockWidget(self, widget, title, allowedAreas, defaultArea,
                      name=None):
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
    print interface
    interface.close()

