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
        self._precision = 2
        self.mneComboBox.addItems( [''] + self.specRunner.getMotorsMne() )

    @property
    def limits(self):
        try:
            return self._motor.getLimits()
        except AttributeError:
            return [-1, 1]

    @property
    def motorMne(self):
        try:
            return self._motor.specName
        except AttributeError:
            return ''

    @property
    def nextPosition(self):
        return self.nextPosSpinBox.value()

    @property
    def position(self):
        try:
            return self._motor.getPosition()
        except AttributeError:
            return 0

    @property
    def precision(self):
        return self._precision

    @property
    def state(self):
        try:
            return self._motor.getState()
        except AttributeError:
            return 'NOTINITIALIZED'

    @property
    def stepSize(self):
        return self.stepSpinBox.value()

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

    def _isNextPositionCurrentPosition(self):
        fmt = '%.' + str(self.precision) + 'f'
        self.emit(
            QtCore.SIGNAL("nextPositionIsCurrent(PyQt_PyObject)"),
            fmt%self.nextPosition == fmt%self.position
        )

    def _limitsChanged(self, limits):
        low, high = limits

        self.lowLimitLabel.setText('%g'%low)
        self.highLimitLabel.setText('%g'%high)
        self.posSpinBox.setRange(low, high)
        self.nextPosSpinBox.setRange(low, high)
        self.nextPosSlider.setRange(low*1000, high*1000)

    def _nextPositionChanged(self, position):
        self.nextPosSpinBox.setValue(position)
        self.nextPosSlider.setValue(int(position*1000))

    def _positionChanged(self, position):
        self.posSpinBox.setValue(position)
        self._isNextPositionCurrentPosition()

    def _setMotorMoving(self, state):
        self.groupBox.setDisabled(state in ('MOVESTARTED', 'MOVING'))

    def _setMotorUsable(self, state):
        usable = state not in ('NOTINITIALIZED', 'UNUSABLE')
        self.posSpinBox.setEnabled(usable)
        self.stepSpinBox.setEnabled(usable)
        self.nextPosSlider.setEnabled(usable)
        self.nextPosSpinBox.setEnabled(usable)

    def _setPrecision(self, precision):
        self.posSpinBox.setDecimals(precision)
        self.stepSpinBox.setDecimals(precision)
        self.nextPosSpinBox.setDecimals(precision)

    def _stateChanged(self, state):
        self._setMotorMoving(state)
        self._setMotorUsable(state)
        self.emit(QtCore.SIGNAL("stateChanged(PyQt_PyObject)"), state)

    @QtCore.pyqtSignature("QString")
    def on_mneComboBox_currentIndexChanged(self, motorMne):
        motorMne = str(motorMne)
        if motorMne:
            self._motor = self.specRunner.getMotor("%s"%motorMne)
            self._connectMotor()
        else:
            self._motor = None
            self._stateChanged(self.state)

        # TODO: Is there a way to get the precision from Spec?
        self._setPrecision(5)
        self._limitsChanged(self.limits)
        self._positionChanged(self.position)
        self._nextPositionChanged(self.position)
        self._stateChanged(self.state)

    @QtCore.pyqtSignature("")
    def on_posSpinBox_editingFinished(self):
        self._motor.move(self.posSpinBox.value())

    @QtCore.pyqtSignature("int")
    def on_nextPosSlider_sliderMoved(self, val):
        self.nextPosSpinBox.setValue(val*0.001)
        self._isNextPositionCurrentPosition()

    @QtCore.pyqtSignature("double")
    def on_nextPosSpinBox_valueChanged(self, val):
        self.nextPosSlider.setValue(int(val*1000))
        self._isNextPositionCurrentPosition()
