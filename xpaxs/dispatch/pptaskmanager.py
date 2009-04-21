"""
"""
from __future__ import with_statement

import copy
import gc
import logging
import time

import pp
from PyQt4 import QtCore
import numpy as np
np.seterr(all='ignore')


logger = logging.getLogger(__file__)
DEBUG = False


class QRLock(QtCore.QMutex):

    """
    """

    def __init__(self):
        QtCore.QMutex.__init__(self, QtCore.QMutex.Recursive)

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()


class PPTaskManager(QtCore.QThread):

    def _get_dirty(self):
        with self.lock:
            return copy.copy(self.__dirty)
    def _set_dirty(self, val):
        with self.lock:
            self.__dirty = copy.copy(val)
    dirty = property(_get_dirty, _set_dirty)

    @property
    def lock(self):
        return self.__lock

    @property
    def numCpus(self):
        with self.lock:
            return copy.copy(self._numCpus)

    def _get_stopped(self):
        with self.lock:
            return copy.copy(self.__stopped)
    def _set_stopped(self, val):
        with self.lock:
            self.__stopped = copy.copy(val)
    stopped = property(_get_stopped, _set_stopped)

    def __init__(self, scan, enumerator=None, parent=None):
        super(PPTaskManager, self).__init__(parent)

        self.__lock = QRLock()

        with self.lock:
            settings = QtCore.QSettings()
            settings.beginGroup('PPJobServers')
            ncpus, ok = settings.value(
                'LocalProcesses', QtCore.QVariant(1)
            ).toInt()
            self._jobServer = pp.Server(ncpus, ('*',))
            # TODO: make this configurable
            self._jobServer.set_ncpus(ncpus)
            self._numCpus = np.sum(
                [i for i in self._jobServer.get_active_nodes().itervalues()]
            )

            self.__dirty = False
            self.__stopped = False

            self._totalProcessed = 0
            self._lastReport = time.time()

            self._scan = scan

            if enumerator is None:
                enumerator = enumerate([])
            self._enumerator = enumerator

    def processData(self):
        while 1:
            with self.lock:
                if self.stopped:
                    return

                try:
                    numSubmitted = 0
                    for index, data in self._enumerator:
                        self.submitJob(index, data)
                        numSubmitted += 1
                        if numSubmitted >= self.numCpus*3:
                            break
                    else:
                        self._jobServer.wait()
                        self.report(force=True)
                        return
                except (IndexError, ValueError):
                    pass
                self._jobServer.wait()
                self.report()

            time.sleep(0.1)

    def submitJob(self, numJobs):
        raise NotImplementedError

    def report(self, force=False):
        if DEBUG: print self

        if self.dirty:
            with self.lock:
                with self._scan.plock:
                    track = self._totalProcessed + self._enumerator.total_skipped
                    total = self._scan.npoints
                self.emit(
                    QtCore.SIGNAL('percentComplete'),
                    (100.0 * track) / total
                )

                stats = copy.deepcopy(self._jobServer.get_stats())
                self.emit(QtCore.SIGNAL("ppJobStats"), stats)

                reportNow = force or (time.time() - self._lastReport >= 2)

                if reportNow:
                    self.emit(QtCore.SIGNAL("dataProcessed"))
                    self._lastReport = time.time()

                self.dirty = False

    def run(self):
        self.processData()
        self._jobServer.destroy()

    def setData(self, *args, **kwargs):
        raise NotImplementedError

    def stop(self):
        self.stopped = True

    def updateRecords(self, data):
        raise NotImplementedError
