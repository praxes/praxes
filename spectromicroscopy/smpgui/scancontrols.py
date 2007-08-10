"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import scanmotor, ui_scancontrols
from spectromicroscopy.smpcore import specutils, specrunner

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanControls(ui_scancontrols.Ui_ScanControls, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        if parent is None:
            specrunner = specrunner.SpecRunner('f3.chess.cornell.edu:xrf', 500)
        else:
            specrunner = parent.specrunner
        self.specrunner = specrunner
        
        self.gridX = QtGui.QGridLayout(self.xAxisTab)
        self.motorX = scanmotor.ScanMotor(self, 'samx')
        self.gridX.addWidget(self.motorX)

        self.gridY = QtGui.QGridLayout(self.yAxisTab)
        self.motorY = scanmotor.ScanMotor(self, 'samz')
        self.gridY.addWidget(self.motorY)

        self.gridZ = QtGui.QGridLayout(self.zAxisTab)
        self.motorZ = scanmotor.ScanMotor(self, 'samy')
        self.gridZ.addWidget(self.motorZ)
        
        scans = specutils.SCAN_NUM_MOTORS.keys()
        scans.sort()
        self.scanTypeComboBox.addItems(scans)
        self.setMotors(scans[0])

        QtCore.QObject.connect(self.scanTypeComboBox,
                               QtCore.SIGNAL("currentIndexChanged(const \
                                                QString&)"),
                               self.setMotors)

    def setMotors(self, scanType):
        scanType = '%s'%scanType
        numMotors = specutils.SCAN_NUM_MOTORS[scanType]
        
        self.xAxisTab.setEnabled(numMotors > 0)
        self.yAxisTab.setEnabled(numMotors > 1)
        self.zAxisTab.setEnabled(numMotors > 2)
        
        self.motorTab.setCurrentIndex(0)

    def abort(self):
        self.specrunner.abort()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
