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

from xpaxs.instrumentation.spec.ui import ui_gamepad
from xpaxs.instrumentation.spec import TEST_SPEC
from xpaxs.instrumentation.spec.motorwidget import MotorWidget

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

'''Needs CHESS macro mmv and mmvr'''

cmds = ('umvr %s %s','mmvr %s %s %s %s','mmv %s %s %s %s')



class GamePad(ui_gamepad.Ui_GamePad, QtGui.QWidget):

    """Establishes motor pad"""

    def __init__(self, specRunner=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.setDefaultShortcuts()
        self.positionDict = {}

        if specRunner:
            self.specRunner = specRunner
        elif not TEST_SPEC:
            from xpaxs.instrumentation.spec.specconnect import SpecConnect
            self.specRunner = SpecConnect()#.exec_()
        else:
            from xpaxs.instrumentation.spec.runner import TestSpecRunner
            self.specRunner = TestSpecRunner()

        motorsMne = self.specRunner.getMotorsMne()
        self.northSouthMotorWidget = MotorWidget(
            'N/S Motor', motorsMne[0], specRunner, self
        )
        self.eastWestMotorWidget = MotorWidget(
            'E/W Motor', motorsMne[1], specRunner, self
        )

        self.vboxlayout1.insertWidget(0, self.eastWestMotorWidget)
        self.vboxlayout1.insertWidget(0, self.northSouthMotorWidget)

        self.connect(
            self.eastWestMotorWidget,
            QtCore.SIGNAL("stateChanged(PyQt_PyObject)"),
            self.eastWestMotorStateChanged
        )
        self.connect(
            self.northSouthMotorWidget,
            QtCore.SIGNAL("stateChanged(PyQt_PyObject)"),
            self.northSouthMotorStateChanged
        )

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

#        self.connect(
#            self.saveButton,
#            QtCore.SIGNAL("pressed()"),
#            self.savePosition
#        )
#        self.connect(
#            self.moveButton,
#            QtCore.SIGNAL("pressed()"),
#            self.moveToPosition
#        )
#        self.connect(
#            self.delButton,
#            QtCore.SIGNAL("pressed()"),
#            self.delPosition
#        )
#        self.connect(
#            self.savedPosComboBox,
#            QtCore.SIGNAL('currentIndexChanged(int)'),
#            self.loadPosition
#        )
#
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
#
##    def setButtonShortcut(self,button,key):
##        #I still need to implement Its use for customization
##        button.setShortcut(QtGui.QKeySequence(key))
#

    def setButtonsEnabled(self, val):
#        self.positionFrame.setEnabled(val)
#        self.motorFrame.setEnabled(val)
        self.eastButton.setEnabled(val)
        self.westButton.setEnabled(val)
        self.northButton.setEnabled(val)
        self.southButton.setEnabled(val)
        self.northwestButton.setEnabled(val)
        self.northeastButton.setEnabled(val)
        self.southwestButton.setEnabled(val)
        self.southeastButton.setEnabled(val)
        self.stopButton.setEnabled(not val)
        # TODO: is this next line necessary? Yes, in Qt-4.4.1:
        QtGui.qApp.processEvents()

#####MOTOR GUI INTERACTIONS######

    def northSouthMotorStateChanged(self, state):
        if state in ('READY', 'ONLIMIT'):
            if self.eastWestMotorWidget.state in ('READY', 'ONLIMIT'):
                self.setButtonsEnabled(True)
                return

        self.setButtonsEnabled(False)

    @QtCore.pyqtSignature("PyQt_PyObject")
    def eastWestMotorStateChanged(self, state):
        if state in ('READY', 'ONLIMIT'):
            if self.northSouthMotorWidget.state in ('READY', 'ONLIMIT'):
                self.setButtonsEnabled(True)
                return

        self.setButtonsEnabled(False)

#    def getState(self):
#        if self.northSouthMotorWidget._MotorMne:
#            udState = self.northSouthMotorWidget.getState()
#        else:
#            udState = 'NOTINITIALIZED'
#
#        if self.eastWestMotorWidget._MotorMne:
#            lrState = self.eastWestMotorWidget.getState()
#        else:
#            lrState = 'NOTINITIALIZED'
#        return [udState, lrState]
#
#    def motorStatesChanged(self, state):
#        if (
#            states[0] in ('READY', 'ONLIMIT') ) \
#            and \
#            (states[1] in ('READY', 'ONLIMIT') \
#        ):
#            print 'Both are READY'
#            self.emit(QtCore.SIGNAL("motorReady()"))
#            self.setButtons(True)
#        else:
#            print 'One or more are not READY'
#            self.emit(QtCore.SIGNAL("motorActive()"))
#            self.setButtons(False)
#
#####MOTOR ACTIONS#####
#



#
#    def savePosition(self):
#        ID = self.positionBox.currentText()
#        if ID:
#            self.positionDict[ID] = (
#                self.northSouthMotorWidget._MotorMne,
#                self.northSouthMotorWidget._Motor.getPosition(),
#                self.eastWestMotorWidget._MotorMne,
#                self.eastWestMotorWidget._Motor.getPosition()
#            )
#            if self.positionBox.findText(ID) == -1:
#                self.positionBox.addItem(ID)
#        self.positionBox.setCurrentIndex(0)
#
#    def loadPosition(self, index):
#        ID = self.positionBox.currentText()
#        if ID:
#            UDmotor, UDposition, LRmotor, LRposition = self.positionDict[ID]
#            self.northSouthMotorWidget.setMotor(UDmotor)
#            self.eastWestMotorWidget.setMotor(LRmotor)
#            self.northSouthMotorWidget.NameBox.setCurrentIndex(self.northSouthMotorWidget.NameBox.findText(UDmotor))
#            self.eastWestMotorWidget.NameBox.setCurrentIndex(self.eastWestMotorWidget.NameBox.findText(LRmotor))
#
#    def moveToPosition(self):
#        ID = self.positionBox.currentText()
#        if ID:
#            UDmotor, UD, LRmotor, LR = self.positionDict.get(ID)
#            cmd = cmds[2]%(UDmotor,UD,LRmotor,LR)
#            self.specRunner(cmd)
#            self.positionBox.setCurrentIndex(0)
#        else:
#            udPosition = self.udSlider.value()*0.001
#            lrPosition = self.lrSlider.value()*0.001
#            self.move(2,udPosition,lrPosition)
#        self.aborted = False
#
#    def delPosition(self):
#        if self.positionBox.currentText():
#            self.positionBox.removeItem(self.positionBox.currentIndex())


if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('test')
    myapp = GamePad()
    myapp.show()
    sys.exit(app.exec_())
