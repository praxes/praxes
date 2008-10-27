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

from xpaxs.instrumentation.spec.ui import ui_scanmotorwidget

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanMotorWidget(ui_scanmotorwidget.Ui_ScanMotorWidget, QtGui.QGroupBox):

    def __init__(
        self, specRunner, title="", motorName=None, scanBounds=None,
        parent=None
    ):
        QtGui.QGroupBox.__init__(self, parent)
        self.setupUi(self)

        self.setTitle(title)

        self.specRunner = specRunner
        self._scanBounds = scanBounds

    @property
    def scanBounds(self):
        return self._scanBounds

    def _setBounds(self):
        # TODO: use scanBounds to determine the defaults
        pass


class AScanMotorWidget(ScanMotorWidget):
    pass


class DScanMotorWidget(ScanMotorWidget):
    pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
