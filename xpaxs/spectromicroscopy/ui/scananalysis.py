"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

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

    def __init__(self, scan, parent=None):
        super(ScanAnalysis, self).__init__(parent)

        self.scan = scan
        self.createActions()

        self._pymcaConfig = None
        self.fitParamDlg = FitParamDialog()

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        if self.controller.getScanDimensions() == 2:
            self.elementDataPlot = elementsview.ElementImage(controller, self)
        else:
            self.elementDataPlot = elementsview.ElementPlot(controller, self)
        layout.addWidget(self.elementDataPlot)

        self.fitThread = AdvancedFitThread(scan)

    def createActions(self):
        self.actions = []
        analyzeSpectra = QtGui.QAction('Analyze Spectra', None)
        self.connect(analyzeSpectra,
                     QtCore.SIGNAL("triggered()"),
                     self.processData)
        self.connect(analyzeSpectra,
                     QtCore.SIGNAL("triggered()"),
                     self.disableMenuToolsActions)
        self.connect(self.fitThread,
                     QtCore.SIGNAL("finished()"),
                     self.enableMenuToolsActions)
        self.connect(self.fitThread,
                     QtCore.SIGNAL('dataProcessed'),
                     self.dataUpdated)
        self.actions.append(analyzeSpectra)

    def getElementMap(self, mapType=None, element=None, normalization=None):
        if element is None: element = self._currentElement
        if maptype is None: maptype = self._currentDataType
        if normalization is None: normalization = self._normalizationChannel

        return self.scan.getElementMap(mapType, element, normalization)


    def getMenuToolsActions(self):
        return self.actions

    def getPymcaConfig(self):
        self.fitParamDlg.exec_()
        self._pymcaConfig = self.fitParamDlg.getParameters()
        self.scan.resetPeaks(self._pymcaConfig['peaks'])

    def enableMenuToolsActions(self):
        for action in self.actions:
            action.setEnabled(True)

    def disableMenuToolsActions(self):
        for action in self.actions:
            action.setEnabled(False)

    def processData(self):
        if self._pymcaConfig is None: self.getPymcaConfig()

        config = copy.deepcopy(self._pymcaConfig)

        self.fitThread.initialize(config, self.scan)
        thread.start(QtCore.QThread.NormalPriority)

    def setCurrentElement(self, element):
        element = str(element).replace(' ', '')
        if not self._currentElement == element:
            self._currentElement = element
            self.emit(QtCore.SIGNAL("elementDataChanged"), self.getElementMap())

    def setCurrentMapType(self, maptype):
        datatype = str(datatype).replace(' ', '')
        if not self._currentDataType == datatype:
            self._currentDataType = datatype
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
