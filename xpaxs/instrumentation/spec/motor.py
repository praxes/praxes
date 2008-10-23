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

from xpaxs.instrumentation.spec import TEST_SPEC

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.instrumentation.spec.client.motor')

[NOTINITIALIZED,UNUSABLE,READY,MOVESTARTED,MOVING,ONLIMIT]=[0,1,2,3,4,5]


class QtSpecMotorBase(SpecMotor.SpecMotorA, QtCore.QObject):

    __state_strings = ['NOTINITIALIZED',
                       'UNUSABLE',
                       'READY',
                       'MOVESTARTED',
                       'MOVING',
                       'ONLIMIT']

    def __init__(self, specName=None, specVersion=None):
        QtCore.QObject.__init__(self)
        SpecMotor.SpecMotorA.__init__(self, str(specName), str(specVersion))
        self.getPosition()

    def connected(self):
        logger.debug('Motor %s connected',self.specName)

    def disconnected(self):
        logger.debug('Motor %s disconnected',self.specName)

    def motorLimitsChanged(self):
        limits = self.getLimits()
        self.emit(QtCore.SIGNAL("limitsChanged(PyQt_PyObject)"),
                  limits)
        logger.debug("Motor %s limits changed to (%s,%s)",self.specName,
                                                           limits[0],limits[1])

    def motorPositionChanged(self, absolutePosition):
        self.emit(QtCore.SIGNAL("positionChanged(PyQt_PyObject)"),
                  absolutePosition)
        logger.debug("Motor %s position changed to %s",self.specName,
                                                           absolutePosition)

    def syncQuestionAnswer(self, specSteps, controllerSteps):
        logger.debug( "Motor %s syncing",self.specName)

    def motorStateChanged(self, state):
        state = self.__state_strings[state]
        self.emit(QtCore.SIGNAL("stateChanged(PyQt_PyObject)"),
                  state)
        logger.debug( "Motor %s state changed to %s",self.specName, state)

    def getState(self):
        state = SpecMotor.SpecMotorA.getState(self)
        return self.__state_strings[state]


class TestQtSpecMotor(QtSpecMotorBase):

    __state_strings = ['NOTINITIALIZED',
                       'UNUSABLE',
                       'READY',
                       'MOVESTARTED',
                       'MOVING',
                       'ONLIMIT']
    def __init__(self,mne,specVersion = None):

        QtCore.QObject.__init__(self)
        self.specName = mne
        self.position = len(mne)*10
        self.toGoTo=0
        self.limits=(len(mne),len(mne)*1000)
        self.paramdict = {'step_size':len(mne)*1000,
                                'slew_rate':len(mne)*1000,
                                'acceleration':len(mne)*10}


        self.state = READY
        self.Timer = QtCore.QTimer()
        self.time =len(mne)*1000

        self.connect(self.Timer, QtCore.SIGNAL('timeout()'), self.end)
        logger.debug("Motor %s is in Test Mode",self.specName)
    def getPosition(self):
        return self.position

    def getParameter(self,parameter):
        return self.paramdict[parameter]

    def getState(self):
        return self.__state_strings[self.state]

    def getLimits(self):
        return self.limits

    def move(self,amount=0):
        if self.state in (READY,ONLIMIT):
            self.Timer.start(self.time)
            self.state = MOVING
            self.toGoTo=amount
            self.motorStateChanged(self.state)

    def end(self):
        self.Timer.stop()
        self.state = READY
        self.motorStateChanged(self.state)
        self.position=self.toGoTo
        self.motorPositionChanged(self.getPosition())


if TEST_SPEC:
    class QtSpecMotorA(TestQtSpecMotor):
        pass
else:
    class QtSpecMotorA(QtSpecMotorBase):
        pass


if __name__ == "__main__":
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
    print
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
    print
    m = QtSpecMotorA('samz', 'f3.chess.cornell.edu:xrf')
