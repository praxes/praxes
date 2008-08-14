from PyQt4 import QtCore

class TestQtSpecMotor(QtCore.QObject):

    def __init__(self,mne, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.specname = mne
        self.position = int(mne)*10
        self.toGoTo=0
        self.limits=(int(mne),int(mne)*1000)
        self.paramdict = {'step_size':int(mne)*1000,
                          'slew_rate':int(mne)*1000,
                          'acceleration':int(mne)*10}

        self.__state_strings = ['NOTINITIALIZED',
                       'UNUSABLE',
                       'READY',
                       'MOVESTARTED',
                       'MOVING',
                       'ONLIMIT']

        self.state = 'READY'
        self.Timer = QtCore.QTimer()
        self.time =int(mne)*1000

        self.connect(self.Timer, QtCore.SIGNAL('timeout()'), self.end)

    def getPosition(self):
        return self.position

    def getParameter(self,parameter):
        return self.paramdict[parameter]

    def getState(self):
        return self.state

    def getLimits(self):
        return self.limits

    def move(self,amount=0):
        if self.state in ('READY','ONLIMIT'):
            self.Timer.start(self.time)
            self.state = 'MOVING'
            state = 4
            self.toGoTo=amount
            self.motorStateChanged(state)

    def end(self):
        self.Timer.stop()
        self.state = 'READY'
        state = 2
        self.motorStateChanged(state)
        self.position=self.toGoTo
        self.motorPositionChanged(self.getPosition())

    def motorStateChanged(self, state):
        state = self.__state_strings[state]
        self.emit(QtCore.SIGNAL("motorStateChanged(PyQt_PyObject)"),state)

    def motorLimitsChanged(self):
        limits = self.getLimits()
        self.emit(QtCore.SIGNAL("motorLimitsChanged(PyQt_PyObject)"),
                  limits)

    def motorPositionChanged(self, absolutePosition):
        self.emit(QtCore.SIGNAL("motorPositionChanged(PyQt_PyObject)"),
                  absolutePosition)
