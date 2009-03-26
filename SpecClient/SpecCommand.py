"""SpecCommand module

This module defines the classes Spec command
objects

Classes:
BaseSpecCommand
SpecCommand
SpecCommandA
"""

__author__ = 'Matias Guijarro'
__version__ = '1.0'

import types
import logging
from SpecConnection import SpecClientNotConnectedError
from SpecReply import SpecReply
import SpecConnectionsManager
import SpecEventsDispatcher
import SpecWaitObject

class BaseSpecCommand:
    """Base class for SpecCommand objects"""
    def __init__(self, command = None, connection = None):
        self.command = None
        self.connection = None
        self.specVersion = None
        self.isConnected = self.isSpecConnected #alias

        if connection is not None:
            if type(connection) in (types.UnicodeType, types.StringType):
                #
                # connection is given in the 'host:port' form
                #
                self.connectToSpec(str(connection))
            else:
                self.connection = connection

        if command is not None:
            self.setCommand(command)


    def connectToSpec(self, specVersion):
        pass


    def isSpecConnected(self):
        return self.connection is not None and self.connection.isSpecConnected()


    def isSpecReady(self):
        if self.isSpecConnected():
            try:
                status_channel = self.connection.getChannel("status/ready")
                status = status_channel.read()
            except:
                pass
            else:
                return status

        return False


    def setCommand(self, command):
        self.command = command


    def __repr__(self):
        return '<SpecCommand object, command=%s>' % self.command or ''


    def __call__(self, *args, **kwargs):
        if self.command is None:
            return

        if self.connection is None or not self.connection.isSpecConnected():
            return

        if self.connection.serverVersion < 3:
            func = False

            if 'function' in kwargs:
                func = kwargs['function']

            #convert args list to string args list
            #it is much more convenient using .call('psvo', 12) than .call('psvo', '12')
            #a possible problem will be seen in Spec
            args = map(repr, args)

            if func:
                # macro function
                command = self.command + '(' + ','.join(args) + ')'
            else:
                # macro
                command = self.command + ' ' + ' '.join(args)
        else:
            # Spec knows
            command = [self.command] + list(args)

        return self.executeCommand(command)


    def executeCommand(self, command):
        pass



class SpecCommand(BaseSpecCommand):
    """SpecCommand objects execute macros and wait for results to get back"""
    def __init__(self, command, connection, timeout = None):
        self.__timeout = timeout
        BaseSpecCommand.__init__(self, command, connection)


    def connectToSpec(self, specVersion):
        self.connection = SpecConnectionsManager.SpecConnectionsManager().getConnection(specVersion)
        self.specVersion = specVersion

        SpecWaitObject.waitConnection(self.connection, self.__timeout)


    def executeCommand(self, command):
        if self.connection.serverVersion < 3:
            connectionCommand = 'send_msg_cmd_with_return'
        else:
            if type(command) == types.StringType:
                connectionCommand = 'send_msg_cmd_with_return'
            else:
                connectionCommand = 'send_msg_func_with_return'

        return SpecWaitObject.waitReply(self.connection, connectionCommand, (command, ), self.__timeout)



class SpecCommandA(BaseSpecCommand):
    """SpecCommandA is the asynchronous version of SpecCommand.
    It allows custom waiting by subclassing."""
    def __init__(self, *args, **kwargs):
        self.__callback = None
        self.__error_callback = None

        BaseSpecCommand.__init__(self, *args, **kwargs)


    def connectToSpec(self, specVersion):
        if self.connection is not None:
            SpecEventsDispatcher.disconnect(self.connection, 'connected', self.connected)
            SpecEventsDispatcher.disconnect(self.connection, 'disconnected', self.disconnected)

        self.connection = SpecConnectionsManager.SpecConnectionsManager().getConnection(specVersion)
        self.specVersion = specVersion

        SpecEventsDispatcher.connect(self.connection, 'connected', self.connected)
        SpecEventsDispatcher.connect(self.connection, 'disconnected', self.disconnected)
        self.connection.registerChannel("status/ready", self.statusChanged)

        if self.connection.isSpecConnected():
            self.connected()


    def connected(self):
        pass


    def disconnected(self):
        pass


    def statusChanged(self, ready):
        pass


    def executeCommand(self, command):
        self.beginWait()

        if self.connection.serverVersion < 3:
            id = self.connection.send_msg_cmd_with_return(command)
        else:
            if type(command) == types.StringType:
                id = self.connection.send_msg_cmd_with_return(command)
            else:
                id = self.connection.send_msg_func_with_return(command)


    def __call__(self, *args, **kwargs):
        self.__callback = kwargs.get("callback", None)
        self.__error_callback = kwargs.get("error_callback", None)

        return BaseSpecCommand.__call__(self, *args, **kwargs)


    def replyArrived(self, reply):
        if reply.error:
            if callable(self.__error_callback):
                try:
                    self.__error_callback()
                except:
                    logging.getLogger("SpecClient").exception("Error while calling error callback (command=%s,spec version=%s)", self.command, self.specVersion)
                self.__error_callback = None
        else:
            if callable(self.__callback):
                try:
                    self.__callback(reply.data)
                except:
                    logging.getLogger("SpecClient").exception("Error while calling error callback (command=%s,spec version=%s)", self.command, self.specVersion)
                self.__callback = None


    def beginWait(self):
        pass


    def abort(self):
        if self.connection is None or not self.connection.isSpecConnected():
            return

        self.connection.abort()













