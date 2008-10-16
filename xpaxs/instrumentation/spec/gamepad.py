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



#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

'''Needs CHESS macro mmv and mmvr'''

cmds = ('umvr %s %s','mmvr %s %s %s %s','mmv %s %s %s %s')



class Pad(ui_gamepad.Ui_Pad, QtGui.QWidget):

    """Establishes motor pad"""

    def __init__(self, specRunner=None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setDefaultShortcuts()
        self.aborted = True
        self.positionDict = {}

        if specRunner:
            self.specRunner = specRunner
        elif not TEST_SPEC:
            from xpaxs.instrumentation.spec.specconnect import SpecConnect
            self.specRunner = SpecConnect()#.exec_()
        else:
            from xpaxs.instrumentation.spec.runner import TestSpecRunner as runner
            self.specRunner = runner()
        self.motors = motors = self.specRunner.getMotorsMne()

        self.ud = MotorWidget(self.udSlider,self.udSpin,\
                              self.udPositionSpin,self.udNameBox,\
                              motors,self.specRunner,self)
        self.lr = MotorWidget(self.lrSlider,self.lrSpin,\
                              self.lrPositionSpin,self.lrNameBox,\
                              motors,self.specRunner,self)

        self.connectGui()

        self.lr.setMotor(motors[0], self.specRunner.specVersion)
        self.ud.setMotor(motors[1], self.specRunner.specVersion)
        #delete next three lines
        self.lr.NameBox.setCurrentIndex(0)
        self.ud.NameBox.setCurrentIndex(1)
#        self.motorStatesChanged(self.getState())
#        self.connectGui()


    def connectGui(self):
        self.connect(self.ud, QtCore.SIGNAL('motorChanged()'), self.motorStatesChanged)
        self.connect(self.lr, QtCore.SIGNAL('motorChanged()'), self.motorStatesChanged)
        self.connect(self.ud, QtCore.SIGNAL('motorStateChanged()'), self.motorStatesChanged)
        self.connect(self.lr, QtCore.SIGNAL('motorStateChanged()'), self.motorStatesChanged)
        self.connect(self.leftButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self.lr._MotorMne, -1*self.lrSpin.value() ) )
        self.connect(self.rightButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self.lr._MotorMne, self.lrSpin.value() ) )
        self.connect(self.upButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self.ud._MotorMne, self.udSpin.value() ) )
        self.connect(self.downButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self.ud._MotorMne, -1*self.udSpin.value() ) )

        self.connect(self.ulButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda :  self.move(1,self.udSpin.value(),-1*self.lrSpin.value()) )
        self.connect(self.urButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda :  self.move(1,self.udSpin.value(),self.lrSpin.value()) )
        self.connect(self.dlButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda :  self.move(1,-1*self.udSpin.value(),-1*self.lrSpin.value() ) )
        self.connect(self.drButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda :  self.move(1,-1*self.udSpin.value(),self.lrSpin.value() ) )

        self.connect(self.centerButton, QtCore.SIGNAL("pressed()"), self.stop)

        self.connect(self.saveButton,QtCore.SIGNAL("pressed()"),self.savePosition)

        self.connect(self.loadButton,QtCore.SIGNAL("pressed()"),self.moveToPosition)

        self.connect(self.delButton,QtCore.SIGNAL("pressed()"),self.delPosition)

        self.connect(self.positionBox.lineEdit(),
                     QtCore.SIGNAL("returnPressed()"),
                     self.positionBoxReturned)
        self.connect(self.positionBox,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     self.loadPosition)

    def setDefaultShortcuts(self):
        self.leftButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left))
        self.rightButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right))
        self.upButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up))
        self.downButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down))
        self.ulButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Home))
        self.urButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageUp))
        self.dlButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_End))
        self.drButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageDown))
        self.centerButton.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space))

    def setButtonShortcut(self,button,key):
        #I still need to implement Its use for customization
        button.setShortcut(QtGui.QKeySequence(key))

    def setButtons(self, Bool):
        print "Buttons set to  %s"%Bool
#        self.positionFrame.setEnabled(Bool)
#        self.motorFrame.setEnabled(Bool)
        self.rightButton.setEnabled(Bool)
        self.leftButton.setEnabled(Bool)
        self.upButton.setEnabled(Bool)
        self.downButton.setEnabled(Bool)
        self.ulButton.setEnabled(Bool)
        self.urButton.setEnabled(Bool)
        self.dlButton.setEnabled(Bool)
        self.drButton.setEnabled(Bool)
        self.centerButton.setEnabled(not Bool)
        QtGui.qApp.processEvents()


####MOTOR GUI INTERACTIONS######

    def getState(self):
        if self.ud._MotorMne:
            udState = self.ud.getState()
        else:
            udState = 'NOTINITIALIZED'

        if self.lr._MotorMne:
            lrState = self.lr.getState()
        else:
            lrState = 'NOTINITIALIZED'
        return [udState, lrState]

    def motorStatesChanged(self):
        states = self.getState()
        if (states[0] in ('READY', 'ONLIMIT') )and (states[1] in ('READY', 'ONLIMIT')):
            print 'Both are READY'
            self.emit(QtCore.SIGNAL("motorReady()"))
            self.setButtons(True)
        else:
            print states
            print 'One or more are not READY'
            self.emit(QtCore.SIGNAL("motorActive()"))
            self.setButtons(False)



