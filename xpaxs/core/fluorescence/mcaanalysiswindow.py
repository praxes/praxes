"""
"""

from __future__ import absolute_import, with_statement

import copy
import gc
import logging
import posixpath

from PyQt4 import QtCore, QtGui
from PyMca.FitParam import FitParamDialog
import numpy as np

from xpaxs.frontend.analysiswindow import AnalysisWindow
from .ui.ui_mcaanalysiswindow import Ui_McaAnalysisWindow
from .elementsview import ElementsView
import phynx


logger = logging.getLogger(__file__)


class McaAnalysisWindow(Ui_McaAnalysisWindow, AnalysisWindow):

    """
    """

    # TODO: this should eventually take an MCA entry
    def __init__(self, scan_data, parent=None):
        super(McaAnalysisWindow, self).__init__(parent)

        self.analysisThread = None

        if isinstance(scan_data, phynx.Entry):
            self.scan_data = scan_data.measurement
        elif isinstance(scan_data, phynx.Measurement):
            self.scan_data = scan_data
        elif isinstance(scan_data, phynx.MultiChannelAnalyzer):
            self.scan_data = scan_data
        else:
            with scan_data.plock:
                raise TypeError(
                    'H5 node type %s not recognized by McaAnalysisWindow'
                    % scan_data.__class__.__name__
                )

        pymcaConfig = self.scan_data.pymca_config
        self.setupUi(self)

        title = '%s: %s: %s'%(
            posixpath.split(scan_data.file.filename)[-1],
            posixpath.split(getattr(scan_data.entry, 'name', ''))[-1],
            posixpath.split(self.scan_data.name)[-1]
        )
        self.setWindowTitle(title)

        self.elementsView = ElementsView(self.scan_data, self)
        self.splitter.addWidget(self.elementsView)

        self.xrfBandComboBox.addItems(self.availableElements)
        try:
            self.deadTimeReport.setText(
                str(self.scan_data.mcas.values()[0]['dead_time'].format)
                )
        except phynx.H5Error:
            self.deadTimeReport.setText('Not found')

        self._setupMcaDockWindows()
        self._setupPPJobStats()

        plotOptions = self.elementsView.plotOptions
        self.optionsWidgetVLayout.insertWidget(1, plotOptions)

        self.connect(
            self.elementsView,
            QtCore.SIGNAL("pickEvent"),
            self.processAverageSpectrum
        )
        # TODO: remove the window from the list of open windows when we close
