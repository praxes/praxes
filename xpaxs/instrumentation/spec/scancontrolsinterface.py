"""
"""

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui

from .scanparameters import ScanParametersWidget
from .skipmode import SkipModeWidget


class ScanControlsInterface(QtGui.QTabWidget):

    """Dialog for setting spec scan options"""

    def __init__(self, specRunner, parent=None):
        QtGui.QTabWidget.__init__(self, parent)

        self.specRunner = specRunner

        self.scanWidget = ScanParametersWidget(specRunner, self)
        self.addTab(self.scanWidget, 'Setup')

        self.skipMode = SkipModeWidget(specRunner, self)
        self.addTab(self.skipMode, 'Skip Mode')

        self.connect(
            self.scanWidget,
            QtCore.SIGNAL("specBusy"),
            self,
            QtCore.SIGNAL("specBusy")
        )
        self.connect(
            self.scanWidget,
            QtCore.SIGNAL("specBusy"),
            self.setBusy
        )

    def setBusy(self, busy):
        self.skipMode.setBusy(busy)
        self.scanWidget.setBusy(busy)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
