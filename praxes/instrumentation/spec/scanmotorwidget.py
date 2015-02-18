"""
"""
from __future__ import absolute_import

from PyQt4 import QtCore, QtGui, uic

from .ui import resources


class ScanMotorWidget(QtGui.QGroupBox):

    motorReady = QtCore.pyqtSignal(bool)

    def __init__(self, specRunner, title="", motorName=None, parent=None):
        QtGui.QGroupBox.__init__(self, parent)
        uic.loadUi(resources['scanmotorwidget.ui'], self)

        self._direction = title.replace(' ', '')
        self.setTitle(title)

        self.specRunner = specRunner

        self.mneComboBox.addItems([''] + self.specRunner.getMotorsMne() )
        settings = QtCore.QSettings()
        settings.beginGroup("%s/%s"%(self.__class__, self._direction))
        mne = settings.value('motorMne').toString()
        i = self.mneComboBox.findText(mne)
        if i != -1:
            self.mneComboBox.setCurrentIndex(i)

    @property
    def limits(self):
        try:
            return self._motor.getLimits()
        except AttributeError:
            return [-1, 1]

    @property
    def motorMne(self):
        return self.mneComboBox.currentText()

    @property
    def isReady(self):
        if self._motor is None:
            return False
        else:
            return True

    @property
    def position(self):
        try:
            return self._motor.getPosition()
        except AttributeError:
            return 0

    @property
    def precision(self):
        try:
            return self._motor.getPrecision()
        except AttributeError:
            return 0

    @property
    def start(self):
        return self.startSpinBox.value()

    @property
    def stop(self):
        return self.stopSpinBox.value()

    @property
    def steps(self):
        return self.stepSpinBox.value()

    def _connectMotor(self):
        if self._motor:
            self._motor.scanBoundStartChanged.connect(self._setStartPosition)
            self._motor.scanBoundStopChanged.connect(self.stopSpinBox.setValue)
            self._motor.limitsChanged.connect(self._limitsChanged)

    def _limitsChanged(self, limits):
        low, high = limits

        self.startSpinBox.setRange(low, high)
        self.stopSpinBox.setRange(low, high)

    def _setPrecision(self, precision):
        self.startSpinBox.setDecimals(precision)
        self.stopSpinBox.setDecimals(precision)

    def _setEnabled(self, enabled):
        self.startSpinBox.setEnabled(enabled)
        self.stopSpinBox.setEnabled(enabled)
        self.stepSpinBox.setEnabled(enabled)

    @QtCore.pyqtSignature("QString")
    def on_mneComboBox_currentIndexChanged(self, motorMne):
        if motorMne:
            self._motor = self.specRunner.getMotor(str(motorMne))
            self._connectMotor()
            self._setEnabled(True)
            self.motorReady.emit(True)
        else:
            self._motor = None
            self._setEnabled(False)
            self.motorReady.emit(False)

        self._limitsChanged(self.limits)
        self._setPrecision(self.precision)

        if motorMne:
            self._setStartPosition(self._motor.getScanBoundStart())
            self._setStopPosition(self._motor.getScanBoundStop())

            settings = QtCore.QSettings()
            settings.beginGroup("%s/%s"%(self.__class__, self._direction))
            settings.setValue(
                'motorMne',
                QtCore.QVariant(self.mneComboBox.currentText())
            )
        else:
            self._setStartPosition(0)
            self._setStopPosition(0)

    def _setStartPosition(self, val):
        self.startSpinBox.setValue(val)

    def _setStopPosition(self, val):
        self.stopSpinBox.setValue(val)

    def getScanArgs(self, steps=True):
        args = [self.motorMne, self.start, self.stop]
        if steps:
            args.append(self.steps)

        return args


class AScanMotorWidget(ScanMotorWidget):
    pass


class DScanMotorWidget(ScanMotorWidget):

    @property
    def limits(self):
        try:
            low, high = self._motor.getLimits()
            low -= self.position
            high -= self.position
            return [low, high]
        except AttributeError:
            return [-1, 1]

    def _connectMotor(self):
        ScanMotorWidget._connectMotor(self)
        if self._motor:
            self._motor.positionChanged.connect(
                lambda: self._limitsChanged(self.limits)
                )

    def _setStartPosition(self, val):
        self.startSpinBox.setValue(val - self.position)

    def _setStopPosition(self, val):
        self.stopSpinBox.setValue(val - self.position)


class MeshMotorWidget(ScanMotorWidget):
    pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('Praxes')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
