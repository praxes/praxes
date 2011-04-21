"""
"""

#import logging
import os
import sys

from PyQt4 import QtCore
from SpecClient import SpecMotor

from . import TEST_SPEC


#logger = logging.getLogger(__file__)

[NOTINITIALIZED,UNUSABLE,READY,MOVESTARTED,MOVING,ONLIMIT]=[0,1,2,3,4,5]


class QtSpecMotorA(SpecMotor.SpecMotorA, QtCore.QObject):

    __state_strings = ['NOTINITIALIZED',
                       'UNUSABLE',
                       'READY',
                       'MOVESTARTED',
                       'MOVING',
                       'ONLIMIT']

    limitsChanged = QtCore.pyqtSignal(tuple)
    positionChanged = QtCore.pyqtSignal(float)
    stateChanged = QtCore.pyqtSignal(str)
    scanBoundStartChanged = QtCore.pyqtSignal(float)
    scanBoundStopChanged = QtCore.pyqtSignal(float)

    def __init__(self, specName=None, specVersion=None):
        QtCore.QObject.__init__(self)
        SpecMotor.SpecMotorA.__init__(self, str(specName), str(specVersion))

        self._scanBoundStart = None
        self._scanBoundStop = None
        self._precision = self._getPrecision()

    def _getPrecision(self):
        try:
            stepsPerUnit = self.getParameter('step_size')
            stepSize = 1. / stepsPerUnit
            stepRes = len( str(stepSize).split('.')[-1] )
            resOrderMagniture = len( str(stepsPerUnit).split('.')[0] ) - 1

            if stepRes > resOrderMagniture:
                return resOrderMagniture + 1

            else:
                return resOrderMagniture

        except IndexError:
            return 0

    def getPrecision(self):
        return self._precision

    def getScanBoundStart(self):
        if self._scanBoundStart is None:
            return self.getPosition()
        else:
            return self._scanBoundStart

    def getScanBoundStop(self):
        if self._scanBoundStop is None:
            return self.getPosition() + 1
        else:
            return self._scanBoundStop

#    def connected(self):
#        logger.debug('Motor %s connected',self.specName)

#    def disconnected(self):
#        logger.debug('Motor %s disconnected',self.specName)

    def motorLimitsChanged(self):
        limits = self.getLimits()
        self.limitsChanged.emit(self.getLimits())
#        logger.debug("Motor %s limits changed to (%s,%s)",self.specName,
#                                                           limits[0],limits[1])

    def motorPositionChanged(self, absolutePosition):
        self.positionChanged.emit(absolutePosition)
#        logger.debug("Motor %s position changed to %s",self.specName,
#                                                           absolutePosition)

#    def syncQuestionAnswer(self, specSteps, controllerSteps):
#        logger.debug( "Motor %s syncing",self.specName)

    def motorStateChanged(self, state):
        state = self.__state_strings[state]
        self.stateChanged.emit(state)
#        logger.debug( "Motor %s state changed to %s",self.specName, state)

    def getState(self):
        state = SpecMotor.SpecMotorA.getState(self)
        return self.__state_strings[state]

    def setScanBoundStart(self, val):
        self._scanBoundStart = val
        self.scanBoundStartChanged.emit(val)

    def setScanBoundStop(self, val):
        self._scanBoundStop = val
        self.scanBoundStopChanged.emit(val)
