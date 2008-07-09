"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import gc
import hashlib
import logging
import os
import Queue
import tempfile
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import pp
from PyQt4 import QtCore
import numpy
numpy.seterr(all='ignore')

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


logger = logging.getLogger('XPaXS.core.dispatch.ppdispatcher')
DEBUG = False


class PPDispatcherThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(PPDispatcherThread, self).__init__(parent)

        self.mutex = QtCore.QMutex()

        settings = QtCore.QSettings()
        settings.beginGroup('PPJobServers')
        ncpus, ok = settings.value('LocalProcesses',
                                   QtCore.QVariant(1)).toInt()
        self.jobServer = pp.Server(ncpus, ('*',))
        # TODO: make this configurable
        self.jobServer.set_ncpus(ncpus)
        self.numCpus = numpy.sum([i for i in
                            self.jobServer.get_active_nodes().itervalues()])
        self.numQueued = 0
        self.numProcessed = 0
        self.numSkipped = 0
        self.numExpected = 0
        self.queue = Queue.Queue()

        self.dirty = False
        self.stopped = False
        self.completed = False

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.report)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.cleanup)

    def cleanup(self):
        gc.collect()

    def findNextPoint(self):
        raise NotImplementedError

    def getQueue(self):
        return self.queue

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()

    def processData(self):
        while 1:
            if self.isStopped(): return

            self.queueNext()
            self.jobServer.wait()

            if self.numExpected <= (self.numProcessed+self.numSkipped): return

    def queueNext(self):
        raise NotImplementedError

    def report(self):
        if DEBUG: print self
        if self.dirty:
            self.emit(QtCore.SIGNAL("dataProcessed"))
            self.emit(QtCore.SIGNAL("ppJobStats"), self.jobServer.get_stats())
            self.dirty = False

    def run(self):
        self.timer.start(1000)
        self.processData()
        self.stop()
        self.emit(QtCore.SIGNAL('finished()'))

    def setData(self, *args, **kwargs):
        raise NotImplementedError

    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def updateRecords(self, data):
        raise NotImplementedError
