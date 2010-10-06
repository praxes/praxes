#$Id: SpecConnectionsManager.py,v 1.13 2005/09/27 13:54:58 guijarro Exp $
"""Module for managing connections to Spec

The SpecConnectionsManager module provides facilities to get
a connection to Spec. It can run a thread for 'asynchronous'
polling of socket events. It prevents from having more than
one connection to the same Spec server at the same time, and
automatically reconnects lost connections.


Classes :
  _ThreadedSpecConnectionsManager
  _SpecConnectionsManager
"""

__author__ = 'Matias Guijarro'
__version__ = '1.1'

import atexit
import threading
import time
import weakref
import asyncore
import sys
import gc

import SpecConnection
import SpecEventsDispatcher


_SpecConnectionsManagerInstance = None #keep a reference to the Singleton instance


def SpecConnectionsManager(pollingThread = True, also_dispatch_events=False):
    """Return the Singleton Spec connections manager instance"""
    global _SpecConnectionsManagerInstance

    if _SpecConnectionsManagerInstance is None:
        if pollingThread:
            _SpecConnectionsManagerInstance = _ThreadedSpecConnectionsManager(also_dispatch_events)

            def _endSpecConnectionsManager():
                global _SpecConnectionsManagerInstance

                if _SpecConnectionsManagerInstance is not None:
                    _SpecConnectionsManagerInstance.stop()
                    _SpecConnectionsManagerInstance = None

            # register _endSpecConnectionsManager() to be called on Python interpreter exit
            atexit.register(_endSpecConnectionsManager)
        else:
            _SpecConnectionsManagerInstance = _SpecConnectionsManager()

    return _SpecConnectionsManagerInstance


class _ThreadedSpecConnectionsManager(threading.Thread):
    """Class for managing connections to Spec

    Polling of asynchronous socket events is delegated to a separate thread

    Warning: should never be instanciated directly ; use the module level SpecConnectionsManager()
    function instead.
    """
    def __init__(self, dispatch_events):
        """Constructor"""
        threading.Thread.__init__(self)

        self.lock = threading.Lock()
        self.connections = {}
        self.connectionDispatchers = {}
        self.stopEvent = threading.Event()
        self.__started = False
        self.doEventsDispatching = dispatch_events
        self.setDaemon(True)


    def run(self):
        """Override Thread.run() ; define behaviour for the connections manager thread

        For each SpecConnection object in the connections dictionary, try to make
        a connection. If the connection is already established, nothing occurs.
        Poll the asyncore dispatchers for processing socket events.
        """
        self.__started = True

        while not self.stopEvent.isSet():
            self.lock.acquire()
            try:
                connection_dispatcher_keys = self.connectionDispatchers.keys()
                for k in connection_dispatcher_keys:
                  connection = self.connectionDispatchers.get(k)
                  if connection is not None:
                    connection.makeConnection()

                if self.stopEvent.isSet():
                    break
            finally:
                self.lock.release()

            if len(self.connectionDispatchers) > 0:
                asyncore.loop(0.01, False, None, 1)
                if self.doEventsDispatching:
                  SpecEventsDispatcher.dispatch()
            else:
                time.sleep(0.01)

        asyncore.loop(0.01, False, None, 1)


    def stop(self):
        """Stop the connections manager thread and dereferences all connections"""
        self.stopEvent.set()

        self.join()

        self.__started = False
        self.connections = {}


    def getConnection(self, specVersion):
        """Return a SpecConnection object

        Arguments:
        specVersion -- a string in the 'host:port' form
        """
        gc.collect()

        try:
            con = self.connections[specVersion]()
        except KeyError:
            con = SpecConnection.SpecConnection(specVersion)

            def removeConnection(ref, connectionName = specVersion):
                self.closeConnection(connectionName)

            self.connections[specVersion] = weakref.ref(con, removeConnection)

            self.lock.acquire()
            try:
                self.connectionDispatchers[specVersion] = con.dispatcher
            finally:
                self.lock.release()

        if not self.__started:
            self.start()
            self.__started = True

        return con


    def closeConnection(self, specVersion):
        self.lock.acquire()
        try:
            self.connectionDispatchers[specVersion].handle_close()

            del self.connectionDispatchers[specVersion]
            del self.connections[specVersion]
        finally:
            self.lock.release()


    def closeConnections(self):
        for connectionName in self.connectionDispatchers.keys():
            self.closeConnection(connectionName)


class _SpecConnectionsManager:
    """Class for managing connections to Spec

    The poll() method should be called inside a GUI loop during idle time.
    Unlike the threaded class, the poll method will also dispatch SpecClient events

    Warning: should never be instanciated directly ; use the module level SpecConnectionsManager()
    function instead.
    """
    def __init__(self):
        """Constructor"""
        self.connections = {}
        self.connectionDispatchers = {}


    def poll(self, timeout=0.01):
        """Poll the asynchronous socket connections and dispatch incomming events"""
        connection_dispatcher_keys = self.connectionDispatchers.keys()
        for k in connection_dispatcher_keys:
          connection = self.connectionDispatchers.get(k)
          if connection is not None:
            connection.makeConnection()

        asyncore.loop(timeout, False, None, 1)

        SpecEventsDispatcher.dispatch()


    def stop(self):
        """Stop the connections manager thread and dereferences all connections"""
        self.connections = {}


    def getConnection(self, specVersion):
        """Return a SpecConnection object

        Arguments:
        specVersion -- a string in the 'host:port' form
        """
        con = self.connections.get(specVersion)
        if con is None or con() is None:
            con = SpecConnection.SpecConnection(specVersion)

            def removeConnection(ref, connectionName = specVersion):
                self.closeConnection(connectionName)

            self.connections[specVersion] = weakref.ref(con, removeConnection)
            self.connectionDispatchers[specVersion] = con.dispatcher
        else:
            con = con()

        return con
    

    def closeConnection(self, specVersion):
        try:
            self.connectionDispatchers[specVersion].handle_close()

            del self.connectionDispatchers[specVersion]
            del self.connections[specVersion]
        except:
            pass


    def closeConnections(self):
        for connectionName in self.connectionDispatchers.keys():
            self.closeConnection(connectionName)


















