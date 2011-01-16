"""SpecCounter module

This module defines the classes for counter objects

Classes:
SpecCounter -- class representing a counter in Spec
SpecCounterA -- class representing a counter in Spec, to be used with a GUI
"""

__author__ = 'Matias Guijarro'
__version__ = '1.0'

import SpecConnectionsManager
import SpecEventsDispatcher
import SpecWaitObject

(COUNTING) = (3)
(UNKNOWN, SCALER, TIMER, MONITOR) = (0, 1,2,3)

class SpecCounter:
    """SpecCounter class"""
    def __init__(self, specName = None, specVersion = None, timeout = None):
        """Constructor

        Keyword arguments:
        specName -- the name of the counter in Spec (defaults to None)
        specVersion -- 'host:port' string representing a Spec server to connect to (defaults to None)
        timeout -- optional timeout for connection (defaults to None)
        """
        self.channelName = ''
        self.connection = None
        self.type = UNKNOWN

        if specName is not None and specVersion is not None:
            self.connectToSpec(specName, specVersion, timeout)
        else:
            self.specName = None
            self.specVersion = None


    def connectToSpec(self, specName, specVersion, timeout = None):
        """Connect to a remote Spec

        Connect to Spec

        Arguments:
        specName -- name of the counter in Spec
        specVersion -- 'host:port' string representing a Spec server to connect to
        timeout -- optional timeout for connection (defaults to None)
        """
        self.specName = specName
        self.specVersion = specVersion

        self.connection = SpecConnectionsManager.SpecConnectionsManager().getConnection(specVersion)

        w = SpecWaitObject.SpecWaitObject(self.connection)
        w.waitConnection(timeout)

        c = self.connection.getChannel('var/%s' % self.specName)
        index = c.read()
        if index == 0:
            self.type = TIMER
        elif index == 1:
            self.type = MONITOR
        else:
            self.type = SCALER


    def count(self, time):
        """Count up to a certain time or monitor count

        Arguments:
        time -- count time
        """
        if self.connection is not None:
            c1 = self.connection.getChannel('scaler/.all./count')
            c2 = self.connection.getChannel('scaler/%s/value' % self.specName)

            if self.type == MONITOR:
                time = -time

            c1.write(time)

            w = SpecWaitObject.SpecWaitObject(self.connection)
            w.waitChannelUpdate('scaler/.all./count', waitValue = 0)

            return c2.read()


    def getValue(self):
        """Return current counter value."""
        if self.connection is not None:
            c = self.connection.getChannel('scaler/%s/value' % self.specName)

            return c.read()














