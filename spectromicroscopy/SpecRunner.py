DEBUG=None


import sys
import SpecClient
SpecClient.setLoggingOff()
from SpecClient import SpecMotor, Spec, SpecEventsDispatcher, SpecVariable, SpecCommand

"""
    Section for actual Motor Control Mockup
    These are the things set up by Danny
***********ACTUAL MOTOR CONTROLS FOLLOW**********

Motor Names refer to motor nemonics
specclient expects to wrok with nemonics and never used full motor names

"""
from PyQt4 import QtCore

class TestSpecMotor(SpecMotor.SpecMotorA):
    
    __state_strings__ = ['NOTINITIALIZED', 'UNUSABLE', 'READY', 'MOVESTARTED', 'MOVING', 'ONLIMIT']
    
    def __init__(self, specName = None, specVersion = None):
        SpecMotor.SpecMotorA.__init__(self, specName, specVersion)
        self.getPosition()

    def connected(self):
        self.__connected__ = True
        print'Motor %s connected'%self.specName
    
    def disconnected(self):
        self.__connected__ = False
        print 'Motor %s disconnected'%self.specName

    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)

    def motorLimitsChanged(self):
        limits = self.getLimits()
        limitString = "(" + str(limits[0])+", "+ str(limits[1]) + ")"
        print "Motor %s limits changed to %s"%(self.specName,limitString)
    
    def motorPositionChanged(self, absolutePosition):
        print "Motor %s position changed to %s"%(self.specName,absolutePosition)
    
    def syncQuestionAnswer(self, specSteps, controllerSteps):
        print "Motor %s syncing"%self.specName
    
    def motorStateChanged(self, state):
        print "Motor %s state changed to %s"%(self.specName, self.__state_strings__[state])
    
    def status(self):
        return self.__state_strings__[self.getState()]
    
    def motor_name(self):
        return self.specName



class TestSpecVariable(SpecVariable.SpecVariableA):
    
    def connected(self):
        self.__connected__ = True
        print 'Variable %s connected'%self.getVarName()
    
    def disconnected(self):
        self.__connected__ = False
        print "Variable %s disconnected"%self.getVarName()
    
    def update(self, value):
        print "Variable %s updated to %s"%(self.getVarName(), value)
    
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)
    
    def getVarName(self):
        return self.channelName[4:len(self.channelName)]




class TestSpecCommand(SpecCommand.SpecCommandA):

    def beingWait(self):
        print 'Command %s was sent'%self.command
    
    def replyArrived(self, reply):
        self.Reply=reply
        if (reply.error):
            print "command %s received an error message: %s"%(self.command, reply.data)
        else:
            print "Command %s received a reply: %s"%(self.command, reply.data)
    
    def connected(self):
       print "Command connected"
       self.Reply=None 
    
    def disconnected(self):
        print "disconnected"
                
    def statusChanged(self, ready):
        state=["In progress","Complete","Unknown"]
        print "Status is %s"%state[ready]
    
    def get_Reply(self):
        return self.Reply




class Indexer(TestSpecVariable):
    
    def connected(self):
        self.__connected__ = True
    
    def disconnected(self):
        self.__connected__ = False
    
    def update(self, value):
        pass


    
"""
This section is what actualy interacts with the motorsand GUI
"""





