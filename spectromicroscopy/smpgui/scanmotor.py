"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from ui_scanmotor import Ui_ScanMotor
from spectromicroscopy.external.SpecClient import SpecMotor

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = 0

class TestSpecMotor(SpecMotor.SpecMotorA, QtCore.QObject):
    
    __state_strings__ = ['NOTINITIALIZED',
                         'UNUSABLE',
                         'READY',
                         'MOVESTARTED',
                         'MOVING',
                         'ONLIMIT']
    
    def __init__(self, specName=None, specVersion=None):
	QtCore.QObject.__init__(self)
        SpecMotor.SpecMotorA.__init__(self, specName, specVersion)
        self.getPosition()

    def connected(self):
        self.__connected__ = True
        if DEBUG: print'Motor %s connected'%self.specName
    
    def disconnected(self):
        self.__connected__ = False
        if DEBUG: print 'Motor %s disconnected'%self.specName

    def isConnected(self):
        if DEBUG: return (self.__connected__ != None) and (self.__connected__)

    def motorLimitsChanged(self):
        limits = self.getLimits()
        limitString = "(" + str(limits[0])+", "+ str(limits[1]) + ")"
        if DEBUG: print "Motor %s limits changed to %s"%(self.specName,limitString)
    
    def motorPositionChanged(self, absolutePosition):
        self.emit(QtCore.SIGNAL("motorPositionChanged"), absolutePosition)
        if DEBUG: print "Motor %s position changed to %s"%(self.specName,absolutePosition)
    
    def syncQuestionAnswer(self, specSteps, controllerSteps):
        if DEBUG: print "Motor %s syncing"%self.specName
    
    def motorStateChanged(self, state):
        if DEBUG: print "Motor %s state changed to %s"%(self.specName, self.__state_strings__[state])
    
    def status(self):
        if DEBUG: return self.__state_strings__[self.getState()]
    
    def motor_name(self):
        if DEBUG: return self.specName


class ScanMotor(Ui_ScanMotor, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent, motor, motorlist=[]):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.specrunner = parent.specrunner
        self.setupUi(self)
        
        self.motorComboBox.addItems(motorlist)
        try:
            ind = motorlist.index(motor)
            self.motorComboBox.setCurrentIndex(ind)
        except ValueError:
            motor = motorlist[0]
        self.setMotor(motor)
        
        self.connect(self.motorComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.setMotor)
        self.connect(self._motor,
                     QtCore.SIGNAL("motorPositionChanged"),
                     self.setPosition)
        
        

    def setMotor(self, motor):
        self._motor = motor = TestSpecMotor(motor, 'f3.chess.cornell.edu:xrf')
        self.setPosition(motor.getPosition())
    
    def setPosition(self, position):
        self.currentPosReport.setText('%.3f'%position)
