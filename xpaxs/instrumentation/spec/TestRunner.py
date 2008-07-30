from PyQt4 import QtCore
from TestMotor import TestQtSpecMotor

class TestSpecRunner:

    def __init__(self, specVersion='', Timeout=0):
        self.motordict = {'1':TestQtSpecMotor('1'), '2':TestQtSpecMotor('2'),\
                     '3':TestQtSpecMotor('3'), '4':TestQtSpecMotor('4'),\
                     '5':TestQtSpecMotor('5')}

        self.specVersion = 'thiscomp:nospec'
    def __call__(self, x):
        strings=QtCore.QString(x).split(' ')

        motorA = self.motordict[str(strings[1])]
        motorB = self.motordict[str(strings[-2])]
        if str(strings[0]) in ('mvr','umvr','mmvr'):
            APosition = motorA.getPosition()
            BPosition = motorB.getPosition()
            motorA.move(float(strings[2])+APosition)
            motorB.move(float(strings[-1])+BPosition)
        elif str(strings[0]) in ('mv','umv','mmv'):
            motorA.move(float(strings[2]))
            motorB.move(float(strings[-1]))
        print x

    def abort(self):
        for motor in self.motordict.values():
            motor.end()
        print "ABORT"

    def getMotorsMne(self):
        motors = self.motordict.keys()
        motors.sort()
        return  motors

    def getMotor(self, name):
        return self.motordict[name]


