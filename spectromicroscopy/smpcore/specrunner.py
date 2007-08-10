"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

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


class SpecRunner:
    """Connects to a Spec host server and manipulates its motors
    
    TODO: fill this with info
    
    """
    
    _motorNames = []
    
    def __init__(self, parent=None, Debug=0, spechost='', specport='',
                 motor_names=[]):
        """input a debug roll and parrent if needed by default all are 0 or None
        Debug--set to 1 it deactivates spec commands
        roll --set to 1 it auto starts spec -s on roll.chess.cornell.edu and 
                    connects,
             --set to 2 it wont autostart but will autoconnect.
         
        """
        DEBUG=Debug
        self._param_names = ()
        self._spec = None
        self._specPort = specport
        self._specHost = spechost
        self._var_strings = []
        self._var = []
        self._cmd_string = ''
        self._motors = {}
        self._exc = ''
        self._parameters = {}
        self._type_dict = {}
        self._param_names = ['position',
                             'offset',
                             'sign',
                             'low_limit',
                             'high_limit']
        self._motor = None
        if self._specHost and self._specPort:
            self.serverconnect()

    def set_spec_host(self, spechost):
        self._specHost = spechost
    
    def get_spec_host(self):
        return self._specHost
    
    def set_spec_port(self,port):
        self._specPort = port
    
    def get_spec_port(self):
        return self._specPort
    
    def serverconnect(self):
        try:
            self._spec = Spec.Spec(self._specHost + ":" + self._specPort, 500)
            self._exc = SpecCommand.SpecCommandA('',
                                self._specHost+":"+self._specPort)
            
            try:
                self._S = XrfSpecVar("S", self._specHost+":"+self._specPort)
                self._Detector = XrfSpecVar("MCA_NAME",
                                            self._specHost+":"+self._specPort)
                self.mca_data = XrfSpecVar("MCA_DATA", 
                                           self._specHost+":"+self._specPort,
                                           500)
                return True
            except:
                print "Variables Failed to Connect"
        except:
            print "Failed to Connect"
            return False

    def exc(self, command_string):
        if self._exc:
            self._exc.executeCommand(command_string)

    def readMotors(self, *args):
        if len(args) == 0:
            args = self.getMotorNames()
        for arg in args:
            self._motors[arg] = QtSpecMotorA(arg,
                                             self._specHost + \
                                             ":" + self._specPort)
            # TODO: Is this necessary?
            self._type_dict[arg] = 'Async'
        
    def readParam(self,motor):
        motor = self._motors[motor]
        value = []
        for param in self._param_names:
            try: 
                value.append(motor.getParameter(param))
            except:
                value.append("unable to get value")
            self._parameters[motor] = value
        return self._parameters[motor]
    
    def getMotorNames(self):
        if len(self._motorNames) == 0:
            self._motorNames = self._spec.getMotorsMne()
            self._motorNames.sort()
        return self._motorNames
    
    def set_motor(self, motor_name):
        if motor_name in self._motors:
            self._motor = self._motors[motor_name]
    
    def get_motor(self, motor_name):
        if motor_name in self._motors:
            return self._motors[motor_name]
        else:
            self.readMotors(motor_name)
            return self._motors[motor_name]

    def get_motor_name(self):
        if self._motor:
            return self._motor.motor_name()
        else:
            return None
    
    def get_motor_limits(self, motor_name):
        return self._motors[motor_name].getLimits()
    
    def get_motor_position(self, motor_name):
        return self._motors[motor_name].getPosition()
    
    def status(self, motor_name):
        return self._motors[motor_name].status()
    
    def get_params_names(self):
        return self._param_names
    
    def get_params_values(self,motor):
        motor = self._motors[motor]
        return self._parameters[motor]
    
    def get_var(self):
        return self._var_strings
    
    def reset_var(self):
        self._var = []
        self._var_strings = []
        print "Select a New Variable"
    
    def set_cmd(self, cmd, type="Test"):
        self._cmd_string = cmd
        self._cmd_list = [str(i) for i in self._cmd_string.split(' ')]
        if type == "Test":
            self._cmd = TestSpecCommand(self._cmd_list[0],
                                        self._specHost+":"+self._specPort)
        if type == "Sync":
            self._cmd = SpecCommand.SpecCommand(self._cmd_list[0],
                                                self._specHost+":"+\
                                                    self._specPort,
                                                500)
        if type == "Async":
            self._cmd = SpecCommand.SpecCommandA(self._cmd_list[0],
                                                 self._specHost+":"+\
                                                    self._specPort)
        self._type_dict[cmd] = type
    
    def get_cmd(self):
        return self._cmd_string
    
    def get_cmd_reply(self):
        if self._cmd:
            return self._cmd.get_Reply()
        else:
            return ''
    
    def run_cmd(self):
#        print 'running command: %s'% ' '.join(self._cmd_list)
        self._cmd(*self._cmd_list[1:])
        self._last_index = -1
    
    def update(self):
        SpecEventsDispatcher.dispatch()
    
    def get_values(self):
        values = []
        prev = self._last_index
        curr = self._index.getValue()
        if curr != prev:
            if curr > prev+1:
                print "missed point %s v %s"%(prev,curr)
                self._last_index = curr
                return ([''],curr,'')
            else:
                if self._Detector.getValue() == "vortex":
                    a = self.compensate()
                    print 'dead time correction: %.3f'% a
                else:
                    a = 1.0
#                time.sleep(TIMEOUT)
                counts = self.mca_data.getValue()
                values.append(a*counts)
                self._last_index = curr
#                    print "*****************Got Point***************"
                if 1 <= a:
                    return (values, curr, True)
                else:
                    return (values, curr, False)
        else:
            return ([''], curr, '')

    def compensate(self):
        S = self._S.getValue()
        icr = float(S["5"])
        ocr = float(S["7"])
        real = float(S["8"])
        live = float(S["9"])
        return icr/ocr*real/live

    def abort(self):
        # TODO: This needs to be robust!
        if self.get_cmd():
            self._cmd.abort()
            self.set_cmd('')
            print "\n %%%%%%%%%%%%ALL STOP%%%%%%%%%%%%"


if __name__ == "__main__":
    print "dont start as main"
