"""
"""
from __future__ import with_statement

import copy
import gc
import hashlib
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
    def jobServer(self):
        return self._jobServer

    @property
    def lock(self):
        return self.__lock

    @property
    def numCpus(self):
        with self.lock:
            return copy.copy(self._numCpus)

    @property
    def scan(self):
        return self._scan

    def _get_stopped(self):
        with self.lock:
            return copy.copy(self.__stopped)
    def _set_stopped(self, val):
        with self.lock:
            self.__stopped = copy.copy(val)
    stopped = property(_get_stopped, _set_stopped)

    def __init__(self, scan, enumerators=None, parent=None):
        super(PPTaskManager, self).__init__(parent)

        self.__lock = QRLock()

        with self.lock:
            settings = QtCore.QSettings()
            settings.beginGroup('PPJobServers')
            ncpus, ok = settings.value(
                'LocalProcesses', QtCore.QVariant(1)
            ).toInt()
            try:
                self._jobServer = pp.Server(ncpus, ('*',))
            except ValueError:
                # this should not be necessary with pp-1.5.6 and later:
                secret = hashlib.md5(str(time.time())).hexdigest()
                self._jobServer = pp.Server(
                    ppservers=('*', ), secret=secret
                )

            self.jobServer.set_ncpus(ncpus)
            self._numCpus = np.sum(
                [i for i in self.jobServer.get_active_nodes().itervalues()]
            )

            self.__dirty = False
            self.__stopped = False

            self._total_processed = 0
            self._lastReport = time.time()

            self._scan = scan

            if enumerators is None:
                enumerators = [enumerate([])]
            self._enumerators = enumerators

    def processData(self):
        while 1:
            if self.stopped:
                return

            numSubmitted = 0
            try:
                while True:
                    temp = [i.next() for i in self._enumerators]
                    index, data = temp[0][0], temp[0][1]
                    if data is None:
                        continue
                    for i, d in temp[1:]:
                        data += d
                    self.submitJob(index, data)
                    numSubmitted += 1
                    if numSubmitted >= self.numCpus*3:
                        break
                else:
                    self._jobServer.wait()
                    self._scan.file.flush()
                    if self.dirty:
                        self.emit(QtCore.SIGNAL("dataProcessed"))
                        self.dirty = False
                    return
            except (IndexError, ValueError):
                pass

            if numSubmitted > 0:
                self.jobServer.wait()
                self._scan.file.flush()
                if self.dirty:
                    self.emit(QtCore.SIGNAL("dataProcessed"))
                    self.dirty = False
            else:
                time.sleep(0.1)

    def submitJob(self, numJobs):
        raise NotImplementedError

    def reportStats(self):
        with self.lock:
            self.emit(
                QtCore.SIGNAL('percentComplete'),
                int((100.0 * self._total_processed) / self.scan.npoints)
            )

            stats = copy.deepcopy(self.jobServer.get_stats())
            self.emit(QtCore.SIGNAL("ppJobStats"), stats)

    def run(self):
        self.processData()
        self.jobServer.destroy()

    def setData(self, *args, **kwargs):
        raise NotImplementedError

    def stop(self):
        self.stopped = True

    def updateRecords(self, data):
        raise NotImplementedError
