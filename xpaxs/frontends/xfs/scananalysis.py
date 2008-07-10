"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy
import logging

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore, QtGui
from PyMca.FitParam import FitParamDialog

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.frontends.xfs import elementsview, mcaspectrum
from xpaxs.frontends.xfs.dispatch import XfsDispatcherThread

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.frontends.xfs.ui.scananalysis')


class ScanAnalysis(QtGui.QWidget):

    """
    """

    def __init__(self, scanData, advancedFit=None,  parent=None):
        super(ScanAnalysis, self).__init__(parent)

        self.scanData = scanData
        self._currentMapType = "massFraction"
        self._normalizationChannel = None
        self._peaks = scanData.getAvailableElements()
        if self._peaks: self._currentElement = self._peaks[0]
        else: self._currentElement = None

        self._pymcaConfig = scanData.getPymcaConfig()

        self.advancedFit = advancedFit

        self.createActions()

        self.fitParamDlg = FitParamDialog(parent=self)

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        if self.scanData.getNumScanDimensions() == 2:
            self.elementDataPlot = elementsview.ElementImage(scanData, self)
        else:
            self.elementDataPlot = elementsview.ElementPlot(scanData, self)
        layout.addWidget(self.elementDataPlot)

        self.statusBarWidget = QtGui.QWidget(self)
        # make it fit in the status bar without resizing the status bar
        self.statusBarWidget.setMaximumHeight(17)
        self.statusBarWidget.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                           QtGui.QSizePolicy.Minimum)
        self.progressBar = QtGui.QProgressBar()
        self.processAbortButton = QtGui.QPushButton("Abort")
        label = QtGui.QLabel('analysis in progress:')
        layout = QtGui.QHBoxLayout()
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.addWidget(label)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.processAbortButton)
        self.statusBarWidget.setLayout(layout)
        self.statusBarWidget.hide()

        self.analysisThread = None
        self.isProcessing = False

        self.connect(self, QtCore.SIGNAL("availablePeaks"),
                     self.elementDataPlot.setAvailablePeaks)
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("pickEvent"),
                     self.plotSpectrum)

    def closeEvent(self, event):
        if self.isProcessing:
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
                return event.ignore()

        if self._pymcaConfig: self.scanData.setPymcaConfig(self._pymcaConfig)
        self.scanData.flush()
        self.emit(QtCore.SIGNAL("scanClosed"), self.scanData)
        return event.accept()

    def configurePyMca(self):
        if self._pymcaConfig:
            self.fitParamDlg.setParameters(self._pymcaConfig)
        else:
            self.fitParamDlg.setParameters(self.advancedFit.mcafit.config)
        if self.fitParamDlg.exec_():
            QtGui.qApp.processEvents()
            self.advancedFit.configure(self.fitParamDlg.getParameters())
            self._pymcaConfig = self.advancedFit.mcafit.config
            self.scanData.setPymcaConfig(self._pymcaConfig)

    def createActions(self):
        self.actions = []

        analyzeSpectra = QtGui.QAction('Analyze Spectra', None)
        self.connect(analyzeSpectra,
                     QtCore.SIGNAL("triggered()"),
                     self.processData)
        self.connect(analyzeSpectra,
                     QtCore.SIGNAL("triggered()"),
                     self.disableMenuToolsActions)
        self.actions.append(analyzeSpectra)

        configurePyMca = QtGui.QAction('Configure PyMca', None)
        self.connect(configurePyMca,
                     QtCore.SIGNAL("triggered()"),
                     self.configurePyMca)
        self.actions.append(configurePyMca)

        calibration = QtGui.QAction('Fit Average Spectrum', None)
        self.connect(calibration,
                     QtCore.SIGNAL("triggered()"),
                     lambda: self.plotSpectrum(None))
        self.actions.append(calibration)

    def disableMenuToolsActions(self):
        for action in self.actions:
            action.setEnabled(False)

    def elementMapUpdated(self):
        self.emit(QtCore.SIGNAL("elementDataChanged"), self.getElementMap())

    def enableMenuToolsActions(self):
        for action in self.actions:
            action.setEnabled(True)

    def getElementMap(self, mapType=None, element=None, normalization=None):
        if element is None: element = self._currentElement
        if mapType is None: mapType = self._currentMapType
        if normalization is None: normalization = self._normalizationChannel

        if mapType and element:
            return self.scanData.getElementMap(mapType, element, normalization)
        else:
            return numpy.zeros(self.scanData.getScanShape(), dtype='f')

    def getMenuToolsActions(self):
        return self.actions

    def getPeaks(self):
        return copy.deepcopy(self._peaks)

    def plotSpectrum(self,indices):
        if self._pymcaConfig is not self.advancedFit.mcafit.config:
            if not self._pymcaConfig:
                self.configurePyMca()
            else:
                self.advancedFit.configure(self._pymcaConfig)
                self._pymcaConfig = self.advancedFit.mcafit.config

        indices = self.scanData.getValidDataPoints(indices)

        if not indices: return

        counts = self.scanData.getAverageMcaSpectrum(indices,
                                    normalization=self._normalizationChannel)
        channels = self.scanData.getMcaChannels()

        self.advancedFit.setData(x=channels, y=counts)
        self.advancedFit.fit()

    def processComplete(self):
        self.statusBarWidget.hide()
        self.progressBar.reset()
        self.isProcessing = False
        self.analysisThread = None
        self.emit(QtCore.SIGNAL("removeStatusBarWidget"), self.statusBarWidget)

    def processData(self):
        self.configurePyMca()

        self.resetPeaks()

        config = copy.deepcopy(self._pymcaConfig)
        thread = XfsDispatcherThread(parent=self)
        thread.setData(self.scanData, config)
        self.scanData.setQueue(thread.getQueue())

        self.connect(thread,
                     QtCore.SIGNAL('dataProcessed'),
                     self.elementMapUpdated)
        self.connect(thread,
                     QtCore.SIGNAL('ppJobStats'),
                     self,
                     QtCore.SIGNAL("ppJobStats"))
        self.connect(thread, QtCore.SIGNAL("finished()"),
                     self.elementMapUpdated)
        self.connect(thread, QtCore.SIGNAL("finished()"),
                     self.enableMenuToolsActions)
        self.connect(thread, QtCore.SIGNAL("finished()"),
                     thread, QtCore.SLOT("deleteLater()"))
        self.connect(thread, QtCore.SIGNAL("finished()"),
                     self.processComplete)
        self.connect(thread, QtCore.SIGNAL('percentComplete'),
                     self.progressBar.setValue)
        self.connect(self.processAbortButton,
                     QtCore.SIGNAL('clicked(bool)'),
                     thread.stop)

        self.isProcessing = True
        self.emit(QtCore.SIGNAL("addStatusBarWidget"), self.statusBarWidget)
        self.statusBarWidget.show()

        self.analysisThread = thread

        thread.start(QtCore.QThread.NormalPriority)

    def resetPeaks(self):
        self._peaks = []

        if self._pymcaConfig:
            for el, edges in self._pymcaConfig['peaks'].iteritems():
                for edge in edges:
                    name = ' '.join([el, edge])
                    self._peaks.append(name)
            self._peaks.sort()
            if self._currentElement is None and len(self._peaks) > 0:
                self._currentElement = self._peaks[0].replace(' ', '')

        self.scanData.initializeElementMaps(self._peaks)

        self.emit(QtCore.SIGNAL("availablePeaks"),
                  copy.deepcopy(self._peaks))

    def setCurrentElement(self, element):
        element = str(element).replace(' ', '')
        if not self._currentElement == element:
            self._currentElement = element
            self.emit(QtCore.SIGNAL("elementDataChanged"), self.getElementMap())

    def setCurrentMapType(self, mapType):
        mapType = str(mapType).replace(' ', '')
        if not self._currentMapType == mapType:
            self._currentMapType = mapType[0].lower() + mapType[1:]
            self.emit(QtCore.SIGNAL("elementDataChanged"), self.getElementMap())

    def setNormalizationChannel(self, channel):
        channel = str(channel)
        if channel == 'None': channel = None
        if not self._normalizationChannel == channel:
            self._normalizationChannel = channel
            self.emit(QtCore.SIGNAL("elementDataChanged"), self.getElementMap())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanAnalysis
    sys.exit(app.exec_())
