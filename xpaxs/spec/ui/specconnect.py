"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from SpecClient import SpecClientError

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------


from xpaxs.spec.ui import ui_specconnect
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

        self.specRunner = specRunner
        self.dockWidgets = {}

        self.scanControls = ScanControls(specRunner)
        scanControlsDock = QtGui.QDockWidget('Scan Controls')
        scanControlsDock.setObjectName('SpecScanControlsWidget')
        scanControlsDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|
                                         QtCore.Qt.RightDockWidgetArea)
        scanControlsDock.setWidget(self.scanControls)

        self.dockWidgets['Scan Controls'] = (QtCore.Qt.LeftDockWidgetArea,
                                             scanControlsDock)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    dlg = SpecConnect()
    interface = dlg.exec_()
    print interface
