"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpcore import getSmpConfig
from ui_configuresmp import Ui_ConfigureSmp

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ConfigureSmp(Ui_ConfigureSmp, QtGui.QDialog):

    def __init__(self):
        self.smpConfig = getSmpConfig()
        self.validateConfig()

        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)

        server = self.smpConfig['session'].setdefault('server', '')
        self.serverEdit.setText(server)
        port = self.smpConfig['session'].setdefault('port', '')
        self.portEdit.setText(port)

        QtCore.QObject.connect(self.serverEdit,
                               QtCore.SIGNAL("editingFinished()"),
                               self.set_server)
        QtCore.QObject.connect(self.portEdit,
                               QtCore.SIGNAL("editingFinished()"),
                               self.set_port)
        QtCore.QMetaObject.connectSlotsByName(self)

    def set_server(self):
        self.smpConfig['session']['server'] = '%s'%self.serverEdit.text()
    
    def set_port(self):
        self.smpConfig['session']['port'] = '%s'%self.portEdit.text()

    def accept(self):
        self.smpConfig.write()
        QtGui.QDialog.accept(self)

    def reject (self):
        QtGui.QDialog.accept(self)

    def validateConfig(self):
        self.smpConfig.setdefault('session', {})

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ConfigureSmp()
    myapp.show()
    sys.exit(app.exec_())
