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

from xpaxs.instrumentation.spec.ui import ui_gamepad
from xpaxs.instrumentation.spec import TEST_SPEC
from xpaxs.instrumentation.spec.motorwidget import MotorWidget

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class GamePad(ui_gamepad.Ui_GamePad, QtGui.QWidget):

    """Establishes motor pad"""

    def __init__(self, specRunner=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # TODO: isnt there a way to do a stacked layout in Designer?
        self.startStopStackedLayout = QtGui.QStackedLayout(
            self.startStopButtonFrame
        )
        self.startStopStackedLayout.setContentsMargins(0, 0, 0, 0)
        self.startStopStackedLayout.addWidget(self.startButton)
        self.startStopStackedLayout.addWidget(self.stopButton)

        if specRunner:
            self.specRunner = specRunner

        elif not TEST_SPEC:
            from xpaxs.instrumentation.spec.specconnect import SpecConnect
            self.specRunner = SpecConnect()#.exec_()

        else:
            from xpaxs.instrumentation.spec.runner import TestSpecRunner
            self.specRunner = TestSpecRunner()

        self._northSouthMotorWidget = MotorWidget(
            'N/S Motor', specRunner, self
        )
        self._eastWestMotorWidget = MotorWidget(
            'E/W Motor', specRunner, self
        )
        self._stateChanged(
            nsState=self.northSouthMotorWidget.state,
            ewState=self.eastWestMotorWidget.state
        )

        self.vboxlayout1.insertWidget(0, self.eastWestMotorWidget)
        self.vboxlayout1.insertWidget(0, self.northSouthMotorWidget)

        self.connect(
            self.eastWestMotorWidget,
            QtCore.SIGNAL("stateChanged(PyQt_PyObject)"),
            self._eastWestMotorStateChanged
        )
        self.connect(
            self.northSouthMotorWidget,
            QtCore.SIGNAL("stateChanged(PyQt_PyObject)"),
            self._northSouthMotorStateChanged
        )
        self.connect(
            self.eastWestMotorWidget,
            QtCore.SIGNAL("nextPositionIsCurrent(PyQt_PyObject)"),
            self.startButton.setDisabled
        )
        self.connect(
            self.northSouthMotorWidget,
            QtCore.SIGNAL("nextPositionIsCurrent(PyQt_PyObject)"),
            self.startButton.setDisabled
        )

    @property
    def northSouthMotorWidget(self):
        return self._northSouthMotorWidget

    @property
    def eastWestMotorWidget(self):
        return self._eastWestMotorWidget

    def _absoluteMove(self):
        args = []

        if self.northSouthMotorWidget.motorMne:
            args.append(self.northSouthMotorWidget.motorMne)
            args.append(self.northSouthMotorWidget.nextPosition)

        if self.eastWestMotorWidget.motorMne:
            args.append(self.eastWestMotorWidget.motorMne)
            args.append(self.eastWestMotorWidget.nextPosition)

        self.specRunner( 'mv ' + ' '.join( str(arg) for arg in args ) )

    def _relativeMove(self, *args):
        self.specRunner( 'mvr ' + ' '.join( str(arg) for arg in args ) )

    def _stopMove(self):
        self.stopButton.setDisabled(True)
        self.specRunner.abort()

    # navigation pad

    def _gamepadButtonClicked(self, nsDir=None, ewDir=None):
        cmdArgs = []
        if nsDir:
            cmdArgs.extend(
                [self.northSouthMotorWidget.motorMne,
                 nsDir*self.northSouthMotorWidget.stepSize
                ]
            )

        if ewDir:
            cmdArgs.extend(
                [self.eastWestMotorWidget.motorMne,
                 ewDir*self.eastWestMotorWidget.stepSize
                ]
            )

        self._relativeMove(*cmdArgs)

    def setBusy(self, busy):
        self.setDisabled(busy)

    @QtCore.pyqtSignature("")
    def on_eastButton_clicked(self):
        self._gamepadButtonClicked(ewDir=1)

    @QtCore.pyqtSignature("")
    def on_northButton_clicked(self):
        self._gamepadButtonClicked(nsDir=1)

    @QtCore.pyqtSignature("")
    def on_northeastButton_clicked(self):
        self._gamepadButtonClicked(nsDir=1, ewDir=1)

    @QtCore.pyqtSignature("")
    def on_northwestButton_clicked(self):
        self._gamepadButtonClicked(nsDir=1, ewDir=-1)

    @QtCore.pyqtSignature("")
    def on_southButton_clicked(self):
        self._gamepadButtonClicked(nsDir=-1)

    @QtCore.pyqtSignature("")
    def on_southeastButton_clicked(self):
        self._gamepadButtonClicked(nsDir=-1, ewDir=1)

    @QtCore.pyqtSignature("")
    def on_southwestButton_clicked(self):
        self._gamepadButtonClicked(nsDir=-1, ewDir=-1)

    @QtCore.pyqtSignature("")
    def on_westButton_clicked(self):
        self._gamepadButtonClicked(ewDir=-1)

    @QtCore.pyqtSignature("")
    def on_startButton_clicked(self):
        self._absoluteMove()

    @QtCore.pyqtSignature("")
    def on_stopButton_clicked(self):
        self._stopMove()

    # GUI state

    def _eastWestMotorStateChanged(self, state):
        self._stateChanged(ewState=state)

    def _northSouthMotorStateChanged(self, state):
        self._stateChanged(nsState=state)

    def _stateChanged(self, nsState=None, ewState=None):

        if nsState is None:
            nsState = self.northSouthMotorWidget.state

        if ewState is None:
            ewState = self.eastWestMotorWidget.state

        nsEnabled = nsState not in ('NOTINITIALIZED', 'UNUSABLE')
        ewEnabled = ewState not in ('NOTINITIALIZED', 'UNUSABLE')
        bothEnabled = nsEnabled and ewEnabled
        eitherEnabled = nsEnabled or ewEnabled

        nsReady = nsState in ('READY', 'ONLIMIT')
        ewReady = ewState in ('READY', 'ONLIMIT')
        bothReady = nsReady and ewReady

        nsMoving = nsState in ('MOVESTARTED', 'MOVING')
        ewMoving = ewState in ('MOVESTARTED', 'MOVING')
        eitherMoving = nsMoving or ewMoving

        self.buttonFrame.setEnabled(eitherEnabled)

        if eitherMoving:
            self.startStopStackedLayout.setCurrentWidget(self.stopButton)
            self.stopButton.setEnabled(True)
            nsEnabled = ewEnabled = bothEnabled = False
            self.emit(QtCore.SIGNAL("specBusy"), True)

        else:
            self.stopButton.setEnabled(False)
            self.startStopStackedLayout.setCurrentWidget(self.startButton)
            self.emit(QtCore.SIGNAL("specBusy"), False)

        self.northButton.setEnabled(nsEnabled)
        self.southButton.setEnabled(nsEnabled)

        self.eastButton.setEnabled(ewEnabled)
        self.westButton.setEnabled(ewEnabled)

        self.northwestButton.setEnabled(bothEnabled)
        self.northeastButton.setEnabled(bothEnabled)
        self.southwestButton.setEnabled(bothEnabled)
        self.southeastButton.setEnabled(bothEnabled)


if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('test')
    myapp = GamePad()
    myapp.show()
    sys.exit(app.exec_())
