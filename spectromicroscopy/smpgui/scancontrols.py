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
from spectromicroscopy.smpcore import specutils, specrunner, qtspecscan

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
        
        # TODO: where to keep the scan?
        self.specrunner.scan = qtspecscan.QtSpecScanA(specrunner.specVersion)
        
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
        self.scanTypeChanged(scans[0])

        self.connect(self.scanTypeComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.scanTypeChanged)
        self.connect(self.abortButton,
                     QtCore.SIGNAL("clicked()"),
                     self.specrunner.abort)
        self.connect(self.scanButton,
                     QtCore.SIGNAL("clicked()"),
                     self.startScan)

    def startScan(self):
        scantype = '%s'%self.scanTypeComboBox.currentText()
        motors = [m.motorComboBox.currentText().toAscii() \
                  for m in (self.motorX, self.motorY, self.motorZ)
                  if m.isEnabled()]
        scanFrom = [m.scanFromSpinBox.value() \
                     for m in (self.motorX, self.motorY, self.motorZ)
                     if m.isEnabled()]
        scanTo = [m.scanToSpinBox.value() \
                     for m in (self.motorX, self.motorY, self.motorZ)
                     if m.isEnabled()]
        scanSteps = [m.scanStepsSpinBox.value() \
                     for m in (self.motorX, self.motorY, self.motorZ)
                     if m.scanStepsSpinBox.isEnabled()]
        if scanSteps:
            scanZip = zip(motors, scanFrom, scanTo, scanSteps)
        else:
            scanZip = zip(motors, scanFrom, scanTo)
            scanZip.append(self.scanStepsSpinBox.value())
        scanArgs = []
        for i in scanZip:
            try:
                scanArgs.extend(i)
            except TypeError:
                scanArgs.append(i)
        scanArgs.append( float(self.scanCountSpinBox.value()) )
        scan = getattr(self.specrunner.scan, scantype)
        scan(*scanArgs)

    def scanTypeChanged(self, scanType):
        scanType = '%s'%scanType
        numMotors = specutils.SCAN_NUM_MOTORS[scanType]
        self.setMotorsEnabled(numMotors)
        
        flag = scanType in ('mesh')
        self.setIndependentStepsEnabled(flag)

    def setIndependentStepsEnabled(self, val=False):
        for m in (self.motorX, self.motorY, self.motorZ):
            m.scanStepsSpinBox.setEnabled(val)
        self.scanStepsSpinBox.setEnabled(not val)

    def setMotorsEnabled(self, numMotors):
        self.motorX.setEnabled(numMotors > 0)
        self.motorY.setEnabled(numMotors > 1)
        self.motorZ.setEnabled(numMotors > 2)
        
        self.motorTab.setCurrentIndex(0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
