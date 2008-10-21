#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



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

    def __init__(self, direction, specRunner, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.directionLabel.setText(direction)
        self.specRunner = specRunner
        self._motor = None
        self.mneComboBox.addItems( [''] + self.specRunner.getMotorsMne() )

    @property
    def motorMne(self):
        try:
            return self._motor.specName
        except AttributeError:
            return ''

    @property
    def position(self):
        try:
            return self._motor.getPosition()
        except AttributeError:
            return 0

    @property
    def limits(self):
        try:
            return self._motor.getLimits()
        except AttributeError:
            return [-1, 1]

    @property
    def nextPosition(self):
        return self.posSpinBox.value()

    @property
    def stepSize(self):
        return self.stepSpinBox.value()

    @property
    def state(self):
        try:
            return self._motor.getState()
        except AttributeError:
            return 'NOTINITIALIZED'

    def _connectMotor(self):
        if self._motor:
            self.connect(
                self._motor,
                QtCore.SIGNAL("positionChanged(PyQt_PyObject)"),
                self._positionChanged
            )
            self.connect(
                self._motor,
                QtCore.SIGNAL("limitsChanged(PyQt_PyObject)"),
                self._limitsChanged
            )
            self.connect(
                self._motor,
                QtCore.SIGNAL("stateChanged(PyQt_PyObject)"),
                self._stateChanged
            )

    def _positionChanged(self, position):
        self.posLineEdit.setText("%g"%position)

    def _limitsChanged(self, limits):
        low, high = limits
        self.lowLimitLabel.setText('%g'%low)
        self.highLimitLabel.setText('%g'%high)
        self.posSpinBox.setRange(low, high)
        self.posSlider.setRange(low*1000, high*1000)

    def _setMotorMoving(self, state):
        self.groupBox.setDisabled(state in ('MOVESTARTED', 'MOVING'))

    def _setMotorUsable(self, state):
        usable = state not in ('NOTINITIALIZED', 'UNUSABLE')
        self.posLineEdit.setEnabled(usable)
        self.stepSpinBox.setEnabled(usable)
        self.posSlider.setEnabled(usable)
        self.posSpinBox.setEnabled(usable)

    def _stateChanged(self, state):
        self._setMotorMoving(state)
        self._setMotorUsable(state)
        self.emit(QtCore.SIGNAL("stateChanged(PyQt_PyObject)"), state)

    def _nextPositionChanged(self, position):
        self.posSpinBox.setValue(position)
        self.posSlider.setValue(int(position*1000))

    @QtCore.pyqtSignature("QString")
    def on_mneComboBox_currentIndexChanged(self, motorMne):
        motorMne = str(motorMne)
        if motorMne:
            self._motor = self.specRunner.getMotor("%s"%motorMne)
            self._connectMotor()
        else:
            self._motor = None
            self._stateChanged(self.state)

        self._limitsChanged(self.limits)
        self._positionChanged(self.position)
        self._nextPositionChanged(self.position)
        self._stateChanged(self.state)

    @QtCore.pyqtSignature("")
    def on_posLineEdit_returnPressed(self):
        self._motor.move(float(self.posLineEdit.text()))

    @QtCore.pyqtSignature("int")
    def on_posSlider_sliderMoved(self, val):
        self.posSpinBox.setValue(val*0.001)

    @QtCore.pyqtSignature("double")
    def on_posSpinBox_valueChanged(self, val):
        self.posSlider.setValue(int(val*1000))
