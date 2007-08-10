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

from ui_scancontrols import Ui_ScanControls
from scanmotor import ScanMotor
from spectromicroscopy.smpcore import SCAN_NUM_MOTORS, SpecRunner

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanControls(Ui_ScanControls, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        if parent is None:
            specrunner = SpecRunner('f3.chess.cornell.edu:xrf', 500)
        else:
            specrunner = parent.specrunner
        self.specrunner = specrunner
        
        self.gridX = QtGui.QGridLayout(self.xAxisTab)
        self.motorX = ScanMotor(self, 'samx')
        self.gridX.addWidget(self.motorX)

        self.gridY = QtGui.QGridLayout(self.yAxisTab)
        self.motorY = ScanMotor(self, 'samz')
        self.gridY.addWidget(self.motorY)

        self.gridZ = QtGui.QGridLayout(self.zAxisTab)
        self.motorZ = ScanMotor(self, 'samy')
        self.gridZ.addWidget(self.motorZ)
        
        scans = SCAN_NUM_MOTORS.keys()
        scans.sort()
        self.scanTypeComboBox.addItems(scans)
        self.setMotors(scans[0])

        QtCore.QObject.connect(self.scanTypeComboBox,
                               QtCore.SIGNAL("currentIndexChanged(const \
                                                QString&)"),
                               self.setMotors)

    def setMotors(self, scanType):
        scanType = '%s'%scanType
        numMotors = SCAN_NUM_MOTORS[scanType]
        
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
