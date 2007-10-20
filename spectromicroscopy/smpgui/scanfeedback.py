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


class SmpTabWidget(QtGui.QTabWidget):

    def __init__(self, parent=None):
        QtGui.QTabWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        
        self.__initMenu()
        self.contextMenuEditor = None
        self.contextMenuIndex = -1
        
        self.setTabContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL('customTabContextMenuRequested(const QPoint &, int)'),
                     self.__showContextMenu)

    def __initMenu(self):
        """
        Private method to initialize the tab context menu.
        """
        self.__menu = QtGui.QMenu(self)
        self.__menu.addAction('Save As...', self.__contextMenuSaveAs)
        self.__menu.addAction('Save All', self.__contextMenuSaveAll)
        self.__menu.addSeparator()
        self.__menu.addAction('Close', self.__contextMenuClose)

    def __showContextMenu(self, coord, index):
        """
        Private slot to show the tab context menu.
        
        @param coord the position of the mouse pointer (QPoint)
        @param index index of the tab the menu is requested for (integer)
        """
        self.contextMenuEditor = self.widget(index)

        self.contextMenuIndex = index
        
        coord = self.mapToGlobal(coord)
        self.__menu.popup(coord)
    
    def __handleTabCustomContextMenuRequested(self, point):
        """
        Private slot to handle the context menu request for the tabbar.
        
        @param point point the context menu was requested (QPoint)
        """
        _tabbar = self.tabBar()
        for index in range(_tabbar.count()):
            rect = _tabbar.tabRect(index)
            if rect.contains(point):
                self.emit(QtCore.SIGNAL("customTabContextMenuRequested(const QPoint &, int)"), 
                          _tabbar.mapToParent(point), index)
                break

    def __contextMenuClose(self):
        """
        Private method to close the selected tab.
        """
        self.removeTab(self.contextMenuIndex)
        self.contextMenuEditor.close()
        gc.collect()

    def __contextMenuSaveAs(self):
        """
        Private method to save the selected tab to a new file.
        """
        pass
#        if self.contextMenuEditor:
#            self.vm.saveAsEditorEd(self.contextMenuEditor)
        
    def __contextMenuSaveAll(self):
        """
        Private method to save all tabs.
        """
        pass
#        self.vm.saveEditorsList(self.editors)

    def selectTab(self, pos):
        """
        Public method to get the index of a tab given a position.
        
        @param pos position determining the tab index (QPoint)
        @return index of the tab (integer)
        """
        _tabbar = self.tabBar()
        for index in range(_tabbar.count()):
            rect = _tabbar.tabRect(index)
            if rect.contains(pos):
                return index
        
        return -1

    def setTabContextMenuPolicy(self, policy):
        """
        Public method to set the context menu policy of the tab.
        
        @param policy context menu policy to set (Qt.ContextMenuPolicy)
        """
        self.tabBar().setContextMenuPolicy(policy)
        if policy == QtCore.Qt.CustomContextMenu:
            self.connect(self.tabBar(), 
                QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                self.__handleTabCustomContextMenuRequested)
        else:
            self.disconnect(self.tabBar(), 
                QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                self.__handleTabCustomContextMenuRequested)


class ScanFeedback(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
#        self.resize(QtCore.QSize(QtCore.QRect(0,0,1047,688).size()).expandedTo(self.minimumSizeHint()))
        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName("gridlayout")

        self.scanFeedbackTab = SmpTabWidget(self)
        self.scanFeedbackTab.setObjectName("scanFeedbackTab")
        self.gridlayout.addWidget(self.scanFeedbackTab,0,0,1,1)
#        self.scanFeedbackTab.removeTab(0)
        
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
        
        self.closeAction = QtGui.QAction('&Close', self)

    def __handleTabContextMenuRequested(self, point):
        """
        Private slot to handle the context menu request for the tabbar.
        
        @param point point the context menu was requested (QPoint)
        """
        _tabbar = self.tabBar()
        for index in range(_tabbar.count()):
            rect = _tabbar.tabRect(index)
            if rect.contains(point):
                self.emit(SIGNAL("customTabContextMenuRequested(const QPoint &, int)"), 
                          _tabbar.mapToParent(point), index)
                break

    def newScanAnalysis(self, newAnalysis):
        self.scanFeedbackTab.addTab(newAnalysis, '')
        self.scanFeedbackTab.setCurrentWidget(newAnalysis)
        
        self.scanFeedbackTab.addAction(self.closeAction)
        self.scanFeedbackTab.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.connect(self.closeAction, QtCore.SIGNAL("triggered()"), self.scanFeedbackTab.close)

    def newScanAnalysis1D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis1D(self, scanParams))

    def newScanAnalysis2D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis2D(self, scanParams))

    def setTabLabel(self, scanParams):
        i = self.scanFeedbackTab.currentIndex()
        self.scanFeedbackTab.setTabText(i, scanParams['title'])
