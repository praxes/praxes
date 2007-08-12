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

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanFeedback(ui_scanfeedback.Ui_ScanFeedback, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
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
                     QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"),
                     self.mcaSpectrumPlot.update_figure)
