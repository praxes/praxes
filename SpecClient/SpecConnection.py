#$Id: SpecConnection.py,v 1.11 2005/12/09 10:32:24 guijarro Exp $
"""SpecConnection module

Low-level module for communicating with a
remove Spec server

Classes :
SpecClientNotConnectedError -- exception class
SpecConnection
SpecConnectionDispatcher
"""

__author__ = 'Matias Guijarro'
__version__ = '1.0'

import asyncore
import socket
import weakref
import string
import logging
import time
from SpecClient.SpecClientError import SpecClientNotConnectedError
import SpecEventsDispatcher
import SpecChannel
import SpecMessage
import SpecReply
import traceback
import sys

asyncore.dispatcher.ac_in_buffer_size = 32768 #32 ko input buffer

(DISCONNECTED, PORTSCANNING, WAITINGFORHELLO, CONNECTED) = (1,2,3,4)
(MIN_PORT, MAX_PORT) = (6510, 6530)

class SpecConnection:
    """Represent a connection to a remote Spec

    Signals:
    connected() -- emitted when the required Spec version gets connected
    disconnected() -- emitted when the required Spec version gets disconnected
    replyFromSpec(reply id, SpecReply object) -- emitted when a reply comes from the remote Spec
    error(error code) -- emitted when an error event is received from the remote Spec
    """
    def __init__(self, *args):
        """Constructor"""
        self.dispatcher = SpecConnectionDispatcher(*args)

        SpecEventsDispatcher.connect(self.dispatcher, 'connected', self.connected)
        SpecEventsDispatcher.connect(self.dispatcher, 'disconnected', self.disconnected)
        #SpecEventsDispatcher.connect(self.dispatcher, 'replyFromSpec', self.replyFromSpec)
        SpecEventsDispatcher.connect(self.dispatcher, 'error', self.error)


    def __str__(self):
        return str(self.dispatcher)


    def __getattr__(self, attr):
        """Delegate access to the underlying SpecConnectionDispatcher object"""
        if not attr.startswith('__'):
            return getattr(self.dispatcher, attr)
        else:
            raise AttributeError


    def connected(self):
        """Propagate 'connection' event"""
        SpecEventsDispatcher.emit(self, 'connected', ())


    def disconnected(self):
        """Propagate 'disconnection' event"""
        SpecEventsDispatcher.emit(self, 'disconnected', ())


    #def replyFromSpec(self, replyID, reply):
    #    """Propagate 'reply from Spec' event"""
    #    SpecEventsDispatcher.emit(self, 'replyFromSpec', (replyID, reply, ))


    def error(self, error):
        """Propagate 'error' event"""
        SpecEventsDispatcher.emit(self, 'error', (error, ))


