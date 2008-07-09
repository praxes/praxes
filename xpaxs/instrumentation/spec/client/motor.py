"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
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

logger = logging.getLogger('XPaXS.spec.client.motor')



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
        logger.debug('Motor %s connected',self.specName)

    def disconnected(self):
        logger.debug('Motor %s disconnected',self.specName)

    def motorLimitsChanged(self):
        limits = self.getLimits()
        self.emit(QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                  limits)
        logger.debug("Motor %s limits changed to (%s,%s)",self.specName,
                                                           limits[0],limits[1])

    def motorPositionChanged(self, absolutePosition):
        self.emit(QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                  absolutePosition)
        logger.debug("Motor %s position changed to %s",self.specName,
                                                           absolutePosition)

    def syncQuestionAnswer(self, specSteps, controllerSteps):
        logger.debug( "Motor %s syncing",self.specName)

    def motorStateChanged(self, state):
        state = self.__state_strings[state]
        self.emit(QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),
                  state)
        logger.debug( "Motor %s state changed to %s",self.specName, state)

    def getState(self):
        state = SpecMotor.SpecMotorA.getState(self)
        return self.__state_strings[state]


if __name__ == "__main__":
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
    print
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
    print
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
