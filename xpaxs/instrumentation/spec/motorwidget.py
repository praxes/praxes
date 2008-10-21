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

    def __init__(self, direction, motorMne, specRunner, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.directionLabel.setText(direction)
        self.specRunner = specRunner
        self.motor = self.specRunner.getMotor(motorMne)
        self.mneComboBox.addItems(self.specRunner.getMotorsMne())

        self.mneComboBox.setCurrentIndex(
            self.mneComboBox.findText(motorMne)
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
            return self.motor.getPosition()
        except AttributeError:
            return None

    @property
    def stepSize(self):
        return self.stepSpinBox.value()

    @property
    def state(self):
        try:
            return self.motor.getState()
        except AttributeError:
            return 'NOTINITIALIZED'

    def _connectMotor(self):
        if self.motor:
            self.connect(
                self.motor,
                QtCore.SIGNAL("positionChanged(PyQt_PyObject)"),
                self._positionChanged
            )
            self.connect(
                self.motor,
                QtCore.SIGNAL("limitsChanged(PyQt_PyObject)"),
                self._limitsChanged
            )
            self.connect(
                self.motor,
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

    def _stateChanged(self, state):
        self.emit(QtCore.SIGNAL("stateChanged(PyQt_PyObject)"), state)

    @QtCore.pyqtSignature("QString")
    def on_mneComboBox_currentIndexChanged(self, motorMne):
        self.motor = self.specRunner.getMotor("%s"%motorMne)
        self._connectMotor()

        self._limitsChanged(self.motor.getLimits())
        position = self.motor.getPosition()
        self._positionChanged(position)
        self.on_posSpinBox_valueChanged(position)

        self._stateChanged(self.state)

    @QtCore.pyqtSignature("")
    def on_posLineEdit_returnPressed(self):
        self.motor.move(float(self.posLineEdit.text()))

    @QtCore.pyqtSignature("int")
    def on_posSlider_sliderMoved(self, val):
        self.posSpinBox.setValue(val*0.001)

    @QtCore.pyqtSignature("double")
    def on_posSpinBox_valueChanged(self, val):
        self.posSlider.setValue(int(val*1000))
