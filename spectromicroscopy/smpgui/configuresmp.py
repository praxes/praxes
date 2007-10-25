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
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy import smpConfig
from spectromicroscopy import configutils
from spectromicroscopy.smpgui import ui_configuresmp

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ConfigureSmp(ui_configuresmp.Ui_ConfigureSmp, QtGui.QDialog):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.serverEdit.setText(smpConfig.session.server)
        self.portEdit.setText(smpConfig.session.port)

        self.connect(self.serverEdit,
                     QtCore.SIGNAL("editingFinished()"),
                     self.set_server)
        self.connect(self.portEdit,
                     QtCore.SIGNAL("editingFinished()"),
                     self.set_port)

    def set_server(self):
        smpConfig.session.server = '%s'%self.serverEdit.text()
    
    def set_port(self):
        smpConfig.session.port = '%s'%self.portEdit.text()

    def accept(self):
        configutils.saveConfig()
        QtGui.QDialog.accept(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ConfigureSmp()
    myapp.show()
    sys.exit(app.exec_())
