"""
"""

from __future__ import absolute_import

import logging
import os
import sys
import time

from PyQt4 import QtCore
import SpecClient
from SpecClient import Spec, SpecEventsDispatcher, SpecCommand, SpecVariable

from .motor import QtSpecMotorA
from .scan import QtSpecScanA
from . import TEST_SPEC


logger = logging.getLogger(__file__)


def getSpecMacro(filename, package=None):
    if package is not None:
        package = __file__
    temp = os.path.split(__file__)[0]
    try:
        return open(os.path.join(temp, filename)).read()
    except IOError:
        return open(os.path.join(temp, 'macros', filename)).read()


class Dispatcher(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

    def run(self):
        self.exec_()

    def update(self):
        SpecEventsDispatcher.dispatch()


class SpecDatafile(SpecVariable.SpecVariableA, QtCore.QObject):

    datafileChanged = QtCore.pyqtSignal(str)

    def __init__(self, varName=None, specVersion=None, specRunner=None):
        QtCore.QObject.__init__(self, specRunner)
        SpecVariable.SpecVariableA.__init__(self, varName, specVersion)

        self._specRunner = specRunner

    def setValue(self, fileName):
        self._specRunner('newfile %s'%fileName, asynchronous=False)
        specfile = self.getValue()

        specCreated = os.path.split(specfile)[-1]
        if fileName == specCreated:
            logger.debug("file %s created",fileName)
        else:
            logger.error('%s given %s returned',(fileName,specfile))
            self.fileError(fileName, specfile)

    def update(self, value):
        if not value == '/dev/null':
            self.datafileChanged.emit(value)


class SpecRunnerBase(Spec.Spec, QtCore.QObject):

    """
    SpecRunner is our primary interface to Spec. Some caching is added,
    to improve performance.
    """

    specBusy = QtCore.pyqtSignal(bool)

    @property
    def busy(self):
        return self.status == 'busy'

    @property
    def ready(self):
        return self.status == 'ready'

    @property
    def specVersion(self):
        return self.__specVersion

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status):
        status = status.lower()
        assert status in ('aborting', 'busy', 'cleanup', 'ready')
        self.__status = status
        self.specBusy.emit(status != 'ready')

    def __init__(self, specVersion=None, timeout=None, parent=None):
        """specVersion is a string like 'foo.bar:spec' or '127.0.0.1:fourc'
        """
        print 1
        QtCore.QObject.__init__(self, parent)
        print 2
        Spec.Spec.__init__(self, specVersion, timeout)
        print 3
        self.__specVersion = specVersion
        self.__status = 'ready'
        print 4
        self.connection.registerChannel(
            'status/ready',
            self.__statusReady,
            dispatchMode=SpecEventsDispatcher.FIREEVENT
        )

        self._datafile = SpecDatafile('DATAFILE', specVersion, self)

        self._motors = {}
        self._motorNames = []
        self._counterNames = []
        self.getMotorsMne()
        self.getCountersMne()

        print 1
        self(getSpecMacro('clientutils.mac', SpecClient), asynchronous=False)
        self("client_data 1", asynchronous=False)
        print 2

        self.runMacro('skipmode.mac')

#        self.dispatcher = Dispatcher(self)
#        self.dispatcher.start(QtCore.QThread.NormalPriority)
#########
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

    def __statusReady(self, status):
        if status:
            if self.status == 'aborting':
                self.status = 'cleanup'
            else:
                self.status = 'ready'
        else:
            if self.ready:
                self.status = 'busy'

    def update(self):
        SpecEventsDispatcher.dispatch()
#########

    @property
    def datafile(self):
        return self._datafile

    def __call__(self, command, asynchronous=True):
#        logger.debug("executing %s",command)
        if asynchronous:
            cmd = SpecCommand.SpecCommandA(command, self.specVersion)
        else:
            cmd = SpecCommand.SpecCommand(command, self.specVersion, None)

        return cmd()

    def close(self):
        try:
            self("client_data 0", asynchronous=False)
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
        if self.busy:
            self.connection.abort()
            self.status = 'aborting'


class TestSpecRunner(SpecRunnerBase):

    def __init__(self, specVersion='', timeout=None, **kwargs):
        self.motordict = {'1':TestQtSpecMotor('1'), '2':TestQtSpecMotor('2'),\
                          '3':TestQtSpecMotor('3'), '4':TestQtSpecMotor('4'),\
                          '5':TestQtSpecMotor('5')}

        self.specVersion = 'thiscomp:nospec'

    def __call__(self, command):
#        logger.debug( "executing %s",command)
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

    def getCountersMne(self):
        pass

    def close(self):
        pass


    def getMotor(self, name):
        return self.motordict[name]

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

