"""
"""
import operator
import os
import posixpath
import shutil

from PyQt4 import QtCore, QtGui

from praxes.io import phynx
from ..rlock import FastRLock


class RootItem(object):

    @property
    def children(self):
        return self._children

    @property
    def hasChildren(self):
        return True

    @property
    def header(self):
        return self._header

    @property
    def parent(self):
        return None

    def __init__(self, header):
        self._header = header
        self._children = []

    def __iter__(self):
        def iter_files(files):
            for f in files:
                yield f
        return iter_files(self.children)

    def __len__(self):
        return len(self.children)

    def appendChild(self, item):
        self.children.append(H5FileProxy(item, self))


class H5NodeProxy(object):

    @property
    def children(self):
        if not self.hasChildren:
            return []

        if not self._children:
            # obtaining the lock here is necessary, otherwise application can
            # freeze if navigating tree while data is processing
            with self.file:
                self._children = [
                    H5NodeProxy(self.file, i, self)
                    for i in self.getNode(self.name).values()
                    ]
        return self._children

    @property
    def dtype(self):
        return self._dtype

    @property
    def file(self):
        return self._file

    @property
    def hasChildren(self):
        return self._hasChildren

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @property
    def row(self):
        with self.file:
            try:
                return self.parent.children.index(self)
            except ValueError:
                return

    @property
    def shape(self):
        return self._shape

    @property
    def type(self):
        return self._type

    def __init__(self, file, node, parent=None):
        with file:
            self._file = file
            self._parent = parent
            self._name = node.id
            self._type = type(node).__name__
            try:
                self._dtype = str(node.dtype)
            except AttributeError:
                self._dtype = ""
            try:
                self._shape = str(node.shape)
            except AttributeError:
                self._shape = ""

            self._hasChildren = isinstance(node, phynx.Group)
            self._children = []

    def clearChildren(self):
        self._children = []

    def getNode(self, name=None):
        if not name:
            name = self.name
        with self.file:
            return self.file[name]

    def __len__(self):
        return len(self.children)


class H5FileProxy(H5NodeProxy):

    @property
    def file_name(self):
        with self.file:
            return self.file.file_name

    def __init__(self, file, parent=None):
        super(H5FileProxy, self).__init__(file, file, parent)
        self._name = file.name

    def close(self):
        return self.file.close()

    def __getitem__(self, path):
        if path == '/':
            return self
        else:
            return H5NodeProxy(self.file, self.file[path], self)


class FileModel(QtCore.QAbstractItemModel):

    """
    """

    fileAppended = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(FileModel, self).__init__(parent)
        self.rootItem = RootItem(['File/Group/Dataset', 'Description', 'Shape', 'Data Type'])
        self._idMap = {QtCore.QModelIndex().internalId(): self.rootItem}

    def clearRows(self, index):
        self.getProxyFromIndex(index).clearChildren()

    def close(self):
        for item in self.rootItem:
            item.close()
        self._idMap = {}

    def columnCount(self, parent):
        return 4

    def data(self, index, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = self.getProxyFromIndex(index)
        column = index.column()
        if column == 0:
            if item.name == '/':
                return QtCore.QVariant(item.file.file_name)
            else:
                return QtCore.QVariant(posixpath.split(item.name)[-1])
        if column == 1:
            return QtCore.QVariant(item.type)
        if column == 2:
            return QtCore.QVariant(item.shape)
        if column == 3:
            return QtCore.QVariant(item.dtype)
        return QtCore.QVariant()

    def getNodeFromIndex(self, index):
        try:
            return self.getProxyFromIndex(index).getNode()
        except AttributeError:
            return None

    def getProxyFromIndex(self, index):
        try:
            return self._idMap[index.internalId()]
        except KeyError:
            return self.rootItem

    def hasChildren(self, index):
        return self.getProxyFromIndex(index).hasChildren

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and \
                role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.rootItem.header[section])

        return QtCore.QVariant()

    def index(self, row, column, parent):
        parentItem = self.getProxyFromIndex(parent)

        child = parentItem.children[row]
        id = hash((child.file.file_name, child.name))
        index = self.createIndex(row, column, id)
        self._idMap.setdefault(index.internalId(), child)
        return index

    def parent(self, index):
        child = self.getProxyFromIndex(index)
        parent = child.parent
        if parent == self.rootItem:
            return QtCore.QModelIndex()

        if parent.row is None:
            return QtCore.QModelIndex()
        else:
            id = hash((parent.file.file_name, parent.name))
            return self.createIndex(parent.row, 0, id)

    def rowCount(self, index):
        return len(self.getProxyFromIndex(index))

    def openFile(self, file_name):
        for item in self.rootItem:
            if item.file_name == file_name:
                return item.file

        phynxFile = phynx.open(file_name, 'a', lock=FastRLock())
        self.rootItem.appendChild(phynxFile)
        self.fileAppended.emit()
        return phynxFile


class FileView(QtGui.QTreeView):

    def __init__(self, fileModel, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.setModel(fileModel)
        self.setColumnWidth(0, 250)

        self.collapsed.connect(fileModel.clearRows)
        fileModel.fileAppended.connect(self.doItemsLayout)


class ExportRawCSV(QtCore.QObject):

    def __init__(self, h5Node, parent=None):
        QtCore.QObject.__init__(parent)
        assert isinstance(h5Node, phynx.Dataset)
        assert len(h5Node.shape) <= 2

        file_name = QtGui.QFileDialog.getSaveFileName(
            parent,
            "Export Dataset",
            posixpath.split(h5Node.name)[-1] + '.txt',
            "text files (*.txt *.dat *.csv)"
        )
        if file_name:
            self.exportData(str(file_name), h5Node)

    def exportData(self, file_name, h5Node):
        try:
            data = h5Node.map
        except TypeError:
            data = h5Node[:]
        import numpy as np
        np.savetxt(file_name, data, fmt='%g', delimiter=',')

    @classmethod
    def offersService(cls, h5Node):
        try:
            assert isinstance(h5Node, phynx.Dataset)
            assert len(h5Node.shape) <= 2
            return True
        except AssertionError:
            return False


class ExportCorrectedCSV(ExportRawCSV):

    def __init__(self, h5Node, parent=None):
        QtCore.QObject.__init__(parent)
        assert isinstance(h5Node, phynx.Dataset)
        assert len(h5Node.shape) <= 2
        assert hasattr(h5Node, "corrected_value")

        file_name = QtGui.QFileDialog.getSaveFileName(
            parent,
            "Export Dataset",
            posixpath.split(h5Node.name)[-1] + '_corr.txt',
            "text files (*.txt *.dat *.csv)"
        )
        if file_name:
            self.exportData(str(file_name), h5Node)

    def exportData(self, file_name, h5Node):
        try:
            data = h5Node.corrected_value.map
        except TypeError:
            data = h5Node.corrected_value[:]
        import numpy as np
        np.savetxt(file_name, data, fmt='%g', delimiter=',')

    @classmethod
    def offersService(cls, h5Node):
        try:
            assert isinstance(h5Node, phynx.Dataset)
            assert len(h5Node.shape) <= 2
            assert hasattr(h5Node, "corrected_value")
            return True
        except AssertionError:
            return False


#if __name__ == "__main__":
#    import sys
#    app = QtGui.QApplication(sys.argv)
#    fileModel = FileModel()
#    fileView = FileView(fileModel)
#    fileModel.openFile('../io/phynx/tests/citrus_leaves.dat.h5')
#    fileView.show()
#
#    sys.exit(app.exec_())
