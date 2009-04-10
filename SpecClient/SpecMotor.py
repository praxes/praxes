#$Id: SpecMotor.py,v 1.6 2005/02/08 13:17:21 guijarro Exp $
"""SpecMotor module

This module defines the classes for motor objects

Classes:
SpecMotor -- class representing a motor in Spec
SpecMotorA -- class representing a motor in Spec, to be used with a GUI
"""

__author__ = 'Matias Guijarro'
__version__ = '1.0'

import SpecConnectionsManager
import SpecEventsDispatcher
import SpecWaitObject
import SpecCommand
import logging
import types
import math

(NOTINITIALIZED, UNUSABLE, READY, MOVESTARTED, MOVING, ONLIMIT) = (0,1,2,3,4,5)
(NOLIMIT, LOWLIMIT, HIGHLIMIT) = (0,2,4)

class SpecMotorA:
    """SpecMotorA class"""
    def __init__(self, specName = None, specVersion = None):
        """Constructor

        Keyword arguments:
        specName -- name of the motor in Spec (defaults to None)
        specVersion -- 'host:port' string representing a Spec server to connect to (defaults to None)
        """
        self.motorState = NOTINITIALIZED
        self.limit = NOLIMIT
        self.limits = (None, None)
        self.chanNamePrefix = ''
        self.connection = None
        self.__old_position = None

        if specName is not None and specVersion is not None:
            self.connectToSpec(specName, specVersion)
        else:
            self.specName = None
            self.specVersion = None


    def connectToSpec(self, specName, specVersion):
        """Connect to a remote Spec

        Connect to Spec and register channels of interest for the specified motor

        Arguments:
        specName -- name of the motor in Spec
        specVersion -- 'host:port' string representing a Spec server to connect to
        """
        self.specName = specName
        self.specVersion = specVersion
        self.chanNamePrefix = 'motor/%s/%%s' % specName

        self.connection = SpecConnectionsManager.SpecConnectionsManager().getConnection(specVersion)
        SpecEventsDispatcher.connect(self.connection, 'connected', self.__connected)
        SpecEventsDispatcher.connect(self.connection, 'disconnected', self.__disconnected)

        #
        # register channels
        #
        self.connection.registerChannel(self.chanNamePrefix % 'low_limit', self.motorLimitsChanged)
        self.connection.registerChannel(self.chanNamePrefix % 'high_limit', self.motorLimitsChanged)
        self.connection.registerChannel(self.chanNamePrefix % 'position', self.__motorPositionChanged, dispatchMode=SpecEventsDispatcher.FIREEVENT)
        self.connection.registerChannel(self.chanNamePrefix % 'move_done', self.motorMoveDone, dispatchMode = SpecEventsDispatcher.FIREEVENT)
        self.connection.registerChannel(self.chanNamePrefix % 'high_lim_hit', self.__motorLimitHit)
        self.connection.registerChannel(self.chanNamePrefix % 'low_lim_hit', self.__motorLimitHit)
        self.connection.registerChannel(self.chanNamePrefix % 'sync_check', self.__syncQuestion)
        self.connection.registerChannel(self.chanNamePrefix % 'unusable', self.__motorUnusable)
        self.connection.registerChannel(self.chanNamePrefix % 'offset', self.motorOffsetChanged)
        self.connection.registerChannel(self.chanNamePrefix % 'sign', self.signChanged)
        #self.connection.registerChannel(self.chanNamePrefix % 'dial_position', self.dialPositionChanged)

        if self.connection.isSpecConnected():
            self.__connected()


    def __connected(self):
        """Private callback triggered by a 'connected' event from Spec."""
        self.connected()


    def connected(self):
        """Callback triggered by a 'connected' event from Spec

        To be extended by derivated classes.
        """
        pass


    def __disconnected(self):
        """Private callback triggered by a 'disconnected' event from Spec

        Put the motor in NOTINITIALIZED state.
        """
        self.__changeMotorState(NOTINITIALIZED)
        self.disconnected()


    def disconnected(self):
        """Callback triggered by a 'disconnected' event from Spec

        To be extended by derivated classes.
        """
        pass


    #def dialPositionChanged(self, dial_position):
    #    pass


    def signChanged(self, sign):
        self.motorLimitsChanged()


    def motorOffsetChanged(self, offset):
        self.motorLimitsChanged()


    def motorLimitsChanged(self):
        """Callback triggered by a 'low_limit' or a 'high_limit' channel update,
        or when the sign or offset for motor changes

        To be extended by derivated classes.
        """
        pass


    def motorMoveDone(self, channelValue):
        """Callback triggered when motor starts or stops moving

        Change the motor state accordingly.

        Arguments:
        channelValue -- value of the channel
        """
        if channelValue:
            self.__changeMotorState(MOVING)
        elif self.motorState == MOVING or self.motorState == MOVESTARTED or self.motorState == NOTINITIALIZED:
            self.__changeMotorState(READY)


    def __motorLimitHit(self, channelValue, channelName):
        """Private callback triggered by a 'low_lim_hit' or a 'high_lim_hit' channel update

        Update the motor state accordingly.

        Arguments:
        channelValue -- value of the channel
        channelName -- name of the channel (either 'low_lim_hit' or 'high_lim_hit')
        """
        if channelValue:
            if channelName.endswith('low_lim_hit'):
                self.limit = self.limit | LOWLIMIT
                self.__changeMotorState(ONLIMIT)
            else:
                self.limit = self.limit | HIGHLIMIT
                self.__changeMotorState(ONLIMIT)


    def __motorPositionChanged(self, absolutePosition):
        if self.__old_position is None:
           self.__old_position = absolutePosition
           self.motorPositionChanged(absolutePosition)
        else:
           if math.fabs(absolutePosition - self.__old_position) > 1E-6:
              self.__old_position = absolutePosition
              self.motorPositionChanged(absolutePosition)


    def motorPositionChanged(self, absolutePosition):
        """Callback triggered by a position channel update

        To be extended by derivated classes.

        Arguments:
        absolutePosition -- motor absolute position
        """
        pass


    def setOffset(self, offset):
        """Set the motor offset value"""
        c = self.connection.getChannel(self.chanNamePrefix % 'offset')

        c.write(offset)


    def getOffset(self):
        c = self.connection.getChannel(self.chanNamePrefix % 'offset')

        return c.read()


    def getSign(self):
        c = self.connection.getChannel(self.chanNamePrefix % 'sign')

        return c.read()


    def __syncQuestion(self, channelValue):
        """Callback triggered by a 'sync_check' channel update

        Call the self.syncQuestionAnswer method and reply to the sync. question.

        Arguments:
        channelValue -- value of the channel
        """
        if type(channelValue) == type(''):
            steps = channelValue.split()
            specSteps = steps[0]
            controllerSteps = steps[1]

            a = self.syncQuestionAnswer(specSteps, controllerSteps)

            if a is not None:
                c = self.connection.getChannel(self.chanNamePrefix % 'sync_check')
                c.write(a)


    def syncQuestionAnswer(self, specSteps, controllerSteps):
        """Answer to the sync. question

        Return either '1' (YES) or '0' (NO)

        Arguments:
        specSteps -- steps measured by Spec
        controllerSteps -- steps indicated by the controller
        """
        pass


    def __motorUnusable(self, unusable):
        """Private callback triggered by a 'unusable' channel update

        Update the motor state accordingly

        Arguments:
        unusable -- value of the channel
        """
        if unusable:
            self.__changeMotorState(UNUSABLE)
        else:
            self.__changeMotorState(READY)


    def __changeMotorState(self, state):
        """Private method for changing the SpecMotor object's internal state

        Arguments:
        state -- the motor state
        """
        self.motorState = state
        self.motorStateChanged(state)


    def motorStateChanged(self, state):
        """Callback to take into account a motor state update

        To be extended by derivated classes

        Arguments:
        state -- the motor state
        """
        pass


    def move(self, absolutePosition):
        """Move the motor to the required position

        Arguments:
        absolutePosition -- position to move to
        """
        if type(absolutePosition) != types.FloatType and type(absolutePosition) != types.IntType:
            logging.getLogger("SpecClient").error("Cannot move %s: position '%s' is not a number", self.specName, absolutePosition)

        self.__changeMotorState(MOVESTARTED)

        c = self.connection.getChannel(self.chanNamePrefix % 'start_one')

        c.write(absolutePosition)


    def moveRelative(self, relativePosition):
        self.move(self.getPosition() + relativePosition)


    def moveToLimit(self, limit):
        cmdObject = SpecCommand.SpecCommandA("_mvc", self.connection)

        if cmdObject.isSpecReady():
            if limit:
                cmdObject(1)
            else:
                cmdObject(-1)


    def stop(self):
        """Stop the current motor

        Send an 'abort' message to the remote Spec
        """
        self.connection.abort()


    def stopMoveToLimit(self):
        c = self.connection.getChannel("var/_MVC_CONTINUE_MOVING")
        c.write(0)


    def getParameter(self, param):
        c = self.connection.getChannel(self.chanNamePrefix % param)
        return c.read()


    def setParameter(self, param, value):
        c = self.connection.getChannel(self.chanNamePrefix % param)
        c.write(value)


    def getPosition(self):
        """Return the current position of the motor."""
        c = self.connection.getChannel(self.chanNamePrefix % 'position')

        return c.read()


    def getState(self):
        """Return the current motor state."""
        return self.motorState


    def getLimits(self):
        """Return a (low limit, high limit) tuple in user units."""
        lims = [x * self.getSign() + self.getOffset() for x in (self.connection.getChannel(self.chanNamePrefix % 'low_limit').read(), \
                                                                self.connection.getChannel(self.chanNamePrefix % 'high_limit').read())]
        return (min(lims), max(lims))


    def getDialPosition(self):
        """Return the motor dial position."""
        c = self.connection.getChannel(self.chanNamePrefix % 'dial_position')

        return c.read()


