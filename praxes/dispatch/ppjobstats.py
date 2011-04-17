"""
"""

from __future__ import absolute_import

import hashlib
import logging
import time

import numpy as np
import pp
from PyQt4 import QtCore, QtGui

from .ui import ui_ppjobstats


logger = logging.getLogger(__file__)


class PPJobStats(ui_ppjobstats.Ui_PPJobStats, QtGui.QWidget):

    def __init__(self, parent=None):
        super(PPJobStats, self).__init__(parent)
        self.setupUi(self)

        try:
            self.server = pp.Server(ppservers=('*', ))
        except ValueError:
            # this should not be necessary with pp-1.5.6 and later:
            secret = hashlib.md5(str(time.time())).hexdigest()
            self.server = pp.Server(
                ppservers=('*', ), secret=secret
            )
        self.numCpusSpinBox.setMaximum(self.server.get_ncpus())

        self.updateTable()

        self.refreshButton.clicked.connect(self.updateTable)
        self.numCpusSpinBox.valueChanged.connect(self.server.set_ncpus)
        self.numCpusSpinBox.valueChanged.connect(self.updateLocalProcesses)

        settings = QtCore.QSettings()
        settings.beginGroup('PPJobServers')
        default = self.numCpusSpinBox.minimum()
        val, ok = settings.value('LocalProcesses',
                                 QtCore.QVariant(default)).toInt()
        if val > self.numCpusSpinBox.maximum():
            val = self.numCpusSpinBox.maximum()
        self.numCpusSpinBox.setValue(val)

    def updateLocalProcesses(self, val):
        settings = QtCore.QSettings()
        settings.beginGroup('PPJobServers')
        settings.setValue('LocalProcesses',
                          QtCore.QVariant(val))

    def updateTable(self, statsDict=None):
        if statsDict is None: statsDict = self.server.get_stats()

        totalJobs = np.sum([i.njobs for i in statsDict.values()])

        self.jobStatsTable.setUpdatesEnabled(False)
        self.jobStatsTable.clearContents()
        self.jobStatsTable.setRowCount(len(statsDict))
        for row, (address, stats) in enumerate(statsDict.items()):
            item = QtGui.QTableWidgetItem(address)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 0, item)

            item = QtGui.QTableWidgetItem(str(stats.ncpus))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 1, item)

            item = QtGui.QTableWidgetItem(str(stats.njobs))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 2, item)

            try:
                item = QtGui.QTableWidgetItem('%.2f'%(100.*stats.njobs/totalJobs))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.jobStatsTable.setItem(row, 3, item)
            except ZeroDivisionError:
                pass

            item = QtGui.QTableWidgetItem('%.2f'%stats.time)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.jobStatsTable.setItem(row, 4, item)

            try:
                item = QtGui.QTableWidgetItem('%.4f'%(stats.time/stats.njobs))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.jobStatsTable.setItem(row, 5, item)
            except ZeroDivisionError:
                pass

        self.jobStatsTable.resizeColumnsToContents()
        self.jobStatsTable.resizeRowsToContents()
        self.jobStatsTable.sortItems(0, QtCore.Qt.DescendingOrder)
        self.jobStatsTable.setUpdatesEnabled(True)
