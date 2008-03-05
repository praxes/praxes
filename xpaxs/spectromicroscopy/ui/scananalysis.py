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
        self.createActions()

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        if self.controller.getScanDimensions() == 2:
            self.elementDataPlot = elementsview.ElementImage(controller, self)
        else:
            self.elementDataPlot = elementsview.ElementPlot(controller, self)
        layout.addWidget(self.elementDataPlot)

    def createActions(self):
        self.actions = []
        analyzeSpectra = QtGui.QAction('Analyze Spectra', None)
        self.connect(analyzeSpectra,
                     QtCore.SIGNAL("triggered()"),
                     self.controller.processData)
        self.connect(analyzeSpectra,
                     QtCore.SIGNAL("triggered()"),
                     self.disableMenuToolsActions)
        self.connect(self.controller,
                     QtCore.SIGNAL("finished()"),
                     self.enableMenuToolsActions)
        self.actions.append(analyzeSpectra)

    def getMenuToolsActions(self):
        return self.actions

    def enableMenuToolsActions(self):
        for action in self.actions:
            action.setEnabled(True)

    def disableMenuToolsActions(self):
        for action in self.actions:
            action.setEnabled(False)



# TODO: update the window title
#    def setWindowLabel(self, scanParams):
#        temp = scanParams['datafile']
#        temp = temp.rstrip('.dat').rstrip('.txt').rstrip('.mca')
#        label = ' '.join([temp, scanParams['title']])
#        i = self.parent.mainTab.currentIndex()
#        self.parent.mainTab.setTabText(i, label)
