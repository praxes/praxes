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

    @property
    def dirty(self):
        with self.lock:
            return copy.copy(self.__dirty)
    @dirty.setter
    def dirty(self, val):
        with self.lock:
            self.__dirty = copy.copy(val)

#    @property
#    def job_server(self):
#        return self._job_server

    @property
    def lock(self):
        return self.__lock

    @property
    def n_cpus(self):
        return 1
        with self.lock:
            return copy.copy(self._n_cpus)

    @property
    def n_processed(self):
        with self.lock:
            return copy.copy(self._n_processed)
    @n_processed.setter
    def n_processed(self, val):
        with self.lock:
            self._n_processed = copy.copy(val)

    @property
    def n_submitted(self):
        with self.lock:
            return copy.copy(self._n_submitted)
    @n_submitted.setter
    def n_submitted(self, val):
        with self.lock:
            self._n_submitted = copy.copy(val)

    @property
    def scan(self):
        return self._scan

    @property
    def stopped(self):
        with self.lock:
            return copy.copy(self.__stopped)
    @stopped.setter
    def stopped(self, val):
        with self.lock:
            self.__stopped = copy.copy(val)

    def __init__(self, scan, parent=None):
        super(PPTaskManager, self).__init__(parent)

        self.__lock = QRLock()

        with self.lock:
            settings = QtCore.QSettings()
            settings.beginGroup('PPJobServers')
            ncpus, ok = settings.value(
                'LocalProcesses', QtCore.QVariant(1)
            ).toInt()
            #try:
            #    self._job_server = pp.Server(ncpus, ('*',))
            #except ValueError:
            #    # this should not be necessary with pp-1.5.6 and later:
            #    secret = hashlib.md5(str(time.time())).hexdigest()
            #    self._job_server = pp.Server(
            #        ppservers=('*', ), secret=secret
            #    )

            #self.job_server.set_ncpus(ncpus)
            #self._n_cpus = np.sum(
            #    [i for i in self.job_server.get_active_nodes().itervalues()]
            #)

            self.__dirty = False
            self.__stopped = False

            self._n_processed = 0
            self._n_submitted = 0

            self._last_report = time.time()

            self._scan = scan

    def __iter__(self):
        """
        The iterator returned by this method must yield an (index, data) tuple,
        or None to signify that the acquisition is ongoing and the next data
        point is not yet available.
        """
        raise NotImplementedError

    def flush(self):
#        self.job_server.wait()
        self.n_submitted = 0
        if self.dirty:
            self.emit(QtCore.SIGNAL("dataProcessed"))
            self.dirty = False
        self.report_stats()

    def process_data(self):
        for item in self:
            if self.stopped:
                break

            if item is None:
                # next data point is not yet available
                if self.n_submitted > 0:
                    self.flush()
                else:
                    time.sleep(0.1)
            else:
                i, data = item
                self.n_processed += 1

                if data is None:
                    # this point was masked, no data to process
                    continue

                self.submit_job(i, data)
                self.n_submitted += 1

            if self.n_submitted >= self.n_cpus*3:
                self.flush()

        self.sleep(1)
        if self.n_submitted > 1:
            self.flush()

    def submit_job(self, num_jobs):
        raise NotImplementedError

    def report_stats(self):
        with self.lock:
            self.emit(
                QtCore.SIGNAL('percentComplete'),
                int((100.0 * self.n_processed) / self.scan.npoints)
            )

            #stats = copy.deepcopy(self.job_server.get_stats())
            #self.emit(QtCore.SIGNAL("ppJobStats"), stats)

    def run(self):
        self.process_data()
        self.scan.file.flush()

    def stop(self):
        self.stopped = True

    def update_records(self, data):
        raise NotImplementedError()
