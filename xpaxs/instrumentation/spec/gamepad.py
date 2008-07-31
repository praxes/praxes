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

SPEC = False
if SPEC:
    try:
        from xpaxs.instrumentation.spec.specconnect import SpecConnect
    except ImportError:
        from TestRunner import TestSpecRunner as runner
        print 'Could not find SpecConnect'
else:
    from TestRunner import TestSpecRunner as runner


#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

'''Needs CHESS macro mmv and mmvr'''


cmds = ('umvr %s %s','mmvr %s %s %s %s','mmv %s %s %s %s')



class Pad(ui_gamepad.Ui_Pad, QtGui.QWidget):

    """Establishes motor pad"""

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setDefaultShortcuts()
        self.aborted = True
        self.positionDict = {}
        self._LRmotor = None
        self._UDmotor = None


        if parent:
            self.setParent(parent)
            self.specRunner = parent.specRunner
        elif SPEC:
            self.specRunner = SpecConnect().exec_()
        else:
            self.specRunner = runner()
        self.motors = motors = self.specRunner.getMotorsMne()
        self.setLRMotor(motors[0], self.specRunner.specVersion)
        self.setUDMotor(motors[1], self.specRunner.specVersion)
        self.lrNameBox.addItems(motors)
        self.udNameBox.addItems(motors)
        self.lrNameBox.setCurrentIndex(0)
        self.udNameBox.setCurrentIndex(1)
        self.motorStatesChanged(self.getState())


        self.connect(self.lrNameBox,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda int : self.setLRMotor(motors[int]) )
        self.connect(self.udNameBox,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda int : self.setUDMotor(motors[int]) )


        self.connect(self.leftButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self._LRmotor, -1*self.lrSpin.value() ) )
        self.connect(self.rightButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self._LRmotor, self.lrSpin.value() ) )
        self.connect(self.upButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self._UDmotor, self.udSpin.value() ) )
        self.connect(self.downButton,
                     QtCore.SIGNAL("pressed()"),
                     lambda : self.move(0,self._UDmotor, -1*self.udSpin.value() ) )


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

#############################


        self.connect(self.udSlider,
                     QtCore.SIGNAL("sliderMoved(int)"),
                     self.udSliderMoved)
        self.connect(self.udPositionSpin,
                     QtCore.SIGNAL("editingFinished()"),
                     self.udPositionEdited)
        self.connect(self.udSlider,
                     QtCore.SIGNAL('sliderReleased()'),
                     self.udSliderReleased)
        self.connect(self.udSlider,
                     QtCore.SIGNAL('sliderPressed()'),
                     self.udSliderPressed)

#############################
        self.connect(self.lrSlider,
                     QtCore.SIGNAL("sliderMoved(int)"),
                     self.lrSliderMoved)
        self.connect(self.lrPositionSpin,
                     QtCore.SIGNAL("editingFinished()"),
                     self.lrPositionEdited)
        self.connect(self.lrSlider,
                     QtCore.SIGNAL('sliderReleased()'),
                     self.lrSliderReleased)
        self.connect(self.lrSlider,
                     QtCore.SIGNAL('sliderPressed()'),
                     self.lrSliderPressed)



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
        self.positionFrame.setEnabled(Bool)
        self.motorFrame.setEnabled(Bool)
        self.rightButton.setEnabled(Bool)
        self.leftButton.setEnabled(Bool)
        self.upButton.setEnabled(Bool)
        self.downButton.setEnabled(Bool)
        self.ulButton.setEnabled(Bool)
        self.urButton.setEnabled(Bool)
        self.dlButton.setEnabled(Bool)
        self.drButton.setEnabled(Bool)
        self.centerButton.setDisabled(Bool)


####MOTOR GUI INTERACTIONS######

    def getState(self):
        if self._UDmotor:
            self.udState = self.specRunner.getMotor(self._UDmotor).getState()
        else:
            self.udState = 'NOTINITIALIZED'
            
        if self._LRmotor:
            self.lrState = self.specRunner.getMotor(self._LRmotor).getState()
        else:
            self.lrState = 'NOTINITIALIZED'
        return [self.udState, self.lrState]

    def motorStatesChanged(self, states):
        if states[0] in ('READY', 'ONLIMIT') and states[1] in ('READY', 'ONLIMIT'):
            self.emit(QtCore.SIGNAL("motorReady()"))
            self.setButtons(True)
        else:
            self.emit(QtCore.SIGNAL("motorActive()"))
            self.setButtons(False)

    def setUDMotor(self, motor, hostport = None):
        if self._UDmotor:
            UD=self.specRunner.getMotor(self._UDmotor)
            self.disconnect(UD,
                         QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                         self.setUDPosition)
            self.disconnect(UD,
                         QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                         self.setUDLimits)
            self.disconnect(UD,
                         QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                         self.udStateChanged)
        self._UDmotor = motor
        UD = self.specRunner.getMotor(self._UDmotor)
        self.udState=UD.getState()
        self.setUDLimits(UD.getLimits())
        position = UD.getPosition()
        self.setUDPosition(position)
        self.udSlider.setValue(int(position*1000))
        self.udPositionSpin.setValue(position)
        self.motorStatesChanged(self.getState())
        self.connect(UD,
                     QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                     self.setUDPosition)
        self.connect(UD,
                     QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                     self.setUDLimits)
        self.connect(UD,
                     QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                     self.udStateChanged)

    def setUDPosition(self, position):
        self.udPositionSpin.setValue(position)
        self.udPositionSpin.defaultValue=position

    def setUDLimits(self, limits):
        low, high = limits
        self.udPositionSpin.setRange(low, high)
        self.udSlider.setRange(low*1000,high*1000)

    def udStateChanged(self, state):
        self.udState = state
        self.motorStatesChanged([self.udState, self.lrState])

    def udSliderReleased(self):
        self.udPositionSpin.setValue(self.udPositionSpin.defaultValue)
    
    def udSliderMoved(self, int):
        self.udPositionSpin.setValue(int*0.001)
        
    def udSliderPressed(self):
        self.udPositionSpin.setValue(self.udSlider.value()*0.001)
        
    def udPositionEdited(self):
        if self.udPositionSpin.hasFocus():
            self.udSlider.setValue(int(self.udPositionSpin.value()*1000))
        self.udPositionSpin.setValue(self.udPositionSpin.defaultValue)
        

