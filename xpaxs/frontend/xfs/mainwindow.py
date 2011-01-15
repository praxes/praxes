"""
"""

from __future__ import absolute_import

import logging
import sys
import os

from PyMca import McaAdvancedFit
from PyQt4 import QtCore, QtGui

from xpaxs import __version__
from ..base.mainwindow import MainWindow as MainWindowBase
from xpaxs.io import phynx


logger = logging.getLogger(__file__)

USE_PYMCA_ADVANCEDFIT = False
McaAdvancedFit.USE_BOLD_FONT = False


class MainWindow(MainWindowBase):
    """Establishes a Experiment controls

    1) establishes week connection to specrunner
    2) creates ScanIO instance with Experiment Controls
    3) Connects Actions from Toolbar

    """

    def getScanView(self, scan):
        # this is a shortcut for now, in the future the view would be
        # an overview of the entry with ability to open different analyses
        if isinstance(scan, phynx.registry['Entry']):
            from xpaxs.frontends.xfs.mcaanalysiswindow import McaAnalysisWindow
            if len(scan['measurement'].mcas) > 0:
                return McaAnalysisWindow(scan, self)
            else:
                msg = QtGui.QErrorMessage(self)
                msg.showMessage(
                    'The entry you selected has no MCA data to process'
                )


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    form = SmpMainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
