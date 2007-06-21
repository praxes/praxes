import SpecClient

SpecClient.setLoggingOff()

from SpecClient import SpecMotor, Spec, SpecEventsDispatcher, SpecVariable, SpecCommand


stateStrings = ['NOTINITIALIZED', 'UNUSABLE', 'READY', 'MOVESTARTED', 'MOVING', 'ONLIMIT']
# TODO: replace print in Classes with special output to text veiwer

class TestSpecMotor(SpecMotor.SpecMotorA):
    def connected(self):
        self.__connected__ = True
        print 'Motor ', self.specName, ' connected'
    def disconnected(self):
        self.__connected__ = False
        print 'Motor ', self.specName, ' disconnected'
    def motorLimitsChanged(self):
        limits = self.getLimits()
        limitString = "(" + str(limits[0])+", "+ str(limits[1]) + ")"
        print 'Motor ', self.specName, ' limits changed to ', limitString
    def motorPositionChanged(self, absolutePosition):
        print 'Motor ', self.specName, ' position changed to ' , absolutePosition
    def syncQuestionAnswer(self, specSteps, controllerSteps):
        print 'Motor ', self.specName, ' syncing'
    def motorStateChanged(self, state):
        print 'Motor ', self.specName, ' state changed to ' , stateStrings[state]
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)

class TestSpecVariable(SpecVariable.SpecVariableA):
    def connected(self):
        self.__connected__ = True
        print 'Variable ', self.getVarName(), ' connected'
    def disconnected(self):
        self.__connected__ = False
        print 'Variable ', self.getVarName(), ' disconnected'
    def update(self, value):
        print 'Variable ', self.getVarName(), ' updated to ', value
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)
    def getVarName(self):
        return self.channelName[4:len(self.channelName)]

class TestSpecCommand(SpecCommand.SpecCommandA):
    def beingWait(self):
        print 'Command ', self.command, ' was sent'
    def replyArrived(self, reply):
        if (reply.error):
            print 'Command ', self.command, ' received an error: ', reply.data
        else:
            print 'Command ', self.command, ' received a reply: ', reply.data



# TODO: replace raw_input() with input from textbar
# TODO: replace print with output into textviewer
spec = None
while spec == None:
    specHost = raw_input('Enter spec server hostname: ')
    specPort = raw_input('Enter spec server port: ')

    try:
        spec = Spec.Spec(specHost + ":" + specPort, 500)
    except:
        print 'Invalid host or port'

print 'Reading motors: '
motors = spec.getMotorsMne()        #gets the motors methods and puts into list
motornames = []

print 'Reading motor names: ',
for i in range(len(motors)):
    print '.',
    motornames.append(spec.motor_name(i))
print

print 'Valid motors on '+specHost+' are:'
for i in range(len(motors)):
    print "   "+motors[i]+" ("+motornames[i]+")"

sel = None;
while sel == None:
    trysel = raw_input('Select a motor to monitor: ')
    if (motors.count(trysel) > 0):
        sel = trysel
        selnum = motors.index(sel)
    else:
        print 'Invalid motor selection'

var = raw_input('Select a variable to monitor: ')
cmd = raw_input('Enter a command to run asynchronously: ').split(' ',1)

motorMon = TestSpecMotor(sel, specHost+":"+specPort)
variableMon = TestSpecVariable(var, specHost+":"+specPort)
commandMon = TestSpecCommand(cmd[0], specHost+":"+specPort)

commandMon(cmd[1])

while motorMon.isConnected() and variableMon.isConnected():
    SpecEventsDispatcher.dispatch()


     