#############################################################

    def setLRMotor(self, motor, hostport = None):
        if self._LRmotor:
            LR=self.specRunner.getMotor(self._LRmotor)
            self.disconnect(LR,
                         QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                         self.setLRPosition)
            self.disconnect(LR,
                         QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                         self.setLRLimits)
            self.disconnect(LR,
                         QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                         self.lrStateChanged)
        self._LRmotor = motor
        LR = self.specRunner.getMotor(self._LRmotor)
        self.lrState=LR.getState()
        self.setLRLimits(LR.getLimits())
        position = LR.getPosition()
        self.setLRPosition(position)
        self.lrSlider.setValue(int(position*1000))
        self.lrPositionSpin.setValue(position)
        self.motorStatesChanged(self.getState())
        self.connect(LR,
                     QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                     self.setLRPosition)
        self.connect(LR,
                     QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                     self.setLRLimits)
        self.connect(LR,
                     QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                     self.lrStateChanged)

    def setLRPosition(self, position):
        self.lrPositionSpin.setValue(position)
        self.lrPositionSpin.defaultValue=position

    def setLRLimits(self, limits):
        low, high = limits
        self.lrPositionSpin.setRange(low, high)
        self.lrSlider.setRange(low*1000,high*1000)

    def lrStateChanged(self, state):
        self.lrState = state
        self.motorStatesChanged(self.getState())

    def lrSliderReleased(self):
        self.lrPositionSpin.setValue(self.lrPositionSpin.defaultValue)
    
    def lrSliderMoved(self, int):
        self.lrPositionSpin.setValue(int*0.001)
        
    def lrSliderPressed(self):
        self.lrPositionSpin.setValue(self.lrSlider.value()*0.001)
        
    def lrPositionEdited(self):
        if self.lrPositionSpin.hasFocus():
            self.lrSlider.setValue(int(self.lrPositionSpin.value()*1000))
        self.lrPositionSpin.setValue(self.lrPositionSpin.defaultValue)

####MOTOR ACTIONS#####

    def move(self,orders,inputOne,inputTwo):
        if orders == 0:
            cmd = cmds[orders]%(inputOne,inputTwo)
        elif orders in (1,2):
            cmd = cmds[orders]%(self._UDmotor,inputOne,self._LRmotor,inputTwo)
        else:
            cmd = 'Unknown Command'
        self.specRunner(cmd)
        self.aborted = False

    def stop(self):
        if not self.aborted :
            self.specRunner.abort()
            self.aborted = True

    def savePosition(self):
        ID = self.positionBox.currentText()
        if ID:
            UD = self.specRunner.getMotor(self._UDmotor).getPosition()
            LR = self.specRunner.getMotor(self._LRmotor).getPosition()
            self.positionDict[ID] = (self._UDmotor,UD,self._LRmotor,LR)
            if self.positionBox.findText(ID) ==-1: self.positionBox.addItem(ID)
        self.positionBox.setCurrentIndex(0)

    def loadPosition(self, index):
        ID = self.positionBox.currentText()
        if ID:
            UDmotor,UDposition,LRmotor,LRposition = self.positionDict[ID]
            self.setUDMotor(UDmotor)
            self.setLRMotor(LRmotor)
            self.udNameBox.setCurrentIndex(self.udNameBox.findText(UDmotor))
            self.lrNameBox.setCurrentIndex(self.lrNameBox.findText(LRmotor))
            
            


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
        
    def  delPosition(self):
        if self.positionBox.currentText():
            self.positionBox.removeItem(self.positionBox.currentIndex())

    def positionBoxReturned(self):
        self.positionBox.setCurrentIndex(0)






if __name__  ==  "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('test')
    myapp = Pad()
    myapp.show()
    sys.exit(app.exec_())
