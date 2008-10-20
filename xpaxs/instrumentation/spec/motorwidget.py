#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys
import time
from math import ceil

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# GUI imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_motorwidget

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------


class MotorWidget(ui_motorwidget.Ui_MotorWidget, QtGui.QWidget):

    def __init__(self, specRunner, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = specRunner
        self.motorMneComboBox.addItems(self.specRunner.getMotorsMne())
        self._motor = None

        self.connect(
            self.motorMneComboBox,
            QtCore.SIGNAL('currentIndexChanged(QString)'),
            self.setMotor
        )

    @property
    def motorMne(self):
        try:
            return self.motor.specName
        except AttributeError:
            return None

    @property
    def currentPosition(self):
        try:
            return self._motor.getPosition()
        except AttributeError:
            return None

#    @property
#    def motor(self):
#        return self._motor

#    def __getattr__(self, attr):
#        return getattr(self._Motor, attr)

#    def _disconnectMotor(self):
#        if self._motor:
#            self.disconnect(
#                self._motor,
#                QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
#                self.setPosition
#            )
#            self.disconnect(
#                self._motor,
#                QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
#                self.setLimits
#            )
#            self.disconnect(
#                self._motor,
#                QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
#                self.stateChanged
#            )

#        print "Defining %s as new motor"%motor
#        self._Motor = self.specRunner.getMotor(motor)
#        self.setLimits(self._Motor.getLimits())
#        position = self._Motor.getPosition()
#        self.setPosition(position)
#        self.Slider.setValue(int(position*1000))
#        self.PositionSpin.setValue(position)

#        self.connect(
#            self._Motor,
#            QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
#            self.setPosition
#        )
#        self.connect(
#            self._Motor,
#            QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
#            self.setLimits
#        )
#        self.connect(
#            self._Motor,
#            QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
#            self.stateChanged
#        )

#        self.emit(QtCore.SIGNAL("motorChanged()"))

    @QtCore.pyqtSignature("")
    def on_posLineEdit_returnPressed(self):
        self._motor.move(float(self.posLineEdit.text()))

    @QtCore.pyqtSignature("PyQt_PyObject")
    def on__motor_positionChanged(self, position):
        self.posLineEdit.setValue(position)

    @QtCore.pyqtSignature("PyQt_PyObject")
    def on__motor_limitsChanged(self, limits):
        low, high = limits
        self.lowLimitLabel.setText('%g'%low)
        self.highLimitLabel.setText('%g'%high)
        self.posSpinBox.setRange(low, high)
        self.posSlider.setRange(low*1000, high*1000)

    @QtCore.pyqtSignature("PyQt_PyObject")
    def on__motor_stateChanged(self, state):
        print "Motor %s state changed to %s"%(self.motorMne, state)
        self.emit(QtCore.SIGNAL("stateChanged()"))

    @QtCore.pyqtSignature("QString")
    def on_motorMneComboBox_currentIndexChanged(self, motorMne):
        print "Defining %s as new motor"% motorMne
        self._motor = self.specRunner.getMotor(motorMne)
#        self.setLimits(self._motor.getLimits())
#        position = self._Motor.getPosition()
#        self.setPosition(position)
#        self.Slider.setValue(int(position*1000))
#        self.PositionSpin.setValue(position)


    @QtCore.pyqtSignature("int")
    def on_posSlider_sliderMoved(self, val):
        self.posSpinBox.setValue(val*0.001)

    @QtCore.pyqtSignature("double")
    def on_posSpinBox_valueChanged(self, val):
        self.posSlider.setValue(int(val*1000))


#if __name__  ==  "__main__":
#    print __file__
#    app = QtGui.QApplication(sys.argv)
#    app.setOrganizationName('test')
#    myapp = MotorWidget()
#    myapp.show()
#    sys.exit(app.exec_())
