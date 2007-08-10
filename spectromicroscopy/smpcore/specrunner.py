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



#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

import configutils
from spectromicroscopy.external import SpecClient
logfile = os.path.join(configutils.getUserConfigDir(), 'specclient.log')
SpecClient.setLogFile(logfile)
from spectromicroscopy.external.SpecClient import Spec, SpecEventsDispatcher
from qtspecmotor import QtSpecMotorA

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG=False # ??
TIMEOUT=.02


class SpecRunner(Spec.Spec):
    """SpecRunner is our primary interface to Spec
    """
    
    _motorNames = []
    
    def __init__(self, specVersion=None, timeout=None):
        """specVersion is a string like 'foo.bar:spec' or '127.0.0.1:fourc'
        """
        self._motors = {}
        Spec.Spec.__init__(self, specVersion, timeout)

    def getMotor(self, motorName):
        if motorName in self._motors:
            return self._motors[motorName]
        else:
            self._motors[motorName] = QtSpecMotorA(motorName, self.specVersion)
            return self._motors[motorName]

    def update(self):
        SpecEventsDispatcher.dispatch()
