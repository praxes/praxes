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

from xpaxs.datalib.hdf5.qth5filemodel import H5FileModel
from xpaxs.datalib.hdf5.qth5fileview import H5FileView
from xpaxs.datalib.hdf5.xpaxsdatainterface import XpaxsFile, XpaxsScan

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class H5FileInterface(QtCore.QObject):

    def __init__(self, fileClass=XpaxsFile, parent=None):
        super(H5FileInterface, self).__init__(parent)
        self.dockWidgets = {}
        self.mainWindow = parent

        self.fileModel = H5FileModel(fileClass=fileClass, parent=self)
        self.fileView = H5FileView(self.fileModel)
        self.connect(self.fileModel,
                     QtCore.SIGNAL('fileAppended'),
                     self.fileView.appendItem)
        self.connect(self.fileModel,
                     QtCore.SIGNAL('scanActivated'),
                     self.mainWindow.newScanWindow)
        self.addDockWidget(self.fileView, 'File View',
                           QtCore.Qt.AllDockWidgetAreas,
                           QtCore.Qt.LeftDockWidgetArea,
                           'FileViewDock')

    def addDockWidget(self, widget, title, allowedAreas, defaultArea,
                      name = None):
        dock = QtGui.QDockWidget(title)
        if name: dock.setObjectName(name)
        dock.setAllowedAreas(allowedAreas)
        dock.setWidget(widget)
        action = dock.toggleViewAction()
        action.setText(title)
        self.dockWidgets[title] = (dock, defaultArea, action)

    def close(self):
        self.fileModel.close()

    def openFile(self, filename):
        return self.fileModel.openFile(filename)

    def createEntry(self, filename, scanParams):
        fileObject = self.openFile(filename)
        entry = fileObject.createEntry(scanParams)
        self.fileView.doItemsLayout()
        return entry