class SpecRunner:
    """Connects to a Spec host server and manipulates its motors
    
    TODO: fill this with info
    
    """
    
    def __init__(self,parent=None,Debug=0,spechost='',specport='',motor_names=[]):
        """input a debug roll and parrent if needed by default all are 0 or None
        Debug--set to 1 it deactivates spec commands
        roll --set to 1 it auto starts spec -s on roll.chess.cornell.edu and connects,
             --set to 2 it wont autostart but will autoconnect
        Parent -- used to establish stdout.
         
        """
        DEBUG=Debug
        self._param_names = () 
        self._spec = None
        self._specPort=specport
        self._specHost=spechost
        self._var_strings=[]
        self._var=[]
        self._cmd_string=''
        self._motors={}
        self._exc=''
        self._parameters={}
        self._param_names=['position','offset','sign',"low_limit","high_limit"]
        self._motor=None
        if self._specHost and self._specPort:
            self.serverconnect()
    
        
    
    def set_spec_host(self,spechost):
        self._specHost=spechost
    
    def get_spec_host(self):
        return self._specHost
    
    def set_spec_port(self,port):
        self._specPort=port
    
    def get_spec_port(self):
        return self._specPort
    
    def serverconnect(self):
        print "Connecting..."
        try:
            self._spec = Spec.Spec(self._specHost + ":" + self._specPort, 500)
            self._exc=SpecCommand.SpecCommandA('', self._specHost+":"+self._specPort)
            print "Connected!"
            MonDef="def MonitorLoop 'IndexVar+=1'"
            SetDef="def SetMon 'global IndexVar \n IndexVar = -1'"
            testdef ="def testscript '\nSetMon\nlocal i\ni=0 \nfor (;i<20;) {\n\
            i+=1\n        p S[3]+=1 \n        p MonitorLoop}'"
            A='cdef("user_scan_loop", "MonitorLoop;","zru",0x01)'
            C='cdef("_cleanup2","SetMon;","zru",0x01)'
            self.exc(MonDef)
            self.exc(SetDef)
            self.exc(testdef)
            self.exc('SetMon')
            self.exc(A)
            self.exc(C)
            try:
                self._index=Indexer("IndexVar",self._specHost+":"+self._specPort)
                self._last_index=self._index.getValue()
            except:
                print "IndexVar Failed to Connect"
            return True
        except:
            return False
    
    
    def exc(self,command_string):
        if self._exc:
            self._exc.executeCommand(command_string)
    
    
    def readmotors(self,names=[]):
        if names:
            motornames=names
        else:
            motornames=self._spec.getMotorsMne()
        for name in motornames:
            self._motors[name] = TestSpecMotor(name,
                                               self._specHost + ":" + self._specPort)
    
    def readParam(self,motor):
        motor=self._motors[motor]
        value=[]
        for param in self._param_names:
            try: 
                value.append(motor.getParameter(param))
            except:
                value.append("unable to get value")
            self._parameters[motor]=value
        return self._parameters[motor]
    
    def get_motor_names(self): 
        return self._motors.keys()
    
    def set_motor(self,motor_name):
        if motor_name in self._motors:
            self._motor=self._motors[motor_name]
    
    def get_motor(self,motor_name):
        if motor_name in self._motors:
            return self._motors[motor_name]

    def get_motor_name(self):
        if self._motor:
            return self._motor.motor_name()
        else:
            return None
    
    def get_motor_limits(self,motor_name):
        return self._motors[motor_name].getLimits()
    
    def get_motor_position(self, motor_name):
        return self._motors[motor_name].getPosition()
    
    def status(self,motor_name):
        return self._motors[motor_name].status()
    
    def get_params_names(self):
        return self._param_names
    
    def get_params_values(self,motor):
        motor=self._motors[motor]
        return self._parameters[motor]
    
    def set_var(self,var):
        self._var.append(TestSpecVariable(var, self._specHost+":"+self._specPort))
        self._var_strings.append(var)
    
    def get_var(self):
        return self._var_strings
    
    def reset_var(self):
        self._var=[]
        self._var_strings=[]
        print "Select a New Variable"
    
    def set_cmd(self,cmd):
        self._cmd_string=cmd
        self._cmd_list = [str(i) for i in self._cmd_string.split(' ')]
        self._cmd=TestSpecCommand(self._cmd_list[0], self._specHost+":"+self._specPort)
    
    def get_cmd(self):
        return self._cmd_string
    
    def get_cmd_reply(self):
        if self._cmd:
            return self._cmd.get_Reply()
        else:
            return ''
    
    def run_cmd(self):
        self._cmd(*self._cmd_list[1:])
    
    def update(self):
        if self._var[0].isConnected():
            SpecEventsDispatcher.dispatch()
    
    def get_values(self):
        values=[]
        prev = self._last_index
        curr = self._index.getValue()
        if curr != prev:
            if curr > prev+1:
                print "missed data point!"
                return "missed data point!"
            for var in self._var:
                values.append(var.getValue())
                self._last_index=curr
                print "*****************Got Point************"
                return (values,curr)
        else:
            return ([''],curr)


    def EmergencyStop(self):
        if self.get_cmd():
            self._cmd.abort()
            self.set_cmd('')
            print "\n %%%%%%%%%%%%ALL STOP%%%%%%%%%%%%"



    def tester(self):
        print "testing"
    


if __name__ =="__main__":
    NewSpecRun=SpecRunner(1)
