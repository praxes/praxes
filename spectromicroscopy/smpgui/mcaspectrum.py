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

from spectromicroscopy.smpgui import ui_mcaspectrum, mplwidgets

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class McaSpectrum(ui_mcaspectrum.Ui_McaSpectrum, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        self.mcaSpectrumPlot = mplwidgets.McaSpectrum(self)
        self.mcaSpectrumPlot.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                           QtGui.QSizePolicy.Expanding)
#        self.mcaSpectrumPlot.setMaximumHeight(220)
        self.gridlayout2.addWidget(self.mcaSpectrumPlot, 0, 0, 1, 1)
        self.mcaToolbar = mplwidgets.Toolbar(self.mcaSpectrumPlot, self)
        self.gridlayout2.addWidget(self.mcaToolbar, 1, 0, 1, 1)
        
        self.connect(self.mcaLogscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.mcaSpectrumPlot.enableLogscale)
        self.connect(self.mcaAutoscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.mcaSpectrumPlot.enableAutoscale)

    def __getattr__(self, attr):
        return getattr(self.mcaSpectrumPlot, attr)
