#$Id: SpecChannel.py,v 1.6 2006/12/14 10:03:13 guijarro Exp $
"""SpecChannel module

This module defines the SpecChannel class
"""

__author__ = 'Matias Guijarro'
__version__ = '1.0'

import SpecEventsDispatcher
import SpecWaitObject
import weakref
import types

(DOREG, DONTREG, WAITREG) = (0, 1, 2)

class SpecChannel:
    """SpecChannel class

    Represent a channel in Spec

    Signals:
    valueChanged(channelValue, channelName) -- emitted when the channel gets updated
    """
    #channel_aliases = {}

    def __init__(self, connection, channelName, registrationFlag = DOREG):
        """Constructor

        Arguments:
        connection -- a SpecConnection object
        channelName -- string representing a channel name, i.e. 'var/toto'

        Keyword arguments:
        registrationFlag -- defines how the channel is registered, possible
        values are : SpecChannel.DOREG (default), SpecChannel.DONTREG
        (do not register), SpecChannel.WAITREG (delayed registration until Spec is
        reconnected)
        """
        self.connection = weakref.ref(connection)
        self.name = channelName

        if channelName.startswith("var/") and '/' in channelName[4:]:
            l = channelName.split('/')
            self.spec_chan_name = "/".join((l[0], l[1]))

            if len(l)==3:
                self.access1=l[2]
                self.access2=None
            else:
                self.access1=l[2]
                self.access2=l[3]
        else:
            self.spec_chan_name = self.name
            self.access1=None
            self.access2=None
        self.registrationFlag = registrationFlag
        self.isdisconnected = True
        self.registered = False
        self.value = None

        SpecEventsDispatcher.connect(connection, 'connected', self.connected)
        SpecEventsDispatcher.connect(connection, 'disconnected', self.disconnected)

        if connection.isSpecConnected():
            self.connected()


    def connected(self):
        """Do registration when Spec gets connected

        If registration flag is WAITREG put the flag to DOREG if not yet connected,
        and register if DOREG
        """
        if self.registrationFlag == WAITREG:
            if self.isdisconnected:
                self.registrationFlag = DOREG

        self.isdisconnected = False

        if self.registrationFlag == DOREG:
            self.register()


    def disconnected(self):
        """Reset channel object when Spec gets disconnected."""
        self.value = None
        self.isdisconnected = True


    def unregister(self):
        """Unregister channel."""
        connection = self.connection()

        if connection is not None:
            connection.send_msg_unregister(self.spec_chan_name)
            self.registered = False
            self.value = None


    def register(self):
        """Register channel

        Registering a channel means telling the server we want to receive
        update events when a channel value changes on the server side.
        """
        if self.spec_chan_name != self.name:
            return

        connection = self.connection()

        if connection is not None:
            connection.send_msg_register(self.spec_chan_name)
            self.registered = True


    def update(self, channelValue, deleted = False,force=False):
        """Update channel's value and emit the 'valueChanged' signal."""
        if type(channelValue) == types.DictType and self.access1 is not None:
            if self.access1 in channelValue:
                if deleted:
                    SpecEventsDispatcher.emit(self, 'valueChanged', (None, self.name, ))
                else:
                    if self.access2 is None:
                        if force or self.value is None or self.value != channelValue[self.access1]: 
                            self.value = channelValue[self.access1]
                            SpecEventsDispatcher.emit(self, 'valueChanged', (self.value, self.name, ))
                    else:
                        if self.access2 in channelValue[self.access1]:
                            if deleted:
                                SpecEventsDispatcher.emit(self, 'valueChanged', (None, self.name, ))
                            else:
                                if force or self.value is None or self.value != channelValue[self.access1][self.access2]:
                                    self.value = channelValue[self.access1][self.access2]
                                    SpecEventsDispatcher.emit(self, 'valueChanged', (self.value, self.name, ))
            return

        if type(self.value) == types.DictType and type(channelValue) == types.DictType:
            # update dictionary
            if deleted:
                for key,val in channelValue.iteritems():
                    if type(val) == types.DictType:
                        for k in val:
                            try:
                                del self.value[key][k]
                            except KeyError:
                                pass
                        if len(self.value[key])==1 and None in self.value[key]:
                            self.value[key]=self.value[key][None]
                    else:
                        try:
                            del self.value[key]
                        except KeyError:
                            pass
            else:
                for k1,v1 in channelValue.iteritems():
                    if type(v1)==types.DictType:
                        try:
                            self.value[k1].update(v1)
                        except KeyError:
                            self.value[k1]=v1
                        except AttributeError:
                            self.value[k1]={None: self.value[k1]}
                            self.value[k1].update(v1)
                    else:
                        if self.value.has_key(k1) and type(self.value[k1]) == types.DictType:
                            self.value[k1][None] = v1
                        else:
                            self.value[k1] = v1
            value2emit=self.value.copy()
        else:
            if deleted:
                self.value = None
            else:
                self.value = channelValue
            value2emit=self.value

        SpecEventsDispatcher.emit(self, 'valueChanged', (value2emit, self.name, ))


    def read(self):
        """Read the channel value

        If channel is registered, just return the internal value,
        else obtain the channel value and return it.
        """
        if self.registered and self.value is not None:
            #we check 'value is not None' because the
            #'registered' flag could be set, but before
            #the message with the channel value arrived ;
            #in this case, the 'else' is executed and the
            #channel value is read (slower...)
            return self.value
        else:
            connection = self.connection()

            if connection is not None:
                w = SpecWaitObject.SpecWaitObject(connection)
                # make sure spec is connected, we give a short timeout
                # because it is supposed to be the case already
                w.waitConnection(timeout=500)                                 
                w.waitReply('send_msg_chan_read', (self.spec_chan_name, ))

                self.update(w.value)

        return self.value


    def write(self, value):
        """Write a channel value."""
        connection = self.connection()

        if connection is not None:
            if self.access1 is not None:
                if self.access2 is None:
                    value = { self.access1: value }
                else:
                    value = { self.access1: { self.access2: value } }

            connection.send_msg_chan_send(self.spec_chan_name, value)















