"""
"""

import logging
import sys
import os

from PyQt4 import QtCore, QtGui

from xpaxs.frontends.base.ui import ui_analysiswindow
from xpaxs.frontends.base.mainwindow import MainWindowBase


logger = logging.getLogger(__file__)


class AnalysisWindowBase(ui_analysiswindow.Ui_AnalysisWindow, MainWindowBase):

    """
    """

    def __init__(self, scanData, parent=None):
        super(AnalysisWindowBase, self).__init__(parent)

        self.setupUi(self)

        self._configureDockArea()

        self.statusBar.showMessage('Ready', 2000)

        self._setupDockWindows()
        self._restoreSettings()

        self.analysisView = self._getAnalysisView(scanData)

        self.setCentralWidget(self.analysisView)

        title = '%s: Scan %s'%(scan.getDataFileName(), scan.getScanNumber())
        self.setWindowTitle(title)

    def _setupDockWindows(self):
        self._setupPPJobStats()

    def _setupPPJobStats(self):
        from xpaxs.frontends.base.ppjobstats import PPJobStats

        self.ppJobStats = PPJobStats()
        self.ppJobStatsDock = self._createDockWindow('PPJobStatsDock')
        self._setupDockWindow(self.ppJobStatsDock,
                               QtCore.Qt.RightDockWidgetArea,
                               self.ppJobStats, 'Analysis Server Stats')


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    form = MainWindowBase()
    form.show()
    sys.exit(app.exec_())
