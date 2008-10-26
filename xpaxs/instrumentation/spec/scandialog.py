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
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_scancontrols,  ui_scandialog

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanDialog(ui_scandialog.Ui_Dialog, QtGui.QDialog):

    """Dialog for setting spec scan options"""

    def __init__(self, specRunner, scanBounds=None, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = specRunner

        self.tabWidget.removeTab(0)

        self.scanWidget = ScanWidget()
        self.tabWidget.addTab(self.scanWidget, 'Setup')

        sefl.skipMode = SkipMode()
        self.tabWidget.addTab(self.skipMode, 'Skip Mode')

    def exec_(self):
        if QtGui.QDialog.exec_(self):

            self.skipMode.configure()
            try:
                self.scanWidget.startScan()
            except SpecfileError:
                self.exec_()

            return self.result()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
