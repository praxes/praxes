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

from spectromicroscopy.smpgui import ui_scananalysis, mplwidgets
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
        
        self.mcaSpectrumPlot = mplwidgets.McaSpectrum(self)
        self.mcaSpectrumPlot.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                           QtGui.QSizePolicy.Expanding)
#        self.mcaSpectrumPlot.setMaximumHeight(220)
        self.gridlayout2.addWidget(self.mcaSpectrumPlot, 0, 0, 1, 1)
        self.mcaToolbar = mplwidgets.Toolbar(self.mcaSpectrumPlot, self)
        self.gridlayout2.addWidget(self.mcaToolbar, 1, 0, 1, 1)

    def connectSignals(self):
        self.connect(self.mcaLogscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.mcaSpectrumPlot.enableLogscale)
        self.connect(self.mcaAutoscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.mcaSpectrumPlot.enableAutoscale)
        self.connect(self.saveDataPushButton,
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
                     self.xrfbandComboBox.addItems)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                     self.elementDataPlot.updateFigure)
        self.connect(self.xrfbandComboBox,
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
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("dataMax(PyQt_PyObject)"),
                     self.maxSpinBox.setValue)
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("dataMin(PyQt_PyObject)"),
                     self.minSpinBox.setValue)
        self.connect(self.maxSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setDataMax)
        self.connect(self.minSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setDataMin)
        self.connect(self.dataAutoscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.elementDataPlot.enableAutoscale)

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
        
        self.connectSignals()
        self.loadPymcaConfigFile()


class ScanAnalysis2D(ScanAnalysis):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None, scanParams={}):
        ScanAnalysis.__init__(self, parent)
        
        self.scanAnalysis = \
            advancedfitanalysis.AdvancedFitAnalysis2D(scanParams)

        self.elementDataPlot = mplwidgets.ElementImage(self)
        self.gridlayout4.addWidget(self.elementDataPlot, 0, 0, 1, 1)
        self.elementToolbar = mplwidgets.Toolbar(self.elementDataPlot, self)
        self.gridlayout4.addWidget(self.elementToolbar, 1, 0, 1, 1)

        self.connectSignals()
        self.loadPymcaConfigFile()

    def connectSignals(self):
        ScanAnalysis.connectSignals(self)
        self.connect(self.aspectSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setImageAspect)