####MOTOR ACTIONS#####

    def move(self,orders,inputOne,inputTwo):
        if orders == 0:
            cmd = cmds[orders]%(inputOne,inputTwo)
        elif orders in (1,2):
            cmd = cmds[orders]%(self.ud._MotorMne,inputOne,self.lr._MotorMne,inputTwo)
        else:
            cmd = 'Unknown Command'
        self.specRunner(cmd)
        print "Running"
        self.aborted = False

    def stop(self):
        print 'aborting'
        if not self.aborted :
            self.specRunner.abort()
            self.aborted = True
            print 'aborted'

    def savePosition(self):
        ID = self.positionBox.currentText()
        if ID:
            self.positionDict[ID] = (self.ud._MotorMne,\
                                     self.ud._Motor.getPosition(),\
                                     self.lr._MotorMne,\
                                     self.lr._Motor.getPosition())
            if self.positionBox.findText(ID) ==-1: self.positionBox.addItem(ID)
        self.positionBox.setCurrentIndex(0)

    def loadPosition(self, index):
        ID = self.positionBox.currentText()
        if ID:
            UDmotor,UDposition,LRmotor,LRposition = self.positionDict[ID]
            self.ud.setMotor(UDmotor)
            self.lr.setMotor(LRmotor)
            self.ud.NameBox.setCurrentIndex(self.ud.NameBox.findText(UDmotor))
            self.lr.NameBox.setCurrentIndex(self.lr.NameBox.findText(LRmotor))




    def moveToPosition(self):
        ID = self.positionBox.currentText()
        if ID:
            (UDmotor,UD,LRmotor,LR) = self.positionDict.get(ID)
            cmd = cmds[2]%(UDmotor,UD,LRmotor,LR)
            self.specRunner(cmd)
            self.positionBox.setCurrentIndex(0)
        else:
            udPosition = self.udSlider.value()*0.001
            lrPosition = self.lrSlider.value()*0.001
            self.move(2,udPosition,lrPosition)
        self.aborted = False

    def delPosition(self):
        if self.positionBox.currentText():
            self.positionBox.removeItem(self.positionBox.currentIndex())

    def positionBoxReturned(self):
        self.positionBox.setCurrentIndex(0)


class MotorWidget(QtGui.QWidget):

    def __init__(self,Slider,Spin,PositionSpin,NameBox,motors,specRunner,parent):
        QtGui.QWidget.__init__(self,parent)
        self.parent=parent
        self.specRunner=specRunner
        self._MotorMne = None
        self.Slider=Slider
        self.Spin=Spin
        self.PositionSpin=PositionSpin
        self.NameBox=NameBox
        self.NameBox.addItems(motors)
        self.connect(self.NameBox,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda int : self.setMotor(motors[int]) )

        self.connect(self.Slider,
                     QtCore.SIGNAL("sliderMoved(int)"),
                     self.SliderMoved)
        self.connect(self.PositionSpin,
                     QtCore.SIGNAL("editingFinished()"),
                     self.PositionEdited)
        self.connect(self.Slider,
                     QtCore.SIGNAL('sliderReleased()'),
                     self.SliderReleased)
        self.connect(self.Slider,
                     QtCore.SIGNAL('sliderPressed()'),
                     self.SliderPressed)

    def __getattr__(self, attr):
        return getattr(self._Motor, attr)

    def setMotor(self, motor, hostport = None):
        if self._MotorMne:
            print "%s currently set"%self._MotorMne
            self.disconnect(self._Motor,
                         QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                         self.setPosition)
            self.disconnect(self._Motor,
                         QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                         self.setLimits)
            self.disconnect(self._Motor,
                         QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                         self.StateChanged)
        print "Defining %s as new motor"%motor
        self._MotorMne = motor
        self._Motor = self.specRunner.getMotor(self._MotorMne)
        self.setLimits(self._Motor.getLimits())
        position = self._Motor.getPosition()
        self.setPosition(position)
        self.Slider.setValue(int(position*1000))
        self.PositionSpin.setValue(position)


        self.connect(self._Motor,
                     QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                     self.setPosition)
        self.connect(self._Motor,
                     QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                     self.setLimits)
        self.connect(self._Motor,
                     QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                     self.StateChanged)

        self.emit(QtCore.SIGNAL("motorChanged()"))

    def setPosition(self, position):
        self.PositionSpin.setValue(position)
        self.PositionSpin.defaultValue=position

    def setLimits(self, limits):
        low, high = limits
        self.PositionSpin.setRange(low, high)
        self.Slider.setRange(low*1000,high*1000)

    def StateChanged(self, state):
        print "**************************Motor %s State Changed to %s*********************"%(self._MotorMne, state)
        self.emit(QtCore.SIGNAL("motorStateChanged()"))
#        self.parent.motorStatesChanged(self.parent.getState())

    def SliderReleased(self):
        self.PositionSpin.setValue(self.PositionSpin.defaultValue)

    def SliderMoved(self, int):
        self.PositionSpin.setValue(int*0.001)

    def SliderPressed(self):
        self.PositionSpin.setValue(self.Slider.value()*0.001)

    def PositionEdited(self):
        if self.PositionSpin.hasFocus():
            self.Slider.setValue(int(self.PositionSpin.value()*1000))
        self.PositionSpin.setValue(self.PositionSpin.defaultValue)








if __name__  ==  "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('test')
    myapp = Pad()
    myapp.show()
    sys.exit(app.exec_())
