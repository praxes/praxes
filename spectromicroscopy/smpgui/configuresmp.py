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

from spectromicroscopy.smpcore import configutils
from spectromicroscopy.smpgui import ui_configuresmp

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ConfigureSmp(ui_configuresmp.Ui_ConfigureSmp, QtGui.QDialog):

    def __init__(self, parent=None):
        self.smpConfig = configutils.getSmpConfig()
        self.validateConfig()

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        server = self.smpConfig['session'].setdefault('server', '')
        self.serverEdit.setText(server)
        port = self.smpConfig['session'].setdefault('port', '')
        self.portEdit.setText(port)
        threshold = self.smpConfig['session'].setdefault('threshold', 0.00)
        self.thresholdBox.setValue(float(threshold))
        counter = self.smpConfig['session'].setdefault('counter', 'Icol')
        self.counterEdit.setText(counter)



        self.connect(self.serverEdit,
                     QtCore.SIGNAL("editingFinished()"),
                     self.set_server)
        self.connect(self.portEdit,
                     QtCore.SIGNAL("editingFinished()"),
                     self.set_port)
        self.connect(self.counterEdit,
                     QtCore.SIGNAL("editingFinished()"),
                     self.set_counter)
        self.connect(self.thresholdBox,
                     QtCore.SIGNAL("editingFinished()"),
                     self.set_threshold)

    def set_server(self):
        self.smpConfig['session']['server'] = '%s'%self.serverEdit.text()
    
    def set_port(self):
        self.smpConfig['session']['port'] = '%s'%self.portEdit.text()

    def set_threshold(self):
        self.smpConfig['skipmode']['threshold']=self.thresholdBox.value()
    
    def set_counter(self):
        self.smpConfig['skipmode']['counter']='%s'%self.counterEdit.text()

    def accept(self):
        self.smpConfig.write()
        QtGui.QDialog.accept(self)

    def reject (self):
        QtGui.QDialog.accept(self)

    def validateConfig(self):
        self.smpConfig.setdefault('session', {})
        self.smpConfig.setdefault('skipmode', {})

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ConfigureSmp()
    myapp.show()
    sys.exit(app.exec_())
