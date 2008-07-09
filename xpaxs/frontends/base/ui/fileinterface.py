"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.core.datalib.hdf5file import XpaxsFile, XpaxsScan

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.frontends.base.ui.fileinterface')


class TreeItem:
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def itemActivated(self):
        pass


class H5EntryItem(TreeItem):

    def __init__(self, scanData, parent):
        self.scanData = scanData

        self.parentItem = parent
        self.childItems = []

        scannum = '%s'%self.scanData.getScanNumber()
        cmd = self.scanData.getScanCommand()
        numpoints = '%d'%self.scanData.getNumExpectedScanLines()
        self.itemData = [scannum, cmd, numpoints]

    def itemActivated(self):
        return self.scanData


class FileItem(TreeItem):

    def __init__(self, datafile, parent):
        self.xpaxsFile = datafile

        self.parentItem = parent
        self.filename = datafile.getFileName()
        self.itemData = [os.path.split(self.filename)[-1], '', '']
        self.childItems = []

        for entry in datafile.getNodes():
            self.appendChild(entry)

        QtCore.QObject.connect(self.xpaxsFile,
                               QtCore.SIGNAL('newEntry'),
                               self.appendChild)

    def appendChild(self, h5Entry):
        item = H5EntryItem(h5Entry, self)
        self.childItems.append(item)

    def close(self):
        self.xpaxsFile.close()

    def getFileName(self):
        return self.filename

    def getFileObject(self):
        return self.xpaxsFile


class H5FileModel(QtCore.QAbstractItemModel):
    """
    """

    def __init__(self, filename=None, fileClass=XpaxsFile, parent=None):
        super(H5FileModel, self).__init__(parent)

        self._openFile = fileClass

        rootData = []
        rootData.append(QtCore.QVariant('File/Entry #'))
        rootData.append(QtCore.QVariant('Command'))
        rootData.append(QtCore.QVariant('Points'))
        self.rootItem = TreeItem(rootData)
        if filename: self.openFile(filename)

    def close(self):
        for item in self.rootItem.childItems:
            item.close()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = index.internalPointer()

        return QtCore.QVariant(item.data(index.column()))

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and \
                role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) \
                or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def getFileItem(self, filename):
        for item in self.rootItem.childItems:
            if item.getFileName() == filename:
                return item

    def openFile(self, filename):
        item = self.getFileItem(filename)
        if item: return item.getFileObject()

        dataObject = self._openFile(filename, 'r+', self)
        item = FileItem(dataObject, self.rootItem)
        self.rootItem.appendChild(item)
        row = self.rowCount(QtCore.QModelIndex())-1
        index = self.index(row, 0, QtCore.QModelIndex())
        self.emit(QtCore.SIGNAL('fileAppended'), index)
        return dataObject

    def itemActivated(self, index):
        scanData = index.internalPointer().itemActivated()
        self.emit(QtCore.SIGNAL('scanActivated'), scanData)


class H5FileView(QtGui.QTreeView):

    def __init__(self, model=None, parent=None):
        super(H5FileView, self).__init__(parent)

        self.setModel(model)

        self.connect(self,
                     QtCore.SIGNAL('activated(QModelIndex)'),
                     model.itemActivated)

    def appendItem(self, index):
        self.doItemsLayout()
        self.expand(index)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)


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
