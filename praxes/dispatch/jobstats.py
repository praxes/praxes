"""
"""

from __future__ import absolute_import

import hashlib
import logging
import multiprocessing
import time

import numpy as np
from PyQt4 import QtCore, QtGui

from .ui import ui_jobstats


logger = logging.getLogger(__file__)


class JobStats(ui_jobstats.Ui_JobStats, QtGui.QWidget):

    def __init__(self, parent=None):
        super(JobStats, self).__init__(parent)
        self.setupUi(self)

        self.numCpusSpinBox.setMaximum(multiprocessing.cpu_count())

        self.updateTable()

        self.refreshButton.clicked.connect(self.updateTable)
        self.numCpusSpinBox.valueChanged.connect(self.updateLocalProcesses)

        settings = QtCore.QSettings()
        settings.beginGroup('JobServers')
        default = self.numCpusSpinBox.minimum()
        val, ok = settings.value('LocalProcesses',
                                 QtCore.QVariant(default)).toInt()
        if val > self.numCpusSpinBox.maximum():
            val = self.numCpusSpinBox.maximum()
        self.numCpusSpinBox.setValue(val)

    def updateLocalProcesses(self, val):
        settings = QtCore.QSettings()
        settings.beginGroup('JobServers')
        settings.setValue('LocalProcesses', QtCore.QVariant(val))

    def updateTable(self, statsDict=None):
        if statsDict is None:
            return

        self.jobStatsTable.setUpdatesEnabled(False)
        self.jobStatsTable.clearContents()
        self.jobStatsTable.setRowCount(len(statsDict))
        for row, (address, stats) in enumerate(statsDict.items()):
            item = QtGui.QTableWidgetItem(address)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 0, item)

            item = QtGui.QTableWidgetItem(str(stats['n_cpus']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 1, item)

            item = QtGui.QTableWidgetItem(str(stats['n_jobs']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 2, item)

            item = QtGui.QTableWidgetItem('%.2f'%stats['time'])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 3, item)

        self.jobStatsTable.resizeColumnsToContents()
        self.jobStatsTable.resizeRowsToContents()
        self.jobStatsTable.sortItems(0, QtCore.Qt.DescendingOrder)
        self.jobStatsTable.setUpdatesEnabled(True)
