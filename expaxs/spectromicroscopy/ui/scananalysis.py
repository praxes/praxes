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

# TODO: update the window title
#    def setWindowLabel(self, scanParams):
#        temp = scanParams['datafile']
#        temp = temp.rstrip('.dat').rstrip('.txt').rstrip('.mca')
#        label = ' '.join([temp, scanParams['title']])
#        i = self.parent.mainTab.currentIndex()
#        self.parent.mainTab.setTabText(i, label)
