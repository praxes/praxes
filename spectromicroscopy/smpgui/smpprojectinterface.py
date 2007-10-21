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

from spectromicroscopy.smpgui import configuresmp, scananalysis, scancontrols
from spectromicroscopy.smpcore import specrunner, configutils, qtspecscan, \
    qtspecvariable

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SmpProjectInterface(QtGui.QWidget):
    """Establishes a Experimenbt controls 
    Generates Control and Feedback instances
   Addes Scan atributes to specRunner instance 
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        self.gridlayout = QtGui.QGridLayout(self)

        self.specRunner = parent.specRunner

        self.specRunner.scan = \
            qtspecscan.QtSpecScanMcaA(self.specRunner.specVersion)

        self.scanControls = scancontrols.ScanControls(self)
        self.gridlayout.addWidget(self.scanControls,0,0,1,1)

#        self.scanFeedback = scanfeedback.ScanFeedback(self)
#        self.gridlayout.addWidget(self.scanFeedback,0,1,1,1)

        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("newMesh(PyQt_PyObject)"),
                     self.newScanAnalysis2D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newTseries(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newAscan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newA2scan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newA3scan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                     self.setTabLabel)

    def newScanAnalysis(self, newAnalysis):
        self.parent.mainTab.addTab(newAnalysis, '')
        self.parent.mainTab.setCurrentWidget(newAnalysis)
        
#        self.scanFeedbackTab.addAction(self.closeAction)
#        self.scanFeedbackTab.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
#        self.connect(self.closeAction, QtCore.SIGNAL("triggered()"), self.scanFeedbackTab.close)

    def newScanAnalysis1D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis1D(self, scanParams))

    def newScanAnalysis2D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis2D(self, scanParams))

    def setTabLabel(self, scanParams):
        i = self.parent.mainTab.currentIndex()
        self.parent.mainTab.setTabText(i, scanParams['title'])


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = SmpProjectInterface()
    myapp.show()
    sys.exit(app.exec_())
