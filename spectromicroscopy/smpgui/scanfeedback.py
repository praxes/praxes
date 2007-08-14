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

from spectromicroscopy.smpgui import ui_scanfeedback,  mplwidgets
from spectromicroscopy.smpcore import advancedfitanalysis

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanFeedback(ui_scanfeedback.Ui_ScanFeedback, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        self.scanAnalysis = None
        
        self.specRunner = parent.specRunner

        self.mcaSpectrumPlot = mplwidgets.McaSpectrum(self)
        self.mcaSpectrumPlot.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                           QtGui.QSizePolicy.Fixed)
        self.mcaSpectrumPlot.setMaximumHeight(200)
        self.gridlayout3.addWidget(self.mcaSpectrumPlot, 0, 0, 1, 1)
        self.mcaToolbar = mplwidgets.Toolbar(self.mcaSpectrumPlot, self)
        self.gridlayout3.addWidget(self.mcaToolbar, 1, 0, 1, 1)
        
        self.elementImagePlot = mplwidgets.ElementImage(self)
        self.gridlayout5.addWidget(self.elementImagePlot, 0, 0, 1, 1)
        self.imageToolbar = mplwidgets.Toolbar(self.elementImagePlot, self)
        self.gridlayout5.addWidget(self.imageToolbar, 1, 0, 1, 1)
        
        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("newMesh(PyQt_PyObject)"),
                     self.newScanAnalysis2D)
        self.connect(self.logscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.mcaSpectrumPlot.setLogScale)
        

    def newScanAnalysis2D(self, scanParams):
        #TODO: use scanParams to set axis labels, ranges, etc
        self.scanAnalysis = \
            advancedfitanalysis.AdvancedFitAnalysis2D(scanParams)
        
        #TODO: load users pymcaconfig, if selected
        self.scanAnalysis.loadPymcaConfig()
        
        self.saveImagePushButton.setEnabled(False)
        self.xrfbandComboBox.clear()
        self.mcaSpectrumPlot.clear()
        self.elementImagePlot.clear()
        
        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"),
                     self.scanAnalysis.newDataPoint)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"),
                     self.mcaSpectrumPlot.updateFigure)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                     self.xrfbandComboBox.addItem)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("elementImageChanged(PyQt_PyObject)"),
                     self.elementImagePlot.updateFigure)
        self.connect(self.xrfbandComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.scanAnalysis.setCurrentElement)
        self.connect(self.scanAnalysis,
                     QtCore.SIGNAL("enableSaveImageButton(PyQt_PyObject)"),
                     self.saveImagePushButton.setEnabled)
        self.connect(self.saveImagePushButton,
                     QtCore.SIGNAL("clicked()"),
                     self.saveData)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                     self.scanAnalysis.setSuggestedFilename)
    
    def saveData(self):
        filename = self.scanAnalysis.getSuggestedFilename()
        filename = QtGui.QFileDialog.getSaveFileName(self,
                        'Save Element Data File', filename, 
                        'EDF files (*.edf);;Plaintext files (*.dat *.txt *.*)')
        filename = str(filename)
        if filename:
            self.scanAnalysis.saveData(filename)
