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

from xpaxs.instrumentation.spec.scanparameters import ScanParametersWidget
from xpaxs.instrumentation.spec.skipmode import SkipModeWidget

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanControlsInterface(QtGui.QTabWidget):

    """Dialog for setting spec scan options"""

    def __init__(self, specRunner, parent=None):
        QtGui.QTabWidget.__init__(self, parent)

        self.specRunner = specRunner

        self.scanWidget = ScanParametersWidget(specRunner, self)
        self.addTab(self.scanWidget, 'Setup')

        self.skipMode = SkipModeWidget(specRunner, self)
        self.addTab(self.skipMode, 'Skip Mode')


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
