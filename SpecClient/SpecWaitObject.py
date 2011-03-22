"""SpecWaitObject module

This module defines the classes for helper objects
designed for waiting specific events from Spec

Classes:
SpecWaitObject -- base class for Wait objects

Functions:
waitChannel -- wait for a channel update
waitReply -- wait for a reply
waitConnection -- wait for a connection
"""

__author__ = 'Matias Guijarro'
__version__ = '1.0'

import weakref
import time
import types

import SpecEventsDispatcher
from SpecClient.SpecClientError import SpecClientError, SpecClientTimeoutError
import SpecConnectionsManager


def waitFunc(timeout):
  """Waiting function

  Arguments:
  timeout -- waiting time in milliseconds
  """
  try:
    P = getattr(SpecConnectionsManager.SpecConnectionsManager(), "poll")
  except AttributeError:
    time.sleep(timeout/1000.0)
    SpecEventsDispatcher.dispatch()
  else:
    P(timeout/1000.0)


class SpecWaitObject:
    """Helper class for waiting specific events from Spec"""
    def __init__(self, connection):
        """Constructor

        Arguments:
        connection -- a SpecConnection object
        """
        self.connection = weakref.ref(connection)
        self.isdisconnected = True
        self.channelWasUnregistered = False
        self.value = None

        SpecEventsDispatcher.connect(connection, 'connected', self.connected)
        SpecEventsDispatcher.connect(connection, 'disconnected', self.disconnected)

        if connection.isSpecConnected():
            self.connected()


    def connected(self):
        """Callback triggered by a 'connected' event."""
        self.isdisconnected = False


    def disconnected(self):
        """Callback triggered by a 'disconnected' event."""
        self.isdisconnected = True


    def waitReply(self, command, argsTuple, timeout = None):
        """Wait for a reply from Spec

        Arguments:
        command -- method returning a replyID to be executed on the connection object
        argsTuple -- tuple of arguments to be passed to the command
        timeout -- optional timeout (defaults to None)
        """
        connection = self.connection()

        if connection is not None:
            try:
                func = getattr(connection, command)
            except:
                return
            else:
                if callable(func):
                    func(*argsTuple)

                self.wait(timeout = timeout)


    def waitChannelUpdate(self, chanName, waitValue = None, timeout = None):
        """Wait for a channel update

        Arguments:
        chanName -- channel name
        waitValue -- particular value to wait (defaults to None, meaning any value)
        timeout -- optional timeout (defaults to None)
        """
        connection = self.connection()

        if connection is not None:
            self.channelWasUnregistered = False
            channel = connection.getChannel(chanName)

            if not channel.registered:
                self.channelWasUnregistered = True
                connection.registerChannel(chanName, self.channelUpdated) #channel.register()
            else:
                SpecEventsDispatcher.connect(channel, 'valueChanged', self.channelUpdated)

            self.wait(waitValue = waitValue, timeout = timeout)

            if self.channelWasUnregistered:
                connection.unregisterChannel(chanName) #channel.unregister()


    def waitConnection(self, timeout = None):
        """Wait for the connection to Spec being established

        Arguments:
        timeout -- optional timeout (defaults to None)

        Exceptions:
        timeout -- raise a timeout exception on timeout
        """
        connection = self.connection()

        if connection is not None:
            t = 0

            while self.isdisconnected:
                SpecEventsDispatcher.dispatch()

                t0 = time.time()
                waitFunc(10)
                t += (time.time() - t0)*1000

                if timeout is not None and t >= timeout:
                    raise SpecClientTimeoutError


    def wait(self, waitValue = None, timeout = None):
        """Block until the object's internal value gets updated

        Arguments:
        waitValue -- particular value to wait (defaults to None, meaning any value)
        timeout -- optional timeout (defaults to None)

        Exceptions:
        timeout -- raise a timeout exception on timeout
        """
        t0 = time.time()
        while not self.isdisconnected:
            waitFunc(10)

            if self.value is not None:
                if waitValue is None:
                    return

                if waitValue == self.value:
                    return
                else:
                    self.value = None

            if self.value is None:
                t = (time.time() - t0)*1000
                if timeout is not None and t >= timeout:
                    raise SpecClientTimeoutError


    def replyArrived(self, reply):
        """Callback triggered by a reply from Spec."""
        self.value = reply.getValue()

        if reply.error:
            raise SpecClientError('Server request did not complete: %s' % self.value, reply.error_code)


    def channelUpdated(self, channelValue):
        """Callback triggered by a channel update

        If channel was unregistered, we skip the first update,
        else we update our internal value
        """
        if self.channelWasUnregistered == True:
            #
            # if we were unregistered, skip first update
            #
            self.channelWasUnregistered = 2
        else:
            self.value = channelValue


def waitConnection(connection, timeout = None):
    """Wait for a connection to Spec to be established

    Arguments:
    connection -- a 'host:port' string
    timeout -- optional timeout (defaults to None)
    """
    if type(connection) in (types.UnicodeType, types.StringType):
      from SpecClient.SpecConnectionsManager import SpecConnectionsManager
      connection = SpecConnectionsManager().getConnection(str(connection))

    w = SpecWaitObject(connection)

    w.waitConnection(timeout = timeout)


def waitChannelUpdate(chanName, connection, waitValue = None, timeout = None):
    """Wait for a channel to be updated

    Arguments:
    chanName -- channel name (e.g 'var/toto')
    connection -- a 'host:port' string
    waitValue -- value to wait (defaults to None)
    timeout -- optional timeout (defaults to None)
    """
    if type(connection) in (types.UnicodeType, types.StringType):
      connection = str(connection)
      from SpecClient.SpecConnectionsManager import SpecConnectionsManager
      connection = SpecConnectionsManager().getConnection(connection)
      waitConnection(connection, timeout = timeout)

    w = SpecWaitObject(connection)
    w.waitChannelUpdate(chanName, waitValue = waitValue, timeout = timeout)

    return w.value


def waitReply(connection, command, argsTuple, timeout = None):
    """Wait for a reply from a remote Spec server

    Arguments:
    connection -- a 'host:port' string
    command -- command to execute
    argsTuple -- tuple of arguments for the command
    timeout -- optional timeout (defaults to None)
    """
    if type(connection) in (types.UnicodeType, types.StringType):
      connection = str(connection)
      from SpecClient.SpecConnectionsManager import SpecConnectionsManager
      connection = SpecConnectionsManager().getConnection(connection)
      waitConnection(connection, timeout = timeout)

    w = SpecWaitObject(connection)
    w.waitReply(command, argsTuple, timeout=timeout)

    return w.value















