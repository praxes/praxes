"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import ui_scananalysis, elementsdata, \
    mcaspectrum, mplwidgets,elementsplot
from spectromicroscopy.smpcore import advancedfitanalysis

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanAnalysis(ui_scananalysis.Ui_ScanAnalysis, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setEnabled(False)
        
        self.specRunner = parent.specRunner
        self.scanAnalysis = None

        self.mcaSpectrumPlot = mcaspectrum.McaSpectrum()
        self.gridlayout.addWidget(self.mcaSpectrumPlot, 0, 0, 1, 1)
        
        self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.splitter.setCursor(QtCore.Qt.SplitVCursor)
        self.gridlayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.splitter.addWidget(self.mcaSpectrumPlot)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("scanFinished()"),
                     self.disconnectSignals)
        
    def connectSignals(self):
        self.connect(self.elementDataPlot.dataTypeBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.scanAnalysis.setCurrentDataType)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                     self.elementDataPlot.updateFigure)
        self.connect(self.elementDataPlot.saveDataPushButton,
                     QtCore.SIGNAL("clicked()"),
                     self.saveData)
        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"),
                     self.scanAnalysis.newDataPoint)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"),
                     self.mcaSpectrumPlot.updateFigure)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                     self.elementDataPlot.xrfbandComboBox.addItems)
        self.connect(self.elementDataPlot.xrfbandComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.scanAnalysis.setCurrentElement)
        self.connect(self.scanAnalysis,
                     QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                     self.setEnabled)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                     self.scanAnalysis.setSuggestedFilename)
        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("xAxisLabel(PyQt_PyObject)"),
                     self.elementDataPlot.setXLabel)
        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("xAxisLims(PyQt_PyObject)"),
                     self.elementDataPlot.setXLims)
        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("yAxisLabel(PyQt_PyObject)"),
                     self.elementDataPlot.setYLabel)
        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("yAxisLims(PyQt_PyObject)"),
                     self.elementDataPlot.setYLims)
    
    def disconnectSignals(self):
        # workaround to process last data point, reported after scanFinished 
        # signal is emitted:
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"),
                     self._disconnect)

    def _disconnect(self, *args):
        self.window().scanIO.scanControls.skipModeCheckBox.setEnabled(True)
        self.disconnect(self.scanAnalysis, 
                        QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"),
                        self.disconnect)
        self.disconnect(self.specRunner.scan, 
                        QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"),
                        self.scanAnalysis.newDataPoint)
        self.disconnect(self.scanAnalysis, 
                        QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"),
                        self.mcaSpectrumPlot.updateFigure)
        self.disconnect(self.scanAnalysis, 
                        QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                        self.elementDataPlot.xrfbandComboBox.addItems)
        self.disconnect(self.scanAnalysis,
                        QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                        self.setEnabled)
        self.disconnect(self.specRunner.scan,
                        QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                        self.scanAnalysis.setSuggestedFilename)
        self.disconnect(self.specRunner.scan, 
                        QtCore.SIGNAL("xAxisLabel(PyQt_PyObject)"),
                        self.elementDataPlot.setXLabel)
        self.disconnect(self.specRunner.scan, 
                        QtCore.SIGNAL("xAxisLims(PyQt_PyObject)"),
                        self.elementDataPlot.setXLims)
        self.disconnect(self.specRunner.scan, 
                        QtCore.SIGNAL("yAxisLabel(PyQt_PyObject)"),
                        self.elementDataPlot.setYLabel)
        self.disconnect(self.specRunner.scan, 
                        QtCore.SIGNAL("yAxisLims(PyQt_PyObject)"),
                        self.elementDataPlot.setYLims)

    def saveData(self):
        filename = self.scanAnalysis.getSuggestedFilename()
        filename = QtGui.QFileDialog.getSaveFileName(self,
                        'Save Element Data File', filename, 
                        'EDF files (*.edf);;Plaintext files (*.dat *.txt *.*)')
        filename = str(filename)
        if filename:
            self.scanAnalysis.saveData(filename)

    def loadPymcaConfigFile(self):
        configFile = self.window().pymcaConfigFile
        self.scanAnalysis.loadPymcaConfig(configFile)


class ScanAnalysis1D(ScanAnalysis):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None, scanParams={}):
        ScanAnalysis.__init__(self, parent)

        self.scanAnalysis = \
            advancedfitanalysis.AdvancedFitAnalysis1D(scanParams)
        
        self.elementDataPlot = elementsplot.ElementsPlot()
        self.gridlayout.addWidget(self.elementDataPlot, 2, 0, 1, 1)
        self.splitter.addWidget(self.elementDataPlot)
        
        self.connectSignals()
        self.loadPymcaConfigFile()
        
    def connectSignals(self):
        ScanAnalysis.connectSignals(self)


class ScanAnalysis2D(ScanAnalysis):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None, scanParams={}):
        ScanAnalysis.__init__(self, parent)
        
        self.scanAnalysis = \
            advancedfitanalysis.AdvancedFitAnalysis2D(scanParams)
        
        self.elementDataPlot = elementsdata.ElementsData()
        self.gridlayout.addWidget(self.elementDataPlot, 2, 0, 1, 1)
        self.splitter.addWidget(self.elementDataPlot)

        self.connectSignals()
        self.loadPymcaConfigFile()

    def connectSignals(self):
        ScanAnalysis.connectSignals(self)
        self.connect(self.elementDataPlot.aspectSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setImageAspect)
