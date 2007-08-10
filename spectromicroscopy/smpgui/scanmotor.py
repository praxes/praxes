"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from ui_scanmotor import Ui_ScanMotor
from spectromicroscopy.smpcore import QtSpecMotorA

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanMotor(Ui_ScanMotor, QtGui.QWidget):
    
    """Establishes a Experimenbt controls    """
    
    def __init__(self, parent, motor):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
    
        self.parent = parent
        self.specrunner = parent.specrunner
        
        motors = self.specrunner.getMotorsMne()
        try:
            ind = motors.index(motor)
        except ValueError:
            motor = motors[0]
            ind = 0
        self.setMotor(motor, 'f3.chess.cornell.edu:xrf')
        
        self.motorComboBox.addItems(motors)
        self.motorComboBox.setCurrentIndex(ind)
        
        self.connect(self.motorComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.setMotor)
        self.connect(self.nextPosSlider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setNextPosition)
        self.connect(self.nextPosSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.setNextPosition)

    def setMotor(self, motor, hostport=None):

        if hostport is None: hostport = 'f3.chess.cornell.edu:xrf'
#        self._motor = motor = QtSpecMotorA(motor, hostport)
        self._motor = motor = self.specrunner.getMotor('%s'%motor)

        self.setLimits(motor.getLimits())

        position = motor.getPosition()
        self.setPosition(position)
        self.nextPosSlider.setValue(int(position*1000))
        self.nextPosSpinBox.setValue(position)
        self.scanFromSpinBox.setValue(position)
        self.scanToSpinBox.setValue(position+1)

        self.connect(self._motor,
                     QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                     self.setPosition)
        self.connect(self._motor,
                     QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                     self.setLimits)
        self.connect(self._motor,
                     QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                     self.motorStateChanged)
        self.connect(self.nextPosPushButton,
                     QtCore.SIGNAL("clicked()"),
                     self.moveMotor)

    def setPosition(self, position):
        self.currentPosReport.setText('%.3f'%position)

    def setLimits(self, limits):
        low, high = limits
        self.lowLim.setText('%.2f'%low)
        self.highLim.setText('%.2f'%high)
        self.nextPosSpinBox.setRange(low, high)
        self.nextPosSlider.setRange(int(low*1000), int(high*1000))
        self.scanFromSpinBox.setRange(low, high)
        self.scanToSpinBox.setRange(low, high)
    
    def setNextPosition(self, position):
        if isinstance(position, int):
            self.nextPosSpinBox.setValue(position*0.001)
        else:
            self.nextPosSlider.setValue(int(position*1000))
    
    def getState(self):
        return self._motor.getState()

    def motorStateChanged(self, state):
        if state in ('READY', 'ONLIMIT'):
            self.nextPosPushButton.setEnabled(True)
            self.motorComboBox.setEnabled(True)
        else:
            self.nextPosPushButton.setEnabled(False)
            self.motorComboBox.setEnabled(False)
        self.emit(QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                  state)

    def getScanInfo(self):
        motor = '%s'%self.motorComboBox.currentText()
        scanFrom = '%s'%self.scanFromSpinBox.value()
        scanTo = '%s'%self.scanToSpinBox.value()
        scanSteps = '%s'%self.scanStepsSpinBox.value()
    
    def moveMotor(self):
        self._motor.move(self.nextPosSpinBox.value())
