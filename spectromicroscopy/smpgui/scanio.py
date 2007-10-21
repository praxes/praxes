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

from spectromicroscopy.smpgui import configuresmp, scancontrols, scanfeedback
from spectromicroscopy.smpcore import specrunner, configutils, qtspecscan, \
    qtspecvariable

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanIO(QtGui.QWidget):
    """Establishes a Experimenbt controls 
    Generates Control and Feedback instances
   Addes Scan atributes to specRunner instance 
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        self.gridlayout = QtGui.QGridLayout(self)

        self.specRunner = parent.specRunner

        self.specRunner.scan = \
            qtspecscan.QtSpecScanMcaA(self.specRunner.specVersion)

        self.scanControls = scancontrols.ScanControls(self)
        self.gridlayout.addWidget(self.scanControls,0,0,1,1)

        self.scanFeedback = scanfeedback.ScanFeedback(self)
        self.gridlayout.addWidget(self.scanFeedback,0,1,1,1)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ScanIO()
    myapp.show()
    sys.exit(app.exec_())
