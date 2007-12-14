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


from spectromicroscopy.smpgui import ui_configuresmp

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ConfigureSmp(ui_configuresmp.Ui_ConfigureSmp, QtGui.QDialog):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        settings =QtCore.QSettings()
        self.restoreGeometry(settings.value('ConfigureSmp/Geometry').toByteArray())
        server=settings.value('Server').toString()
        port=settings.value('Port').toString()
        self.serverEdit.setText(server)
        self.portEdit.setText(port)

    def accept(self):
        settings=QtCore.QSettings()
        settings.setValue('Port', QtCore.QVariant(self.portEdit.text()))
        settings.setValue('Server', QtCore.QVariant(self.serverEdit.text()))
        settings.setValue('ConfigureSmp/Geometry', QtCore.QVariant(self.saveGeometry()))
        QtGui.QDialog.accept(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('SMP')
    myapp = ConfigureSmp()
    myapp.show()
    sys.exit(app.exec_())
