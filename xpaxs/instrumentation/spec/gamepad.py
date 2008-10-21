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
#--------------------------------------------------------------------------


class GamePad(ui_gamepad.Ui_GamePad, QtGui.QWidget):

    """Establishes motor pad"""

    def __init__(self, specRunner=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.setDefaultShortcuts()
        self.locationDict = {}
        self.nsEnabled = False
        self.ewEnabled = False

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

    @property
    def northSouthMotorWidget(self):
        return self._northSouthMotorWidget

    @property
    def eastWestMotorWidget(self):
        return self._eastWestMotorWidget

    def relativeMove(self, *args):
        self.specRunner( 'mvr ' + ' '.join( str(arg) for arg in args ) )

    @QtCore.pyqtSignature("")
    def on_westButton_clicked(self):
        self.relativeMove(
            self.eastWestMotorWidget.motorMne,
            -self.eastWestMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_eastButton_clicked(self):
        self.relativeMove(
            self.eastWestMotorWidget.motorMne,
            self.eastWestMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_northButton_clicked(self):
        self.relativeMove(
            self.northSouthMotorWidget.motorMne,
            self.northSouthMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_southButton_clicked(self):
        self.relativeMove(
            self.northSouthMotorWidget.motorMne,
            -self.northSouthMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_northwestButton_clicked(self):
        self.relativeMove(
            self.northSouthMotorWidget.motorMne,
            self.northSouthMotorWidget.stepSize,
            self.eastWestMotorWidget.motorMne,
            -self.eastWestMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_northeastButton_clicked(self):
        self.relativeMove(
            self.northSouthMotorWidget.motorMne,
            self.northSouthMotorWidget.stepSize,
            self.eastWestMotorWidget.motorMne,
            self.eastWestMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_southwestButton_clicked(self):
        self.relativeMove(
            self.northSouthMotorWidget.motorMne,
            -self.northSouthMotorWidget.stepSize,
            self.eastWestMotorWidget.motorMne,
            -self.eastWestMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_southeastButton_clicked(self):
        self.relativeMove(
            self.northSouthMotorWidget.motorMne,
            -self.northSouthMotorWidget.stepSize,
            self.eastWestMotorWidget.motorMne,
            self.eastWestMotorWidget.stepSize
        )

    @QtCore.pyqtSignature("")
    def on_stopButton_clicked(self):
        self.stopButton.setEnabled(False)
        self.specRunner.abort()

    @QtCore.pyqtSignature("")
    def on_moveButton_clicked(self):
        args = []

        if self.northSouthMotorWidget.motorMne:
            args.append(self.northSouthMotorWidget.motorMne)
            args.append(self.northSouthMotorWidget.nextPosition)

        if self.eastWestMotorWidget.motorMne:
            args.append(self.eastWestMotorWidget.motorMne)
            args.append(self.eastWestMotorWidget.nextPosition)

        self.specRunner( 'mv ' + ' '.join( str(arg) for arg in args ) )

    def setDefaultShortcuts(self):
        self.westButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left))
        self.eastButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right))
        self.northButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up))
        self.southButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down))
        self.northwestButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Home))
        self.northeastButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageUp))
        self.southwestButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_End))
        self.southeastButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageDown))
        self.stopButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space))

    def _stateChanged(self, state):
        self.stopButton.setEnabled(state == 'MOVING')
        self.moveButton.setEnabled('READY' in state)

        enabled = state in ('EWREADY', 'READY')
        self.eastButton.setEnabled(enabled)
        self.westButton.setEnabled(enabled)

        enabled = state in ('NSREADY', 'READY')
        self.northButton.setEnabled(enabled)
        self.southButton.setEnabled(enabled)

        enabled = state == 'READY'
        self.northwestButton.setEnabled(enabled)
        self.northeastButton.setEnabled(enabled)
        self.southwestButton.setEnabled(enabled)
        self.southeastButton.setEnabled(enabled)

        # TODO: is this next line necessary? Not with Qt-4.4.2:
        QtGui.qApp.processEvents()

    def _northSouthMotorStateChanged(self, state):

        if state in ('NOTINITIALIZED', 'UNUSABLE') and \
            self.eastWestMotorWidget.state in ('NOTINITIALIZED', 'UNUSABLE'):
            self._stateChanged('UNUSABLE')

        elif state in ('MOVESTARTED', 'MOVING') or \
            self.eastWestMotorWidget.state in ('MOVESTARTED', 'MOVING'):
            self._stateChanged('MOVING')

        elif state in ('READY', 'ONLIMIT') and \
            self.eastWestMotorWidget.state in ('READY', 'ONLIMIT'):
            self._stateChanged('READY')

        else:
            self._stateChanged('NSREADY')

    def _eastWestMotorStateChanged(self, state):

        if state in ('NOTINITIALIZED', 'UNUSABLE') and \
            self.northSouthMotorWidget.state in ('NOTINITIALIZED', 'UNUSABLE'):
            self._stateChanged('UNUSABLE')

        elif state in ('MOVESTARTED', 'MOVING') or \
            self.northSouthMotorWidget.state in ('MOVESTARTED', 'MOVING'):
            self._stateChanged('MOVING')

        elif state in ('READY', 'ONLIMIT') and \
            self.northSouthMotorWidget.state in ('READY', 'ONLIMIT'):
            self._stateChanged('READY')

        else:
            self._stateChanged('EWREADY')

#    @QtCore.pyqtSignature("")
#    def on_saveLocationButton_clicked(self):
#        pass
#
#    @QtCore.pyqtSignature("QString")
#    def on_savedLocationComboBox_currentIndexChanged(self, pos):
#        pass
#
#    @QtCore.pyqtSignature("")
#    def on_deleteLocationButton_clicked(self):
#        pass


if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('test')
    myapp = GamePad()
    myapp.show()
    sys.exit(app.exec_())
