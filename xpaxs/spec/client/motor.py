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

from PyQt4 import QtCore
from SpecClient import SpecMotor

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = 0

#    def readParam(self,motor):
#        motor = self._motors[motor]
#        value = []
#        for param in self._param_names:
#            try:
#                value.append(motor.getParameter(param))
#            except:
#                value.append("unable to get value")
#            self._parameters[motor] = value
#        return self._parameters[motor]


class QtSpecMotorA(SpecMotor.SpecMotorA, QtCore.QObject):

    __state_strings = ['NOTINITIALIZED',
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
        if DEBUG: print'Motor %s connected'%self.specName

    def disconnected(self):
        if DEBUG: print 'Motor %s disconnected'%self.specName

    def motorLimitsChanged(self):
        limits = self.getLimits()
        self.emit(QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                  limits)
        if DEBUG:
            limitString = "(" + str(limits[0])+", "+ str(limits[1]) + ")"
            print "Motor %s limits changed to %s"%(self.specName,limitString)

    def motorPositionChanged(self, absolutePosition):
        self.emit(QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                  absolutePosition)
        if DEBUG: print "Motor %s position changed to %s"%(self.specName,
                                                           absolutePosition)

    def syncQuestionAnswer(self, specSteps, controllerSteps):
        if DEBUG: print "Motor %s syncing"%self.specName

    def motorStateChanged(self, state):
        state = self.__state_strings[state]
        self.emit(QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                  state)
        if DEBUG: print "Motor %s state changed to %s"%(self.specName, state)

    def getState(self):
        state = SpecMotor.SpecMotorA.getState(self)
        return self.__state_strings[state]


if __name__ == "__main__":
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
    print
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
    print
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
