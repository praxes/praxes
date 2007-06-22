DEBUG=None
Roll=None

import sys
#SpecClient
import SpecClient

SpecClient.setLoggingOff()
from SpecClient import SpecMotor, Spec, SpecEventsDispatcher, SpecVariable, SpecCommand

"""
    Section for actual Motor Control Mockup
    These are the things set up by Danny
***********ACTUAL MOTOR CONTROLS FOLLOW**********

"""


class TestSpecMotor(SpecMotor.SpecMotorA):
    stateStrings = ['NOTINITIALIZED', 'UNUSABLE', 'READY', 'MOVESTARTED', 'MOVING', 'ONLIMIT']
    def connected(self):
        self.__connected__ = True
        print'Motor %s connected'%self.specName
    def disconnected(self):
        self.__connected__ = False
        print 'Motor %s disconnected'%self.specName
    def motorLimitsChanged(self):
        limits = self.getLimits()
        limitString = "(" + str(limits[0])+", "+ str(limits[1]) + ")"
        print "Motor %s limits changed to %s"%(self.specName,limitString)
    def motorPositionChanged(self, absolutePosition):
        print "Motor %s position changed to %s"%(self.specName,absolutePosition)
    def syncQuestionAnswer(self, specSteps, controllerSteps):
        print "Motor %s syncing"%self.specName
    def motorStateChanged(self, state):
        print "Motor %s state changed to"%self.specName
        print self.stateStrings[state]
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)
    def status(self):
        return self.stateStrings[self.getState()]
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
        print "Variable %s updated to %s"%(self.getVarName(),value)
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)
    def getVarName(self):
        return self.channelName[4:len(self.channelName)]

class TestSpecCommand(SpecCommand.SpecCommandA):
    def beingWait(self):
        print 'Command %s was sent'%self.command
    def replyArrived(self, reply):
        if (reply.error):
            print "command %s received an error message: "%(self.command,reply.data)
        else:
            print "Command %s received a reply: %s"%(self.command,reply.data)


"""
This section is what actualy interacts with the motors
"""



class SpecRunner:
    """Connects to a Spec host server and manipulates its motors
    
    TODO: fill this with info
    
    """


    def __init__(self,Debug=0,roll=0,parent=None):
        """input a debug roll and parrent if needed by default all are 0 or None
        Debug--set to 1 it deactivates spec commands
        roll --set to 1 it auto starts spec -s on roll.chess.cornell.edu and connects,
             --set to 2 it wont autostart but will autoconnect
        Parent -- used to establish stdout.
         
        """
        self.DEBUG=Debug
        self.Roll=roll
        self._varnames = () # TODO: finish these commands
        self._spec = None
        self._specPort=''
        self._specHost=''
        self._var=''
        self._cmd=''
        self._motors={}
        self._variables={}
        self._motor=None
        if parent:
            sys.stdout=parent
        print "spec is on"
    def setspechost(self,spechost):
        self._specHost=spechost
    def getspechost(self):
        return self._specHost
    def setspecport(self,port):
        self._specPort=port
    def getspecport(self):
        return self._specPort
    def serverconnect(self):
        print "connecting..."
        try:
            if self.DEBUG==1:
                self._spec=("motor0","motor1","motor2")
                self._varnames=("variable1","number 2","Shalosh")  
            else:
                if self.Roll==1 or self.Roll==2:
                    self._specHost="roll.chess.cornell.edu"
                    self._specPort="spec"
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
            motors=[]
            for i in range(len(motornames)):
                motors.append(TestSpecMotor(self._spec.motor_name(i),\
                                                   self._specHost + ":" + self._specPort))
                self._motors[motornames[i]]=motors[i]
                
    def readvariables(self,motor):
        motor=self._motors[motor]
        if self.DEBUG!=1:    
            self._varnames=('position','sync_check','unusable','offset','sign')
        else:
            self._varnames=("one","two","three")
            return self._varnames
        value=[]
        for i in range(len(self._varnames)):
            try: 
                value.append(motor.getParameter(self._varnames[i]))
            except:
                value.append("unable to get value")
            self._variables[motor]=value
        
    def getmotors(self): 
        return self._motors.keys()
    def getvars(self,motor):
        return self._varnames
    def getvarsvalues(self,motor):
        return self._variables[motor]
    def setmotor(self,motor):
        if motor in self._motors.keys():
            self._motor=self._motors[motor]
    def getmotor(self):
        return self._motor.motor_name()
    def getmotorlimits(self,nameOfMotor):
        return self._motors[nameOfMotor].getLimits()
    def getmotorposition(self, nameOfMotor):
        return self._motors[nameOfMotor].getPosition()
    def status(self,nameOfMotor):
        return self._motors[nameOfMotor].status()
    def setvar(self,motor,var):
        motor=self._motors[motor]
        if var in self._variables[motor]:
            self._var=var
        else:
            return False
    def getvar(self):
        return self._var
    def setcmd(self,cmd):
        self.cmd=cmd
    def getcmd(self,cmd):
        return self.cmd           
    def runcmd(self):
        self._cmd=self._cmd.split(' ')
        if self.DEBUG==1 or self.DEBUG==2:
            for i in range(len(self._cmd)):
                print "\n**It will %s**"%self._cmd[i]
        else:
            print "working"
            #TODO understand and moridy this code
            motorMon = TestSpecMotor(self._motor, self._specHost+":"+self._specPort)
            variableMon = TestSpecVariable(self._var, self._specHost+":"+self._specPort)
            commandMon = TestSpecCommand(self._cmd[0], self._specHost+":"+self._specPort)
            commandMon(self._cmd[1])
            while motorMon.isConnected() and variableMon.isConnected():
                SpecEventsDispatcher.dispatch()
    
    def EmergencyStop(self):
        if self.getCmd():
            self.setCmd("stop()")
            self.runCMD()
            self.cmd=''
            print "\n %%%%%%%%%%%%ALL STOP%%%%%%%%%%%%"

    def tester(self):
        print "testing"
        
        
        
        
if __name__ =="__main__":
    NewSpecRun=SpecRunner(1)
