"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from __future__ import absolute_import

import logging
import sys
import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyMca import McaAdvancedFit
from PyQt4 import QtCore, QtGui
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import __version__
from ..mainwindow import MainWindow as MainWindowBase
from .fileinterface2 import XfsH5FileInterface

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.frontends.xfs.ui.mainwindow')

USE_PYMCA_ADVANCEDFIT = False
McaAdvancedFit.USE_BOLD_FONT = False


class MainWindow(MainWindowBase):
    """Establishes a Experiment controls

    1) establishes week connection to specrunner
    2) creates ScanIO instance with Experiment Controls
    3) Connects Actions from Toolbar

    """

#    def __init__(self, parent=None):
#        super(MainWindow, self).__init__(parent)
#
#    def _setupDockWindows(self):
#        MainWindowBase._setupDockWindows(self)
#
#        self.spectrumAnalysisDock = self._createDockWindow('SpectrumAnalysisDock')
#        if USE_PYMCA_ADVANCEDFIT:
#            self.spectrumAnalysis = McaAdvancedFit.McaAdvancedFit(
#                top=False,
#                margin=0,
#                spacing=0
#            )
#            self.spectrumAnalysis.matrixSpectrumButton.close()
#            self.spectrumAnalysis.graphWindow.setMinimumHeight(10)
#            self.spectrumAnalysis.headerLabel.hide()
#            self.spectrumAnalysis.dismissButton.hide()
#            self.spectrumAnalysis.configureButton.hide()
#            self.spectrumAnalysis.setData(
#                x=numpy.arange(1000),
#                y=numpy.zeros(1000)
#            )
#
#        else:
#            from xpaxs.frontends.xfs.mcaspectrum import McaSpectrum
#            from PyMca.ConcentrationsWidget import Concentrations
#
#            self.concentrationsAnalysisDock = \
#                self._createDockWindow('ConcentrationAnalysisDock')
#            self.concentrationsAnalysis = Concentrations()
#            self._setupDockWindow(
#                self.concentrationsAnalysisDock,
#                QtCore.Qt.BottomDockWidgetArea,
#                self.concentrationsAnalysis,
#                'Concentrations Analysis'
#            )
#            self.spectrumAnalysis = McaSpectrum(self.concentrationsAnalysis)
#
#        self._setupDockWindow(self.spectrumAnalysisDock,
#                               QtCore.Qt.BottomDockWidgetArea,
#                               self.spectrumAnalysis, 'Spectrum Analysis')

    def _setFileInterface(self):
        self.fileInterface = XfsH5FileInterface(self)
        for key, (item, area, action) in \
                self.fileInterface.dockWidgets.iteritems():
            self.menuView.addAction(action)
            self.addDockWidget(area, item)

    def getScanView(self, scan):
        # this is a shortcut for now, in the future the view would be
        # an overview of the entry with ability to open different analyses
        from xpaxs.frontends.xfs.mcaanalysiswindow import McaAnalysisWindow

        return McaAnalysisWindow(scan, self)


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    form = SmpMainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
