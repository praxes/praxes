"""
"""

from __future__ import absolute_import

#import logging

from PyQt4 import QtCore, QtGui, uic

from .ui import resources


#logger = logging.getLogger(__file__)


class ScanMotor(QtGui.QWidget):

    """Establishes a Experiment controls    """

    motorReady = QtCore.pyqtSignal()
    motorActive = QtCore.pyqtSignal()

    def __init__(self, parent, motor):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi(resources['scanmotor.ui'], self)

        self.setParent(parent)
        self.specRunner = parent.specRunner
#        logger.debug('getting motor')
        motors = self.specRunner.getMotorsMne()
        try:
            ind = motors.index(motor)
        except ValueError:
#            logger.error(ValueError)
            motor = motors[0]
            ind = 0
#        logger.debug('setting motor')
        self.setMotor(motor, self.specRunner.specVersion)

        self.motorComboBox.addItems(motors)
        self.motorComboBox.setCurrentIndex(ind)

        self.motorComboBox.currentIndexChanged['QString'].connect(self.setMotor)
        self.nextPosSlider.valueChanged.connect(self.setNextPosition)
        self.nextPosSpinBox.valueChanged.connect(self.setNextPosition)

    def setMotor(self, motor, hostport=None):
        self._motor = motor = self.specRunner.getMotor(str(motor))

        self.setLimits(motor.getLimits())

        position = motor.getPosition()
        self.setPosition(position)
        self.nextPosSlider.setValue(int(position*1000))
        self.nextPosSpinBox.setValue(position)
        self.scanFromSpinBox.setValue(position)
        self.scanToSpinBox.setValue(position+1)
        self.motorStateChanged(self.getState())

        self._motor.motorPositionChanged.connect(self.setPosition)
        self._motor.motorLimitsChanged.connect(self.setLimits)
        self._motor.motorStateChanged.connect(self.motorStateChanged)
        self.nextPosPushButton.clicked.connect(self.moveMotor)

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
            self.motorReady.emit()
            self.setEnabled(True)
        else:
            self.motorActive.emit()
            self.setEnabled(False)

    def getScanInfo(self):
        m = str(self.motorComboBox.currentText())
        s = self.scanFromSpinBox.value()
        f = self.scanToSpinBox.value()
        i = self.scanStepsSpinBox.value()
        return [m, s, f, i]

    def moveMotor(self):
        self._motor.move(self.nextPosSpinBox.value())
