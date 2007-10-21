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

from spectromicroscopy.smpgui import ui_scanmotor

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanMotor(ui_scanmotor.Ui_ScanMotor, QtGui.QWidget):
    
    """Establishes a Experimenbt controls    """
    
    def __init__(self, parent, motor):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
    
        self.parent = parent
        self.projectInterface = parent.projectInterface
        
        motors = self.projectInterface.specRunner.getMotorsMne()
        try:
            ind = motors.index(motor)
        except ValueError:
            motor = motors[0]
            ind = 0
        self.setMotor(motor, self.projectInterface.specRunner.specVersion)
        
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
        self._motor = motor = self.projectInterface.specRunner.getMotor(str(motor))
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
            self.emit(QtCore.SIGNAL("motorReady()"))
        else:
            self.emit(QtCore.SIGNAL("motorActive()"))

    def getScanInfo(self):
        m = str(self.motorComboBox.currentText())
        s = self.scanFromSpinBox.value()
        f = self.scanToSpinBox.value()
        result = [m, s, f]
        if self.scanStepsSpinBox.isEnabled():
            result.append(self.scanStepsSpinBox.value())
        return result
    
    def moveMotor(self):
        self._motor.move(self.nextPosSpinBox.value())
