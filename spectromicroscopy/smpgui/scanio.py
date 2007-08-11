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

from spectromicroscopy.smpgui import configuresmp, ui_scanio, scancontrols, \
    scanfeedback
from spectromicroscopy.smpcore import specrunner, configutils

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanIO(ui_scanio.Ui_ScanIO, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)

        try:
            self.specRunner = parent.specRunner
        except AttributeError:
            # for debugging, run seperately from main smp
            specVersion = self.getSpecVersion()
            self.specRunner = specrunner.SpecRunner(specVersion, timeout=500)

        self.scanControls = scancontrols.ScanControls(self)
        self.gridlayout.addWidget(self.scanControls,0,0,1,1)

        self.scanFeedback = scanfeedback.ScanFeedback(self)
        self.gridlayout.addWidget(self.scanFeedback,0,1,1,1)

    # TODO: This is only needed for debugging, can eventually go away:
    def getSpecVersion(self):
        smpConfig = configutils.getSmpConfig()
        try:
            return ':'.join([smpConfig['session']['server'],
                             smpConfig['session']['port']])
        except KeyError:
            editor = configure.ConfigureSmp(self)
            editor.exec_()
            self.getSpecVersion()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ScanIO()
    myapp.show()
    sys.exit(app.exec_())
