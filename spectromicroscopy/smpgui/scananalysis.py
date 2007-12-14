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

from spectromicroscopy.smpgui import elementsview, mcaspectrum

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanAnalysis(QtGui.QWidget):

    """
    """
    
    def __init__(self, scan, parent=None):
        super(ScanAnalysis, self).__init__(parent)
        
        self.scan = scan

        self.mcaSpectrumPlot = mcaspectrum.McaSpectrum(scan)
        
        layout = QtGui.QVBoxLayout()
        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        layout.addWidget(splitter)
        self.setLayout(layout)
        splitter.addWidget(self.mcaSpectrumPlot)
        
        if self.scan.getScanType() == '2D':
            self.elementDataPlot = elementsview.ElementImage(scan)
            splitter.addWidget(self.elementDataPlot)
        else:
            self.elementDataPlot = elementsview.ElementPlot(scan)
            splitter.addWidget(self.elementDataPlot)

