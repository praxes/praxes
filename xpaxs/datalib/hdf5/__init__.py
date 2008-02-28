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

from xpaxs.datalib.hdf5.qtdatamodel import QtFileModel
from xpaxs.datalib.hdf5.qtdataview import QtDataView

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class FileInterface(QtCore.QObject):

    """The file interface is an object containing the file model and file views.
    """

    def __init__(self, parent=None):
        super(FileInterface, self).__init__(parent)

        self.dockWidgets = {}

        self.fileModel = QtFileModel()
        self.fileView = QtDataView(self.fileModel)
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