#           self.connect(scanView, QtCore.SIGNAL("scanClosed"), self.scanClosed)

        self.fitParamDlg = FitParamDialog(parent=self)

        if pymcaConfig:
            self.fitParamDlg.setParameters(pymcaConfig)
            self.spectrumAnalysis.configure(pymcaConfig)
        else:
            self.configurePymca()

        try:
            eff = self.scan_data.measurement.mcas.values()[0].monitor.efficiency
            self.monitorEfficiency.setText(str(eff))
            self.monitorEfficiency.setEnabled(True)
        except AttributeError:
            pass

        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setMaximumHeight(17)
        self.progressBar.hide()
        self.progressBar.addAction(self.actionAbort)
        self.progressBar.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.analysisThread = None

        self.elementsView.updateFigure()

        self._restoreSettings()

    @property
    def availableElements(self):
        try:
            return sorted(
                self.scan_data['element_maps'].fits.keys()
                )
        except (phynx.H5Error, AttributeError):
            return []

    @property
    def deadTimePercent(self):
        return str(self.deadTimeComboBox.currentText())

    @property
    def mapType(self):
        return str(self.mapTypeComboBox.currentText()).lower().replace(' ', '_')

    @property
    def normalization(self):
        return str(self.normalizationComboBox.currentText())

    @property
    def xrfBand(self):
        return str(self.xrfBandComboBox.currentText())

    @property
    def pymcaConfig(self):
        return self.fitParamDlg.getParameters()

    def _setupMcaDockWindows(self):
        from .mcaspectrum import McaSpectrum
        from PyMca.ConcentrationsWidget import Concentrations

        self.concentrationsAnalysisDock = \
            self._createDockWindow('ConcentrationAnalysisDock')
        self.concentrationsAnalysis = Concentrations()
        self._setupDockWindow(
            self.concentrationsAnalysisDock,
            QtCore.Qt.BottomDockWidgetArea,
            self.concentrationsAnalysis,
            'Concentrations Analysis'
        )

        self.spectrumAnalysisDock = \
            self._createDockWindow('SpectrumAnalysisDock')
        self.spectrumAnalysis = McaSpectrum(self.concentrationsAnalysis)
        self._setupDockWindow(
            self.spectrumAnalysisDock,
            QtCore.Qt.BottomDockWidgetArea,
            self.spectrumAnalysis,
            'Spectrum Analysis'
        )

    def _setupPPJobStats(self):
        from xpaxs.dispatch.ppjobstats import PPJobStats

        self.ppJobStats = PPJobStats()
        self.ppJobStatsDock = self._createDockWindow('PPJobStatsDock')
        self._setupDockWindow(self.ppJobStatsDock,
                               QtCore.Qt.RightDockWidgetArea,
                               self.ppJobStats, 'Analysis Server Stats')

    @QtCore.pyqtSignature("bool")
    def on_actionAbort_triggered(self):
        try:
            self.analysisThread.stop()
        except AttributeError:
            pass

    @QtCore.pyqtSignature("bool")
    def on_actionAnalyzeSpectra_triggered(self):
        self.processData()

    @QtCore.pyqtSignature("bool")
    def on_actionConfigurePymca_triggered(self):
        self.configurePymca()

    @QtCore.pyqtSignature("bool")
    def on_actionCalibration_triggered(self):
        self.processAverageSpectrum()

    @QtCore.pyqtSignature("QString")
    def on_mapTypeComboBox_currentIndexChanged(self):
        self.elementsView.updateFigure(self.getElementMap())

    @QtCore.pyqtSignature("")
    def on_monitorEfficiency_editingFinished(self):
        try:
            value = float(self.monitorEfficiency.text())
            assert (0 < value <= 1)
            for mca in self.scan_data.measurement.mcas.values():
                mca.monitor.efficiency = value
        except (ValueError, AssertionError):
            self.monitorEfficiency.setText(
                str(self.scan_data.measurement.mcas.values()[0].monitor.efficiency)
                )


    @QtCore.pyqtSignature("QString")
    def on_xrfBandComboBox_currentIndexChanged(self):
        self.elementsView.updateFigure(self.getElementMap())

    def closeEvent(self, event):
        if self.analysisThread:
            self.showNormal()
            self.raise_()
            warning = '''Data analysis is not yet complete.
            Are you sure you want to close?'''
            res = QtGui.QMessageBox.question(self, 'closing...', warning,
                                             QtGui.QMessageBox.Yes,
                                             QtGui.QMessageBox.No)
            if res == QtGui.QMessageBox.Yes:
                if self.analysisThread:
                    self.analysisThread.stop()
                    self.analysisThread.wait()
                    QtGui.qApp.processEvents()
            else:
                event.ignore()
                return

        AnalysisWindow.closeEvent(self, event)
        event.accept()

    def configurePymca(self):
        if self.fitParamDlg.exec_():
            QtGui.qApp.processEvents()

            self.statusbar.showMessage('Reconfiguring PyMca ...')
            configDict = self.fitParamDlg.getParameters()
            self.spectrumAnalysis.configure(configDict)
            self.scan_data.pymca_config = configDict
            self.statusbar.clearMessage()

    def elementMapUpdated(self):
        self.elementsView.updateFigure(self.getElementMap())
        QtGui.qApp.processEvents()

    def getElementMap(self, mapType=None, element=None):
        if element is None: element = self.xrfBand
        if mapType is None: mapType = self.mapType

        if mapType and element:
            try:
                entry = '%s_%s'%(element, mapType)
                return self.scan_data['element_maps'][entry].map

            except phynx.H5Error:
                return np.zeros(self.scan_data.acquisition_shape)

        else:
            return np.zeros(self.scan_data.acquisition_shape, dtype='f')

    def initializeElementMaps(self, elements):
        with self.scan_data.plock:
            if 'element_maps' in self.scan_data.measurement:
                del self.scan_data['element_maps']

            elementMaps = self.scan_data.create_group(
                'element_maps', type='ElementMaps'
            )

            for mapType, cls in [
                ('fit', 'Fit'),
                ('fit_error', 'FitError'),
                ('mass_fraction', 'MassFraction')
            ]:
                for element in elements:
                    entry = '%s_%s'%(element, mapType)
                    elementMaps.create_dataset(
                        entry,
                        type=cls,
                        data=np.zeros(self.scan_data.npoints, 'f')
                    )

    def processAverageSpectrum(self, indices=None):
        if indices is None:
            indices = range(self.scan_data.measurement.acquired)
        if len(indices):
            self.statusbar.showMessage('Averaging spectra ...')
            QtGui.qApp.processEvents()

            try:
                # looking at individual element
                channels = self.scan_data.channels
                counts = self.scan_data['counts'].corrected_value.mean(indices)
            except AttributeError:
                # looking at multiple elements
                mcas = self.scan_data.mcas.values()
                channels = mcas[0].channels
                counts = channels.astype('float32') * 0
                for mca in mcas:
                    counts += mca['counts'].corrected_value.mean(indices)

            self.spectrumAnalysis.setData(x=channels, y=counts)

            self.statusbar.showMessage('Performing Fit ...')
            QtGui.qApp.processEvents()
            fitresult = self.spectrumAnalysis.fit()

            self.fitParamDlg.setFitResult(fitresult['result'])

            self.statusbar.clearMessage()

        self.setMenuToolsActionsEnabled(True)

    def processComplete(self):
        self.progressBar.hide()
        self.progressBar.reset()
        self.statusbar.removeWidget(self.progressBar)
        self.statusbar.clearMessage()

        self.analysisThread = None

        self.setMenuToolsActionsEnabled(True)
        self.elementMapUpdated()

    def processData(self):
        from .pptaskmanager import XfsPPTaskManager

        self.setMenuToolsActionsEnabled(False)

        self._resetPeaks()

        thread = XfsPPTaskManager(
            self.scan_data,
            copy.deepcopy(self.pymcaConfig),
        )

        self.connect(
            thread,
            QtCore.SIGNAL('dataProcessed'),
            self.elementMapUpdated
        )
        self.connect(
            thread,
            QtCore.SIGNAL('ppJobStats'),
            self.ppJobStats.updateTable
        )
        self.connect(
            thread,
            QtCore.SIGNAL("finished()"),
            self.processComplete
        )
        self.connect(
            thread,
            QtCore.SIGNAL('percentComplete'),
            self.progressBar.setValue
        )
        self.connect(
            self.actionAbort,
            QtCore.SIGNAL('triggered(bool)'),
            thread.stop
        )

        self.statusbar.showMessage('Analyzing spectra ...')
        self.statusbar.addPermanentWidget(self.progressBar)
        self.progressBar.show()

        self.analysisThread = thread

        thread.start(QtCore.QThread.NormalPriority)

    def _resetPeaks(self):
        peaks = []

        for el, edges in self.pymcaConfig['peaks'].iteritems():
            for edge in edges:
                name = '_'.join([el, edge])
                peaks.append(name)

        peaks.sort()
        self.initializeElementMaps(peaks)

        self.xrfBandComboBox.clear()
        self.xrfBandComboBox.addItems(peaks)

    def setMenuToolsActionsEnabled(self, enabled=True):
        self.actionAnalyzeSpectra.setEnabled(enabled)
        self.actionConfigurePymca.setEnabled(enabled)
        self.actionCalibration.setEnabled(enabled)

    @classmethod
    def offersService(cls, h5Node):
        return isinstance(
            h5Node, (phynx.Entry, phynx.Measurement, phynx.MultiChannelAnalyzer)
        )


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    form = McaAnalysisWindow()
    form.show()
    sys.exit(app.exec_())
