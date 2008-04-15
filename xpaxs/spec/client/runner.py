"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore
import SpecClient
from SpecClient import Spec, SpecEventsDispatcher, SpecCommand

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import configutils
from xpaxs.spec.client.motor import QtSpecMotorA
from xpaxs.spec.client.scan import QtSpecScanA

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = True

logfile = os.path.join(configutils.getUserConfigDir(), 'specclient.log')

SpecClient.setLogFile(logfile)

def getSpecMacro(filename):
    temp = os.path.split(os.path.split(__file__)[0])[0]
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


class SpecRunner(Spec.Spec, QtCore.QObject):
    """SpecRunner is our primary interface to Spec. Some caching is added,
    to improve performance.
    """

    def __init__(self, specVersion=None, timeout=None, **kwargs):
        """specVersion is a string like 'foo.bar:spec' or '127.0.0.1:fourc'
        """
        QtCore.QObject.__init__(self)
        Spec.Spec.__init__(self, specVersion, timeout)
        self.cmd = SpecCommand.SpecCommand('', specVersion, None)

        self._motors = {}
        self._motorNames = []
        self._counterNames = []
        self.getMotorsMne()
        self.getCountersMne()

        self.dispatcher = Dispatcher()
        self.dispatcher.start(QtCore.QThread.NormalPriority)

    def __call__(self, command):
        if DEBUG: print "SpecRunner(%s)"%command
        self.cmd.executeCommand(command)

    def close(self):
        try:
            self.dispatcher.exit()
            self.dispatcher.wait()
            self.connection.dispatcher.disconnect()
        except:
            pass

    def getCountersMne(self):
        if len(self._counterNames) != self.getNumCounters():
            countersMne = self.cmd.executeCommand("local md; for (i=0; "
                        "i<COUNTERS; i++) { md[i]=cnt_mne(i); }; return md")
            keys = [int(i) for i in countersMne.keys()]
            keys.sort()
            self._counterNames = [countersMne[str(i)] for i in keys]
        return self._counterNames

    def getMotor(self, motorName):
        return QtSpecMotorA(motorName, self.specVersion)

    def getMotorMne(self, motorId):
        motorMne = self.motor_mne(motorId, function = True)
        if not motorMne in self._motorNames:
            self._motorNames.append(motorMne)
        return motorMne

    def getMotorsMne(self):
        if len(self._motorNames) != self.getNumMotors():
            motorsMne = self.cmd.executeCommand("local md; for (i=0; i<MOTORS;"
                                                "i++) { md[i]=motor_mne(i); };"
                                                "return md")
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
        self.cmd.executeCommand(getSpecMacro(macro))

    def getVarVal(self, var):
        if self.connection is not None:
            return self.connection.getChannel('var/%s'%var).read()

    def abort(self):
        self.connection.abort()