class SpecConnectionDispatcher(asyncore.dispatcher):
    """SpecConnection class

    Signals:
    connected() -- emitted when the required Spec version gets connected
    disconnected() -- emitted when the required Spec version gets disconnected
    replyFromSpec(reply id, SpecReply object) -- emitted when a reply comes from the remote Spec
    error(error code) -- emitted when an error event is received from the remote Spec
    """
    def __init__(self, specVersion):
        """Constructor

        Arguments:
        specVersion -- a 'host:port' string
        """
        asyncore.dispatcher.__init__(self)

        self.state = DISCONNECTED
        self.connected = False
        self.receivedStrings = []
        self.message = None
        self.serverVersion = None
        self.scanport = False
        self.scanname = ''
        self.aliasedChannels = {}
        self.registeredChannels = {}
        self.registeredReplies = {}
        self.sendq = []
        self.outputStrings = []
        self.simulationMode = False
        self.valid_socket = False

        # some shortcuts
        self.macro       = self.send_msg_cmd_with_return
        self.macro_noret = self.send_msg_cmd
        self.abort         = self.send_msg_abort

        tmp = str(specVersion).split(':')
        self.host = tmp[0]

        if len(tmp) > 1:
            self.port = tmp[1]
        else:
            self.port = 6789

        try:
            self.port = int(self.port)
        except:
            self.scanname = self.port
            self.port = None
            self.scanport = True

        #
        # register 'service' channels
        #
        self.registerChannel('error', self.error, dispatchMode = SpecEventsDispatcher.FIREEVENT)
        self.registerChannel('status/simulate', self.simulationStatusChanged)

    def __str__(self):
        return '<connection to Spec, host=%s, port=%s>' % (self.host, self.port or self.scanname)

    def set_socket(self, s):
      self.valid_socket = True
      asyncore.dispatcher.set_socket(self, s)

    def makeConnection(self):
        """Establish a connection to Spec

        If the connection is already established, do nothing.
        Otherwise, create a socket object and try to connect.
        If we are in port scanning mode, try to connect using
        a port defined in the range from MIN_PORT to MAX_PORT
        """
        if not self.connected:
            if self.scanport:
              if self.port is None or self.port > MAX_PORT:
                self.port = MIN_PORT
              else:
                self.port += 1
            while not self.scanport or self.port < MAX_PORT:
              s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              s.settimeout(0.2)
              try:
                 if s.connect_ex( (self.host, self.port) ) == 0:
                   self.set_socket(s)
                   self.handle_connect()
                   break
              except socket.error, err:
                 pass #exception could be 'host not found' for example, we ignore it
              if self.scanport:
                self.port += 1 
              else:
                break

    def registerChannel(self, chanName, receiverSlot, registrationFlag = SpecChannel.DOREG, dispatchMode = SpecEventsDispatcher.UPDATEVALUE):
        """Register a channel

        Tell the remote Spec we are interested in receiving channel update events.
        If the channel is not already registered, create a new SpecChannel object,
        and connect the channel 'valueChanged' signal to the receiver slot. If the
        channel is already registered, simply add a connection to the receiver
        slot.

        Arguments:
        chanName -- a string representing the channel name, i.e. 'var/toto'
        receiverSlot -- any callable object in Python

        Keywords arguments:
        registrationFlag -- internal flag
        dispatchMode -- can be SpecEventsDispatcher.UPDATEVALUE (default) or SpecEventsDispatcher.FIREEVENT,
        depending on how the receiver slot will be called. UPDATEVALUE means we don't mind skipping some
        channel update events as long as we got the last one (for example, a motor position). FIREEVENT means
        we want to call the receiver slot for every event.
        """
        if dispatchMode is None:
            return

        chanName = str(chanName)

        try:
          if not chanName in self.registeredChannels:
            channel = SpecChannel.SpecChannel(self, chanName, registrationFlag)
            self.registeredChannels[chanName] = channel
            if channel.spec_chan_name != chanName:
                def valueChanged(value, chanName=chanName):
                    channel = self.registeredChannels[chanName]
                    channel.update(value,force=True)
                self.aliasedChannels[chanName]=valueChanged
                self.registerChannel(channel.spec_chan_name, valueChanged, registrationFlag, dispatchMode)
          else:
            channel = self.registeredChannels[chanName]

          SpecEventsDispatcher.connect(channel, 'valueChanged', receiverSlot, dispatchMode)

          channelValue = self.registeredChannels[channel.spec_chan_name].value
          if channelValue is not None:
            # we received a value, so emit an update signal
            channel.update(channelValue,force=True)
        except Exception,e:
          traceback.print_exc()

    def unregisterChannel(self, chanName):
        """Unregister a channel

        Arguments:
        chanName -- a string representing the channel to unregister, i.e. 'var/toto'
        """
        chanName = str(chanName)

        if chanName in self.registeredChannels:
            self.registeredChannels[chanName].unregister()
            del self.registeredChannels[chanName]


    def getChannel(self, chanName):
        """Return a channel object

        If the required channel is already registered, return it.
        Otherwise, return a new 'temporary' unregistered SpecChannel object ;
        reference should be kept in the caller or the object will get dereferenced.

        Arguments:
        chanName -- a string representing the channel name, i.e. 'var/toto'
        """
        if not chanName in self.registeredChannels:
            # return a newly created temporary SpecChannel object, without registering
            return SpecChannel.SpecChannel(self, chanName, SpecChannel.DONTREG)

        return self.registeredChannels[chanName]


    def error(self, error):
        """Emit the 'error' signal when the remote Spec version signals an error."""
        logging.getLogger('SpecClient').error('Error from Spec: %s', error)

        SpecEventsDispatcher.emit(self, 'error', (error, ))


    def simulationStatusChanged(self, simulationMode):
        self.simulationMode = simulationMode


    def isSpecConnected(self):
        """Return True if the remote Spec version is connected."""
        return self.state == CONNECTED


    def specConnected(self):
        """Emit the 'connected' signal when the remote Spec version is connected."""
        old_state = self.state
        self.state = CONNECTED
        if old_state != CONNECTED:
            logging.getLogger('SpecClient').info('Connected to %s:%s', self.host, (self.scanport and self.scanname) or self.port)

            SpecEventsDispatcher.emit(self, 'connected', ())

    def specDisconnected(self):
        """Emit the 'disconnected' signal when the remote Spec version is disconnected."""
        SpecEventsDispatcher.dispatch()

        old_state = self.state
        self.state = DISCONNECTED
        if old_state == CONNECTED:
            logging.getLogger('SpecClient').info('Disconnected from %s:%s', self.host, (self.scanport and self.scanname) or self.port)

            SpecEventsDispatcher.emit(self, 'disconnected', ())

    def handle_close(self):
        """Handle 'close' event on socket."""
        self.connected = False
        self.serverVersion = None
        if self.socket:
            self.close()
        self.valid_socket = False
        self.registeredChannels = {}
        self.aliasedChannels = {}
        self.specDisconnected()


    def disconnect(self):
        """Disconnect from the remote Spec version."""
        self.handle_close()


    def handle_error(self):
        """Handle an uncaught error."""
        exception, error_string, tb = sys.exc_info()
        # let Python display exception like it wants!
        sys.excepthook(exception, error_string, tb)


    def handle_read(self):
        """Handle 'read' events on socket

        Messages are built from the read calls on the socket.
        """
        self.receivedStrings.append(self.recv(32768)) #read at most all the input buffer
        s = ''.join(self.receivedStrings)
        sbuffer = buffer(s)
        consumedBytes = 0
        offset = 0

        while offset < len(sbuffer):
            if self.message is None:
                self.message = SpecMessage.message(version = self.serverVersion)

            consumedBytes = self.message.readFromStream(sbuffer[offset:])

            if consumedBytes == 0:
                break

            offset += consumedBytes

            if self.message.isComplete():
                try:
                    # dispatch incoming message
                    if self.message.cmd == SpecMessage.REPLY:
                        replyID = self.message.sn

                        if replyID > 0:
                            try:
                                reply = self.registeredReplies[replyID]
                            except:
                                logging.getLogger("SpecClient").exception("Unexpected error while receiving a message from server")
                            else:
                                del self.registeredReplies[replyID]

                                reply.update(self.message.data, self.message.type == SpecMessage.ERROR, self.message.err)
                                #SpecEventsDispatcher.emit(self, 'replyFromSpec', (replyID, reply, ))
                    elif self.message.cmd == SpecMessage.EVENT:
                        self.registeredChannels[self.message.name].update(self.message.data, self.message.flags == SpecMessage.DELETED)
                    elif self.message.cmd == SpecMessage.HELLO_REPLY:
                        if self.checkourversion(self.message.name):
                            self.serverVersion = self.message.vers #header version
                            #self.state = CONNECTED
                            self.specConnected()
                        else:
                            self.serverVersion = None
                            self.connected = False
                            self.close()
                            self.state = DISCONNECTED
                except:
                    self.message = None
                    self.receivedStrings = [ s[offset:] ]
                    raise
                else:
                    self.message = None
                                   
        self.receivedStrings = [ s[offset:] ]


    def checkourversion(self, name):
        """Check remote Spec version

        If we are in port scanning mode, check if the name from
        Spec corresponds to our required Spec version.
        """
        if self.scanport:
            if name == self.scanname:
                return True
            else:
                #connected version does not match
                return False
        else:
            return True


    def readable(self):
        return self.valid_socket


    def writable(self):
        """Return True if socket should be written."""
        ret = self.readable() and (len(self.sendq) > 0 or sum(map(len, self.outputStrings)) > 0)
        #print 'writable?', str(self), ret
        return ret


    def handle_connect(self):
        """Handle 'connect' event on socket

        Send a HELLO message.
        """
        self.connected = True

        self.state = WAITINGFORHELLO
        self.send_msg_hello()


    def handle_write(self):
        """Handle 'write' events on socket

        Send all the messages from the queue.
        """
        while len(self.sendq) > 0:
            self.outputStrings.append(self.sendq.pop().sendingString())

        outputBuffer = ''.join(self.outputStrings)

        sent = self.send(outputBuffer)

        self.outputStrings = [ outputBuffer[sent:] ]


    def send_msg_cmd_with_return(self, cmd):
        """Send a command message to the remote Spec server, and return the reply id.

        Arguments:
        cmd -- command string, i.e. '1+1'
        """
        if self.isSpecConnected():
            try:
                caller = sys._getframe(1).f_locals['self']
            except KeyError:
                caller = None

            return self.__send_msg_with_reply(replyReceiverObject = caller, *SpecMessage.msg_cmd_with_return(cmd, version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_func_with_return(self, cmd):
        """Send a command message to the remote Spec server using the new 'func' feature, and return the reply id.

        Arguments:
        cmd -- command string
        """
        if self.serverVersion < 3:
            logging.getLogger('SpecClient').error('Cannot execute command in Spec : feature is available since Spec server v3 only')
        else:
            if self.isSpecConnected():
                try:
                    caller = sys._getframe(1).f_locals['self']
                except KeyError:
                    caller = None

                message = SpecMessage.msg_func_with_return(cmd, version = self.serverVersion)
                return self.__send_msg_with_reply(replyReceiverObject = caller, *message)
            else:
                raise SpecClientNotConnectedError


    def send_msg_cmd(self, cmd):
        """Send a command message to the remote Spec server.

        Arguments:
        cmd -- command string, i.e. 'mv psvo 1.2'
        """
        if self.isSpecConnected():
            self.__send_msg_no_reply(SpecMessage.msg_cmd(cmd, version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_func(self, cmd):
        """Send a command message to the remote Spec server using the new 'func' feature

        Arguments:
        cmd -- command string
        """
        if self.serverVersion < 3:
            logging.getLogger('SpecClient').error('Cannot execute command in Spec : feature is available since Spec server v3 only')
        else:
            if self.isSpecConnected():
                self.__send_msg_no_reply(SpecMessage.msg_func(cmd, version = self.serverVersion))
            else:
                raise SpecClientNotConnectedError


    def send_msg_chan_read(self, chanName):
        """Send a channel read message, and return the reply id.

        Arguments:
        chanName -- a string representing the channel name, i.e. 'var/toto'
        """
        if self.isSpecConnected():
            try:
                caller = sys._getframe(1).f_locals['self']
            except KeyError:
                caller = None

            return self.__send_msg_with_reply(replyReceiverObject = caller, *SpecMessage.msg_chan_read(chanName, version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_chan_send(self, chanName, value):
        """Send a channel write message.

        Arguments:
        chanName -- a string representing the channel name, i.e. 'var/toto'
        value -- channel value
        """
        if self.isSpecConnected():
            self.__send_msg_no_reply(SpecMessage.msg_chan_send(chanName, value, version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_register(self, chanName):
        """Send a channel register message.

        Arguments:
        chanName -- a string representing the channel name, i.e. 'var/toto'
        """
        if self.isSpecConnected():
            self.__send_msg_no_reply(SpecMessage.msg_register(chanName, version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_unregister(self, chanName):
        """Send a channel unregister message.

        Arguments:
        chanName -- a string representing the channel name, i.e. 'var/toto'
        """
        if self.isSpecConnected():
            self.__send_msg_no_reply(SpecMessage.msg_unregister(chanName, version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_close(self):
        """Send a close message."""
        if self.isSpecConnected():
            self.__send_msg_no_reply(SpecMessage.msg_close(version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_abort(self):
        """Send an abort message."""
        if self.isSpecConnected():
            self.__send_msg_no_reply(SpecMessage.msg_abort(version = self.serverVersion))
        else:
            raise SpecClientNotConnectedError


    def send_msg_hello(self):
        """Send a hello message."""
        self.__send_msg_no_reply(SpecMessage.msg_hello())


    def __send_msg_with_reply(self, reply, message, replyReceiverObject = None):
        """Send a message to the remote Spec, and return the reply id.

        The reply object is added to the registeredReplies dictionary,
        with its reply id as the key. The reply id permits then to
        register for the reply using the 'registerReply' method.

        Arguments:
        reply -- SpecReply object which will receive the reply
        message -- SpecMessage object defining the message to send
        """
        replyID = reply.id
        self.registeredReplies[replyID] = reply

        if hasattr(replyReceiverObject, 'replyArrived'):
            SpecEventsDispatcher.connect(reply, 'replyFromSpec', replyReceiverObject.replyArrived)

        self.sendq.insert(0, message)

        return replyID


    def __send_msg_no_reply(self, message):
        """Send a message to the remote Spec.

        If a reply is sent depends only on the message, and not on the
        method to send the message. Using this method, any reply is
        lost.
        """
        self.sendq.insert(0, message)