class SpecMotor:
    """Spec Motor"""
    def __init__(self, specName = None, specVersion = None, timeout = None):
        """Constructor

        Keyword arguments:
        specName -- name of the motor in Spec (defaults to None)
        specVersion -- 'host:port' string representing a Spec server to connect to (defaults to None)
        timeout -- optional timeout for the connection (defaults to None)
        """
        self.chanNamePrefix = ''
        self.connection = None

        if specName is not None and specVersion is not None:
            self.connectToSpec(specName, specVersion, timeout)
        else:
            self.specName = None
            self.specVersion = None


    def connectToSpec(self, specName, specVersion, timeout = None):
        """Connect to a remote Spec

        Block until Spec is connected or timeout occurs

        Arguments:
        specName -- name of the motor in Spec
        specVersion -- 'host:port' string representing a Spec server to connect to
        timeout -- optional timeout for the connection (defaults to None)
        """
        self.specName = specName
        self.specVersion = specVersion
        self.chanNamePrefix = 'motor/%s/%%s' % specName

        self.connection = SpecConnectionsManager.SpecConnectionsManager().getConnection(specVersion)

        w = SpecWaitObject.SpecWaitObject(self.connection)
        w.waitConnection(timeout)


    def unusable(self):
        """Return whether the motor is unusable or not."""
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'unusable')

            return c.read()


    def lowLimitHit(self):
        """Return if low limit has been hit."""
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'low_lim_hit')

            return c.read()


    def highLimitHit(self):
        """Return if high limit has been hit."""
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'high_lim_hit')

            return c.read()


    def move(self, absolutePosition):
        """Move the motor

        Block until the move is finished

        Arguments:
        absolutePosition -- position where to move the motor to
        """
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'start_one')

            c.write(absolutePosition)

            w = SpecWaitObject.SpecWaitObject(self.connection)
            w.waitChannelUpdate(self.chanNamePrefix % 'move_done', waitValue = 0) #move_done is set to 0 when move has finished


    def moveRelative(self, relativePosition):
        self.move(self.getPosition() + relativePosition)


    def moveToLimit(self, limit):
        if self.connection is not None:
            cmdObject = SpecCommand.SpecCommandA("_mvc", self.connection)

            if cmdObject.isSpecReady():
                if limit:
                    cmdObject(self.specName, 1)
                else:
                    cmdObject(self.specName, -1)


    def stop(self):
        """Stop the current motor

        Send an 'abort' message to the remote Spec
        """
        self.connection.abort()


    def stopMoveToLimit(self):
        if self.connection is not None:
            c = self.connection.getChannel("var/_MVC_CONTINUE_MOVING")
            c.write(0)


    def getPosition(self):
        """Return the current absolute position for the motor."""
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'position')

            return c.read()


    def setOffset(self, offset):
        """Set the motor offset value"""
        if self.connection is not None:
             c = self.connection.getChannel(self.chanNamePrefix % 'offset')

             c.write(offset)


    def getOffset(self):
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'offset')

            return c.read()


    def getSign(self):
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'sign')

            return c.read()


    def getDialPosition(self):
        if self.connection is not None:
            c = self.connection.getChannel(self.chanNamePrefix % 'dial_position')

            return c.read()


    def getLimits(self):
        if self.connection is not None:
            lims = [x * self.getSign() + self.getOffset() for x in (self.connection.getChannel(self.chanNamePrefix % 'low_limit').read(), \
                                                                    self.connection.getChannel(self.chanNamePrefix % 'high_limit').read())]
            return (min(lims), max(lims))
















