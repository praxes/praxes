"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import gc
import logging

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


logger = logging.getLogger(__file__)
DEBUG = False


class PPTaskManager(QtCore.QThread):

    def __init__(self, parent=None):
        super(PPTaskManager, self).__init__(parent)

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

        self.dirty = False
        self.stopped = False

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.report)

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()

    def processData(self):
        while 1:
            if self.isStopped(): return

            try:
                self._submitJobs(self.numCpus*3)
                self.jobServer.wait()
            except StopIteration:
                self.jobServer.wait()
                return

    def _submitJobs(self):
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
        self.jobServer.destroy()

    def setData(self, *args, **kwargs):
        raise NotImplementedError

    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()
        self.timer.stop()

    def updateRecords(self, data):
        raise NotImplementedError
