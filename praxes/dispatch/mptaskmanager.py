"""
"""
from __future__ import with_statement

import copy
import gc
import hashlib
#import logging
import multiprocessing
from threading import RLock
import time

import numpy as np
np.seterr(all='ignore')
from PyQt4 import QtCore


#logger = logging.getLogger(__file__)
DEBUG = False


class QRLock(QtCore.QMutex):

    def __init__(self):
        QtCore.QMutex.__init__(self, QtCore.QMutex.Recursive)

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()


class TaskManager(QtCore.QThread):

    progress_report = QtCore.pyqtSignal(dict)

    @property
    def job_server(self):
        return self._job_server

    @property
    def lock(self):
        return self.__lock

    @property
    def n_cpus(self):
        with self.lock:
            return copy.copy(self._n_cpus)

    @property
    def n_points(self):
        with self.lock:
            return copy.copy(self._n_points)

    @property
    def n_processed(self):
        with self.lock:
            return copy.copy(self._n_processed)
    @n_processed.setter
    def n_processed(self, val):
        with self.lock:
            self._n_processed = copy.copy(val)

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

    def __init__(self, scan, results, **kwargs):
        super(TaskManager, self).__init__()

        self.__lock = QRLock()

        self._scan = scan
        self._n_points = scan.entry.npoints
        self._n_cpus = kwargs.get(
            'n_local_processes', multiprocessing.cpu_count()
            )
        self._available_workers = 3 * self._n_cpus

        self._results = results
        self.job_queue = []

        self._job_server = self.create_pool()

        self.__stopped = False

        self._next_index = 0
        self._n_processed = 0

    def __iter__(self):
        return self

    def next(self):
        """
        This needs to be reimplemented to return either:

        * (func, args) tuple such that func(*args) will work
        * 0 if the point was masked
        * None if the data is not yet available
        """
        raise NotImplementedError

    def create_pool(self):
        raise NotImplementedError()

    def _data_processed(self, data):
        with self.lock:
            self._available_workers += 1

        self.update_records(data)

        stats = {'n_processed': self.n_processed}
        self.progress_report.emit(stats)

    def process_data(self):
        while not self.stopped:
            with self.lock:
                if self._available_workers:
                    self._available_workers -= 1
                else:
                    time.sleep(0.01)
                    continue

            try:
                item = self.next()
            except StopIteration:
                self.job_server.close()
                self.job_server.join()
                break

            if item is None:
                # next data point is not yet available
                time.sleep(0.1)
                continue

            if item: # could be zero if masked
                f, args = item
                self.job_server.apply_async(
                    f, args, callback=self._data_processed
                    )
                #self.job_queue.append(job)

            self.n_processed += 1

    def run(self):
        self.process_data()
        self.scan.file.flush()

    def stop(self):
        self.stopped = True

    def update_records(self, data):
        raise NotImplementedError()
