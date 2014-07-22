"""
"""

from __future__ import absolute_import, with_statement

import copy
#import gc
#import logging
import posixpath
import Queue
import sys

from PyQt4 import QtCore, QtGui
from PyMca5.PyMcaGui.physics.xrf.FitParam import FitParamDialog
import numpy as np

from praxes.frontend.analysiswindow import AnalysisWindow
from .ui.ui_mcaanalysiswindow import Ui_McaAnalysisWindow
from .elementsview import ElementsView
from .results import XRFMapResultProxy
from praxes.io import phynx

#logger = logging.getLogger(__file__)


class McaAnalysisWindow(Ui_McaAnalysisWindow, AnalysisWindow):

    """
    """

    @property
    def n_points(self):
        return self._n_points

    # TODO: this should eventually take an MCA entry
    def __init__(self, scan_data, parent=None):
        super(McaAnalysisWindow, self).__init__(parent)

        self.analysisThread = None

        with scan_data:
            if isinstance(scan_data, phynx.Entry):
                self.scan_data = scan_data.entry.measurement
            elif isinstance(scan_data, phynx.Measurement):
                self.scan_data = scan_data
            elif isinstance(scan_data, phynx.MultiChannelAnalyzer):
                self.scan_data = scan_data
            else:
                with scan_data:
                    raise TypeError(
                        'H5 node type %s not recognized by McaAnalysisWindow'
                        % scan_data.__class__.__name__
                    )
            self._n_points = scan_data.entry.npoints
            self._dirty = False
            self._results = XRFMapResultProxy(self.scan_data)

            pymcaConfig = self.scan_data.pymca_config
            self.setupUi(self)

            title = '%s: %s: %s'%(
                posixpath.split(scan_data.file.file_name)[-1],
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
            except KeyError:
                self.deadTimeReport.setText('Not found')

            self._setupMcaDockWindows()
            self._setupJobStats()

            plotOptions = self.elementsView.plotOptions
            self.optionsWidgetVLayout.insertWidget(1, plotOptions)

            self.elementsView.pickEvent.connect(self.processAverageSpectrum)
            # TODO: remove the window from the list of open windows when we close
    #           self.scanView.scanClosed.connect(self.scanClosed)

            self.fitParamDlg = FitParamDialog(parent=self)

            if pymcaConfig:
                self.fitParamDlg.setParameters(pymcaConfig)
                self.spectrumAnalysis.configure(pymcaConfig)
            else:
                self.configurePymca()

            try:
                mca = self.scan_data.entry.measurement.mcas.values()[0]
                eff = mca.monitor.efficiency
                self.monitorEfficiency.setText(str(eff))
                self.monitorEfficiency.setEnabled(True)
            except AttributeError:
                pass

            self.progressBar = QtGui.QProgressBar(self)
            self.progressBar.setMaximumHeight(17)
            self.progressBar.hide()
            self.progressBar.addAction(self.actionAbort)
            self.progressBar.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

            self.progress_queue = Queue.Queue()
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.elementMapUpdated)

            self.elementsView.updateFigure()

            self._restoreSettings()

    @property
    def availableElements(self):
        with self.scan_data:
            try:
                return sorted(
                    self.scan_data['element_maps'].fits.keys()
                    )
            except KeyError:
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
        from PyMca5.PyMcaGui.physics.xrf.ConcentrationsWidget import Concentrations

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

    def _setupJobStats(self):
        from praxes.dispatch.jobstats import JobStats

        self.jobStats = JobStats()
        self.jobStatsDock = self._createDockWindow('JobStatsDock')
        self._setupDockWindow(self.jobStatsDock,
                               QtCore.Qt.RightDockWidgetArea,
                               self.jobStats, 'Analysis Server Stats')

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
        with self.scan_data:
            try:
                value = float(self.monitorEfficiency.text())
                assert (0 < value <= 1)
                for mca in self.scan_data.entry.measurement.mcas.values():
                    mca.monitor.efficiency = value
            except (ValueError, AssertionError):
                mca = self.scan_data.entry.measurement.mcas.values()[0]
                self.monitorEfficiency.setText(
                    str(mca.monitor.efficiency)
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
                    #QtGui.qApp.processEvents()
            else:
                event.ignore()
                return

        AnalysisWindow.closeEvent(self, event)
        event.accept()

    def configurePymca(self):
        if self.fitParamDlg.exec_():
            #QtGui.qApp.processEvents()

            self.statusbar.showMessage('Reconfiguring PyMca ...')
            configDict = self.fitParamDlg.getParameters()
            self.spectrumAnalysis.configure(configDict)
            with self.scan_data:
                self.scan_data.pymca_config = configDict
            self.statusbar.clearMessage()

    def elementMapUpdated(self):
        if self._dirty:
            self._dirty = False
            self.elementsView.updateFigure(self.getElementMap())
        #QtGui.qApp.processEvents()

    def getElementMap(self, mapType=None, element=None):
        if element is None: element = self.xrfBand
        if mapType is None: mapType = self.mapType

        if mapType and element:
            try:
                return self._results.get(element, mapType)
            except KeyError:
                return np.zeros(self.scan_data.entry.acquisition_shape)
        else:
            with self.scan_data:
                return np.zeros(
                    self.scan_data.entry.acquisition_shape, dtype='f'
                    )

    def initializeElementMaps(self, elements):
        self._results = XRFMapResultProxy(self.scan_data, elements)

    def processAverageSpectrum(self, indices=None):
        with self.scan_data:
            if indices is None:
                indices = np.arange(self.scan_data.entry.acquired)
            n_indices = len(indices)
            if n_indices:
                masked = self.scan_data.entry.measurement.masked[...][indices]
                indices = indices[np.logical_not(masked)]
                n_indices = len(indices)

            if not n_indices:
                return

            self.statusbar.showMessage('Averaging spectra ...')

            try:
                # looking at individual element
                monitor = self.scan_data.monitor.corrected_value
                mon0 = monitor[indices[0]]
                channels = self.scan_data.channels
                counts = channels.astype('float32') * 0
                dataset = self.scan_data['counts'].corrected_value
                for i in indices:
                    counts += dataset[i] / n_indices / (monitor[i]/mon0)
            except AttributeError:
                # looking at multiple elements
                mcas = self.scan_data.mcas.values()
                monitor = mcas[0].monitor.corrected_value
                mon0 = monitor[indices[0]]
                channels = mcas[0].channels
                counts = channels.astype('float32') * 0
                for mca in mcas:
                    dataset = mca['counts'].corrected_value
                    for i in indices:
                        counts += dataset[i] / n_indices / (monitor[i]/mon0)

            self.spectrumAnalysis.setData(x=channels, y=counts)
            self.statusbar.showMessage('Performing Fit ...')
            self.spectrumAnalysis.mcafit.config['concentrations']['flux'] = mon0
            self.spectrumAnalysis.mcafit.config['concentrations']['time'] = 1
            fitresult = self.spectrumAnalysis.fit()

            self.fitParamDlg.setFitResult(fitresult['result'])

            self.statusbar.clearMessage()

        self.setMenuToolsActionsEnabled(True)

    def processComplete(self):
        self.progressBar.hide()
        self.progressBar.reset()
        self.statusbar.removeWidget(self.progressBar)
        self.statusbar.clearMessage()
        self.timer.stop()

        self.analysisThread = None

        self.setMenuToolsActionsEnabled(True)
        self.elementMapUpdated()
        self._results.flush()

    def processData(self):
        from .mptaskmanager import XfsTaskManager

        self.setMenuToolsActionsEnabled(False)

        self._resetPeaks()

        settings = QtCore.QSettings()
        settings.beginGroup('JobServers')
        n_local_processes, ok = settings.value(
            'LocalProcesses', QtCore.QVariant(1)
            ).toInt()

        thread = XfsTaskManager(
            self.scan_data,
            copy.deepcopy(self.pymcaConfig),
            self._results,
            n_local_processes=n_local_processes
            )

        thread.progress_report.connect(self.update)
        thread.finished.connect(self.processComplete)
        self.actionAbort.triggered.connect(thread.stop) #thread.stop

        self.statusbar.showMessage('Analyzing spectra ...')
        self.statusbar.addPermanentWidget(self.progressBar)
        self.progressBar.show()

        self.analysisThread = thread

        thread.start()
        self.timer.start(1000)

    def update(self, report):
        self._dirty = True

        n_processed = report.pop('n_processed')
        with self.scan_data:
            n_points = self.scan_data.entry.npoints
        progress = int((100.0 * n_processed) / n_points)
        self.progressBar.setValue(progress)
#        self.jobStats.updateTable(item)

    def _resetPeaks(self):
        peaks = []

        for el, edges in self.pymcaConfig['peaks'].items():
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
        if isinstance(
            h5Node, (phynx.Entry, phynx.Measurement, phynx.MultiChannelAnalyzer)
            ):
            return len(h5Node.entry.measurement.mcas) > 0
        return False


#if __name__ == "__main__":
#    import sys
#    app = QtGui.QApplication(sys.argv)
#    app.setOrganizationName('Praxes')
#    form = McaAnalysisWindow()
#    form.show()
#    sys.exit(app.exec_())
