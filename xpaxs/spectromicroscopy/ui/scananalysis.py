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
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.spectromicroscopy.ui import elementsview, mcaspectrum

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanAnalysis(QtGui.QWidget):

    """
    """

    def __init__(self, controller, parent=None):
        super(ScanAnalysis, self).__init__(parent)

        self.controller = controller

        self.mcaSpectrumPlot = mcaspectrum.McaSpectrum(controller)

        layout = QtGui.QVBoxLayout()
        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        layout.addWidget(splitter)
        self.setLayout(layout)
        splitter.addWidget(self.mcaSpectrumPlot)

        if self.controller.getScanDimensions() == 2:
            self.elementDataPlot = elementsview.ElementImage(controller)
            splitter.addWidget(self.elementDataPlot)
        else:
            self.elementDataPlot = elementsview.ElementPlot(controller)
            splitter.addWidget(self.elementDataPlot)

#        self.controller.processData()

# TODO: update the window title
#    def setWindowLabel(self, scanParams):
#        temp = scanParams['datafile']
#        temp = temp.rstrip('.dat').rstrip('.txt').rstrip('.mca')
#        label = ' '.join([temp, scanParams['title']])
#        i = self.parent.mainTab.currentIndex()
#        self.parent.mainTab.setTabText(i, label)
