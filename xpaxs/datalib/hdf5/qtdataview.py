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

from xpaxs.datalib.hdf5.qtdatamodel import FileModel

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class QtDataView(QtGui.QTreeView):

    def __init__(self, model=None, parent=None):
        super(QtDataView, self).__init__(parent)

        self.setModel(model)

        self.fileView.connect(self,
                              QtCore.SIGNAL('activated(QModelIndex)'),
                              model.itemActivated)


class FileInterface(QtCore.QObject):

    def __init__(self, parent=None):
        super(FileInterface, self).__init__(parent)

        self.dockWidgets = {}

        self.fileModel = FileModel()
        self.fileView = QtGui.QTreeView()
        self.fileView.setModel(self.fileModel)
        self.fileView.connect(self.fileView,
                              QtCore.SIGNAL('activated(QModelIndex)'),
                              self.fileModel.itemActivated)
        fileDockWidget = QtGui.QDockWidget('File View')
        fileDockWidget.setObjectName('FileDockWidget')
        fileDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|
                                       QtCore.Qt.RightDockWidgetArea)
        fileDockWidget.setWidget(self.fileView)
        self.dockWidgets['File View'] = (QtCore.Qt.LeftDockWidgetArea,
                                         fileDockWidget)

    def openFile(self, filename):
        self.fileModel.appendFile(filename)
        # TODO: add file to list of open files in menu?
        self.fileView.doItemsLayout()
        row = self.fileModel.rowCount(QtCore.QModelIndex())-1
        index = self.fileModel.index(row, 0, QtCore.QModelIndex())
        self.fileView.expand(index)
        self.fileView.resizeColumnToContents(0)
        self.fileView.resizeColumnToContents(1)
        self.fileView.resizeColumnToContents(2)
