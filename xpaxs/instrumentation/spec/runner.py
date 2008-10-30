"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
import os
import sys
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore
from SpecClient import Spec, SpecEventsDispatcher, SpecCommand, SpecVariable

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.motor import QtSpecMotorA
from xpaxs.instrumentation.spec.scan import QtSpecScanA
from xpaxs.instrumentation.spec import TEST_SPEC
#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.instrumentation.spec.runner')


def getSpecMacro(filename):
    temp = os.path.split(__file__)[0]
    filename = os.path.join(temp, 'macros', filename)
    return open(filename).read()


class Dispatcher(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.update)
        self.timer.start(20)

    def run(self):
        self.exec_()

    def update(self):
        SpecEventsDispatcher.dispatch()


class SpecDatafile(SpecVariable.SpecVariableA, QtCore.QObject):

    def __init__(self, varName=None, specVersion=None, specRunner=None):
        QtCore.QObject.__init__(self, specRunner)
        SpecVariable.SpecVariableA.__init__(self, varName, specVersion)

        self._specRunner = specRunner

    def setValue(self, fileName):
        self._specRunner('newfile %s'%fileName)
        specfile = self.getValue()

        specCreated = os.path.split(specfile)[-1]
        if fileName == specCreated:
            logger.debug("file %s created",fileName)
        else:
            logger.error('%s given %s returned',(fileName,specfile))
            self.fileError(fileName, specfile)

    def update(self, value):
        if not value == '/dev/null':
            self.emit(QtCore.SIGNAL("datafileChanged"), value)


class SpecRunnerBase(Spec.Spec, QtCore.QObject):
    """SpecRunner is our primary interface to Spec. Some caching is added,
    to improve performance.
    """

    def __init__(self, specVersion=None, timeout=None, parent=None):
        """specVersion is a string like 'foo.bar:spec' or '127.0.0.1:fourc'
        """
        QtCore.QObject.__init__(self, parent)
        Spec.Spec.__init__(self, specVersion, timeout)
        self.cmd = SpecCommand.SpecCommand('', specVersion, None)
        self.acmd = SpecCommand.SpecCommandA('', specVersion)
        self._datafile = SpecDatafile('DATAFILE', specVersion, self)

        self._motors = {}
        self._motorNames = []
        self._counterNames = []
        self.getMotorsMne()
        self.getCountersMne()

        self.runMacro('clientutils_sxfm.mac')
        self.runMacro('skipmode.mac')

#        self.dispatcher = Dispatcher(self)
#        self.dispatcher.start(QtCore.QThread.NormalPriority)
#########
        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.update)
        self.timer.start(20)

    def update(self):
        SpecEventsDispatcher.dispatch()
#########

    @property
    def datafile(self):
        return self._datafile

    def __call__(self, command, asynchronous=True):
        logger.debug("executing %s",command)

        if asynchronous:
            return self._acmd.executeCommand(command)

        else:
            return self._cmd.executeCommand(command)

    def close(self):
        try:
            self.dispatcher.exit()
            self.dispatcher.wait()
#            self.connection.dispatcher.disconnect()
        except:
            pass

    def getCountersMne(self):
        if len(self._counterNames) != self.getNumCounters():
            countersMne = self(
                "local md; for (i=0; i<COUNTERS; i++) { md[i]=cnt_mne(i); }; "
                "return md", asynchronous=False
            )
            keys = [int(i) for i in countersMne.keys()]
            keys.sort()
            self._counterNames = [countersMne[str(i)] for i in keys]
        return self._counterNames

    def getMotor(self, motorMne):
        if motorMne in self._motors:
            return self._motors[motorMne]

        else:
            motor = QtSpecMotorA(motorMne, self.specVersion)
            self._motors[motorMne] = motor
            return motor

    def getMotorMne(self, motorId):
        motorMne = self.motor_mne(motorId, function = True)
        if not motorMne in self._motorNames:
            self._motorNames.append(motorMne)
        return motorMne

    def getMotorsMne(self):
        if len(self._motorNames) != self.getNumMotors():
            motorsMne = self(
                "local md; for (i=0; i<MOTORS; i++) { md[i]=motor_mne(i); }; "
                "return md", asynchronous=False
            )
            keys = [int(i) for i in motorsMne.keys()]
            keys.sort()
            self._motorNames = [motorsMne[str(i)] for i in keys]
        return self._motorNames

    def getNumCounters(self):
        if self.connection is not None:
            return self.connection.getChannel('var/COUNTERS').read()

    def getNumMotors(self):
        if self.connection is not None:
            return self.connection.getChannel('var/MOTORS').read()

    def runMacro(self, macro):
        self(getSpecMacro(macro), asynchronous=False)

    def getVarVal(self, var):
        if self.connection is not None:
            return self.connection.getChannel('var/%s'%var).read()

    def abort(self):
        self.connection.abort()


class TestSpecRunner(SpecRunnerBase):

    def __init__(self, specVersion='', timeout=None, **kwargs):
        self.motordict = {'1':TestQtSpecMotor('1'), '2':TestQtSpecMotor('2'),\
                          '3':TestQtSpecMotor('3'), '4':TestQtSpecMotor('4'),\
                          '5':TestQtSpecMotor('5')}

        self.specVersion = 'thiscomp:nospec'

    def __call__(self, command):
        logger.debug( "executing %s",command)
        strings=QtCore.QString(command).split(' ')
        if str(strings[0]) in ('mvr','umvr','mmvr'):
            motorA = self.motordict[str(strings[1])]
            motorB = self.motordict[str(strings[-2])]
            APosition = motorA.getPosition()
            BPosition = motorB.getPosition()
            motorA.move(float(strings[2])+APosition)
            motorB.move(float(strings[-1])+BPosition)
        elif str(strings[0]) in ('mv','umv','mmv'):
            motorA = self.motordict[str(strings[1])]
            motorB = self.motordict[str(strings[-2])]
            motorA.move(float(strings[2]))
            motorB.move(float(strings[-1]))
        print command

    def abort(self):
        for motor in self.motordict.values():
            motor.end()
        print "ABORT"

    def getMotorsMne(self):
        motors = self.motordict.keys()
        motors.sort()
        return  motors

    def getCountersMne(self):
        pass

    def close(self):
        pass


    def getMotor(self, name):
        return self.motordict[name]

    def getMotorMne(self, motorId):
        return self.motorDict(motorId).specname

    def getNumCounters(self):
        pass

    def getNumMotors(self):
        pass

    def runMacro(self, macro):
        self.__call__(getSpecMacro(macro))

    def getVarVal(self, var):
        return 1



if TEST_SPEC:
    class SpecRunner(TestSpecRunner):
        pass
else:
    class SpecRunner(SpecRunnerBase):
        pass

