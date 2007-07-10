DEBUG=None
Roll=None

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


"""
This section is what actualy interacts with the motors
"""



class SpecRunner:
    """Connects to a Spec host server and manipulates its motors
    
    TODO: fill this with info
    
    """


    def __init__(self,Debug=0,parent=None):
        """input a debug roll and parrent if needed by default all are 0 or None
        Debug--set to 1 it deactivates spec commands
        roll --set to 1 it auto starts spec -s on roll.chess.cornell.edu and connects,
             --set to 2 it wont autostart but will autoconnect
        Parent -- used to establish stdout.
         
        """
        self.DEBUG=Debug
        self._paramnames = () 
        self._spec = None
        self._specPort=''
        self._specHost=''
        self._var_strings=[]
        self._var=[]
        self._cmd_string=''
        self._motors={}
        self.parameters={}
        self._motor=None
        if parent:
            sys.stdout=parent
        print "spec is on"
    
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
            if self.DEBUG==1:
                self._spec=("motor0","motor1","motor2")
                self._paramnames=("variable1","number 2","Shalosh")  
            else:
                self._spec = Spec.Spec(self._specHost + ":" + self._specPort, 500)
            print "Connected!"
            return True
        except:
            return False
    
    def readmotors(self):
        if self.DEBUG==1:
            motornames=("motor0","motor1","motor2")
            for i in range(len(motornames)):
                self._motors[motornames[i]]=motornames[i]
        else:
            motornames=self._spec.getMotorsMne()
            for name in motornames:
                self._motors[name] = TestSpecMotor(name,
                                                   self._specHost + ":" + self._specPort)
                
    def readParam(self,motor):
        motor=self._motors[motor]
        if self.DEBUG!=1:    
            self._paramnames=('position','offset','sign',"low_limit","high_limit")
        else:
            self._paramnames=("one","two","three")
            return self._paramnames
        value=[]
        for i in range(len(self._paramnames)):
            try: 
                value.append(motor.get_parameter(self._paramnames[i]))
            except:
                value.append("unable to get value")
            self.parameters[motor]=value
        
    def get_motor_names(self): 
        return self._motors.keys()
    
    def get_param(self):
        return self._paramnames
    
    def get_params_values(self,motor):
        motor=self._motors[motor]
        return self.parameters[motor]
    
    def get_param_val(self):
        n=self._paramnames.index(self._var)
        return self.parameters[self._motor][n]
    
    def set_motor(self,motor_name):
        if motor_name in self._motors:
            self._motor=self._motors[motor_name]
    
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
    
    def set_var(self,var):
        self._var.append(TestSpecVariable(var, self._specHost+":"+self._specPort))
        self._var_strings.append(var)
    def get_var(self):
        return self._var_strings
    
    def set_cmd(self,cmd):
        self._cmd_string=cmd
        self._cmd_list = [str(i) for i in self._cmd_string.split(' ')]
        self._cmd=TestSpecCommand(self._cmd_list[0], self._specHost+":"+self._specPort)
    
    def get_cmd(self):
        return self._cmd_string
    
    def get_cmd_reply(self):
        return self._cmd.get_Reply()
    
    def run_cmd(self):
        self._cmd(*self._cmd_list[1:])
    
    def update(self):
        if self._motor.isConnected() and self._var[0].isConnected():
            SpecEventsDispatcher.dispatch()
        #for var in self._var:
           # print  "%s is %s"%(var.getVarName(),var.getValue())
        
    
    def EmergencyStop(self):
        if self.get_cmd():
            #self.set_cmd("stop() ")
            #self.run_cmd()
            self.set_cmd('')
            print "\n %%%%%%%%%%%%ALL STOP%%%%%%%%%%%%"

    def tester(self):
        print "testing"


if __name__ =="__main__":
    NewSpecRun=SpecRunner(1)
