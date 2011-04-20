"""
"""
from __future__ import with_statement

import copy
import gc
import hashlib
import logging
import multiprocessing
import threading
import time

import numpy as np
np.seterr(all='ignore')
from PyQt4 import QtCore


logger = logging.getLogger(__file__)
DEBUG = False


class TaskManager(threading.Thread):

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

    def __init__(self, scan, progress_queue, **kwargs):
        super(TaskManager, self).__init__()

        self.__lock = threading.RLock()

        self._scan = scan
        self._n_points = scan.entry.npoints
        self._n_cpus = kwargs.get(
            'n_local_processes', multiprocessing.cpu_count()
            )

        self.progress_queue = progress_queue
        self.job_queue = []

        self._job_server = self.create_pool()

        self.__stopped = False

        self._next_index = 0
        self._n_processed = 0
        self._n_submitted = 0

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

    def flush(self):
        while True:
            try:
                job = self.job_queue.pop(0)
                job.wait()
                #if res is not None:
                #    self.update_records(res)
            except IndexError:
                break
        self.n_submitted = 0
        self.queue_results()

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
                continue

            if item:
                f, args = item
                job = self.job_server.apply_async(
                    f, args, callback=self.update_records
                    )
                self.job_queue.append(job)

            self.n_processed += 1
            self.n_submitted += 1

            if self.n_submitted >= self.n_cpus*3:
                self.flush()

        self.job_server.close()
        self.job_server.join()
        if self.n_submitted > 0:
            self.flush()

    def queue_results(self):
        stats = {}
        stats['n_processed'] = self.n_processed
        self.progress_queue.put(stats)

    def run(self):
        self.process_data()
        self.scan.file.flush()

    def stop(self):
        self.stopped = True

    def update_records(self, data):
        raise NotImplementedError()
