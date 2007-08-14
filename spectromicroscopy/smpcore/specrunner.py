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

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpcore import configutils
import SpecClient
logfile = os.path.join(configutils.getUserConfigDir(), 'specclient.log')
SpecClient.setLogFile(logfile)
from SpecClient import Spec, SpecEventsDispatcher, SpecCommand
from spectromicroscopy.smpcore import qtspecmotor

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class SpecRunner(Spec.Spec, QtCore.QObject):
    """SpecRunner is our primary interface to Spec. Some caching is added,
    to improve performance.
    """
    
    def __init__(self, specVersion=None, timeout=None):
        """specVersion is a string like 'foo.bar:spec' or '127.0.0.1:fourc'
        """
        QtCore.QObject.__init__(self)
        Spec.Spec.__init__(self, specVersion, timeout)
        
        # load the clientutils macros:
        clientutils = SpecCommand.SpecCommand('', specVersion, timeout)
        clientutils.executeCommand(configutils.getClientUtilsMacro())
        self.clientploton()
        
        self._motors = {}
        self._motorNames = []
        
        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.update)
        self.timer.start(20)

    def __del__(self):
        self.clientplotoff()
        QtCore.QObject.__del__(self)
        Spec.Spec.__del__(self)

    def getMotor(self, motorName):
        if motorName in self._motors:
            return self._motors[motorName]
        else:
            self._motors[motorName] = qtspecmotor.QtSpecMotorA(motorName,
                                                               self.specVersion)
            return self._motors[motorName]

    def getMotorsMne(self):
        if not self._motorNames:
            self._motorNames = Spec.Spec.getMotorsMne(self)
            self._motorNames.sort()
        return self._motorNames

    def update(self):
        SpecEventsDispatcher.dispatch()

    def abort(self):
        self.connection.abort()
