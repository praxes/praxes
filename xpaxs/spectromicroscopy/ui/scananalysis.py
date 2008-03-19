"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore, QtGui
from PyMca.FitParam import FitParamDialog

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.spectromicroscopy.ui import elementsview, mcaspectrum
from xpaxs.spectromicroscopy.advancedfitanalysis import AdvancedFitThread

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanAnalysis(QtGui.QWidget):

    """
    """

    def __init__(self, scanData, parent=None, advancedFit=None):
        super(ScanAnalysis, self).__init__(parent)

        self.scanData = scanData
        self._currentMapType = "massFraction"
        self._normalizationChannel = None
        self._peaks = scanData.getAvailableElements()
        if self._peaks: self._currentElement = self._peaks[0]
        else: self._currentElement = None
        try:
            self._pymcaConfig = scanData.getPymcaConfig()
        except:
            self._pymcaConfig = None

        self.advancedFit = advancedFit

        self.createActions()

        self.fitParamDlg = FitParamDialog()

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        if self.scanData.getNumScanDimensions() == 2:
            self.elementDataPlot = elementsview.ElementImage(scanData, self)
        else:
            self.elementDataPlot = elementsview.ElementPlot(scanData, self)
        layout.addWidget(self.elementDataPlot)

        self.connect(self, QtCore.SIGNAL("availablePeaks"),
                     self.elementDataPlot.setAvailablePeaks)
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("pickEvent"),
                     self.plotSpectrum)

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

    def disableMenuToolsActions(self):
        for action in self.actions:
            action.setEnabled(False)

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

    def configurePyMca(self):
        self.fitParamDlg.exec_()
        self._pymcaConfig = self.fitParamDlg.getParameters()
        self.scanData.setPymcaConfig(self._pymcaConfig)

#    def launchMcaAdvancedFit(self):
#        dialog = QtGui.QDialog()
#        layout = QtGui.QVBoxLayout(dialog)
#        from PyMca import McaAdvancedFit
#        mcaFit = McaAdvancedFit.McaAdvancedFit(dialog)
#        mcaFit.mcafit.configure(self.specInterface.pymcaConfig)
#        x = self.figure.fitData['xdata'].flatten()
#        y = self.figure.mcaCountsSummed.flatten()/self.figure.numSpectra
#        mcaFit.setData(x=x, y=y)
#        layout.addWidget(mcaFit)
#        dialog.exec_()

    def plotSpectrum(self, index):
        if self._pymcaConfig is None:
            self.configurePyMca()

        channels = self.scanData.getMcaChannels()
        counts = self.scanData.getMcaSpectrum(index)
        config = self._pymcaConfig

        if self.advancedFit:
            # We are using PyMca's AdvancedFit
            self.advancedFit.configure(config)
            self.advancedFit.setData(x=channels, y=counts)
            self.advancedFit.fit()
        else:
            self.emit(QtCore.SIGNAL("analyzeSpectrum"),
                      channels, counts, config)


    def processData(self):
        if self._pymcaConfig is None:
            self.configurePyMca()

        self.resetPeaks()

        config = copy.deepcopy(self._pymcaConfig)

        thread = AdvancedFitThread(self.scanData, config, self)
        queue = thread.getQueue()

        self.connect(thread,
                     QtCore.SIGNAL('dataProcessed'),
                     self.elementMapUpdated)
        self.connect(thread, QtCore.SIGNAL("finished()"),
                     self.elementMapUpdated)
        self.connect(thread, QtCore.SIGNAL("finished()"),
                     self.enableMenuToolsActions)
        self.connect(thread, QtCore.SIGNAL("finished()"),
                     thread, QtCore.SLOT("deleteLater()"))

        thread.start(QtCore.QThread.NormalPriority)

        return queue

    def resetPeaks(self):
        self._peaks = []

        if self._pymcaConfig:
            for el, edges in self._pymcaConfig['peaks'].iteritems():
                for edge in edges:
                    name = ' '.join([el, edge])
                    self._peaks.append(name)
            self._peaks.sort()
            if self._currentElement is None:
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

    def elementMapUpdated(self):
        self.emit(QtCore.SIGNAL("elementDataChanged"), self.getElementMap())

# TODO: update the window title
#    def setWindowLabel(self, scanParams):
#        temp = scanParams['datafile']
#        temp = temp.rstrip('.dat').rstrip('.txt').rstrip('.mca')
#        label = ' '.join([temp, scanParams['title']])
#        i = self.parent.mainTab.currentIndex()
#        self.parent.mainTab.setTabText(i, label)
