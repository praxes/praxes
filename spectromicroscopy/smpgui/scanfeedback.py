"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import gc

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import scananalysis

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanFeedback(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName("gridlayout")

        self.scanFeedbackTab = SmpTabWidget(self)
        self.scanFeedbackTab.setObjectName("scanFeedbackTab")
        self.gridlayout.addWidget(self.scanFeedbackTab,0,0,1,1)
        
        self.specRunner = parent.specRunner
        
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
        
#        self.closeAction = QtGui.QAction('&Close', self)

#    def __handleTabContextMenuRequested(self, point):
#        """
#        Private slot to handle the context menu request for the tabbar.
#        
#        @param point point the context menu was requested (QPoint)
#        """
#        _tabbar = self.tabBar()
#        for index in range(_tabbar.count()):
#            rect = _tabbar.tabRect(index)
#            if rect.contains(point):
#                self.emit(SIGNAL("customTabContextMenuRequested(const QPoint &, int)"), 
#                          _tabbar.mapToParent(point), index)
#                break

    def newScanAnalysis(self, newAnalysis):
        self.scanFeedbackTab.addTab(newAnalysis, '')
        self.scanFeedbackTab.setCurrentWidget(newAnalysis)
        
#        self.scanFeedbackTab.addAction(self.closeAction)
#        self.scanFeedbackTab.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
#        self.connect(self.closeAction, QtCore.SIGNAL("triggered()"), self.scanFeedbackTab.close)

    def newScanAnalysis1D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis1D(self, scanParams))

    def newScanAnalysis2D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis2D(self, scanParams))

    def setTabLabel(self, scanParams):
        i = self.scanFeedbackTab.currentIndex()
        self.scanFeedbackTab.setTabText(i, scanParams['title'])
