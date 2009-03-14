"""
"""

import logging
import operator
import os
import shutil

from PyQt4 import QtCore, QtGui

from xpaxs.io import phynx


logger = logging.getLogger(__file__)



class QRLock(QtCore.QMutex):

    """
    """

    def __init__(self):
        QtCore.QMutex.__init__(self, QtCore.QMutex.Recursive)

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()


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
            self._children = [
                H5NodeProxy(self.file, i, self)
                for i in sorted(
                    self.getNode(self.path).listobjects(),
                    key=operator.attrgetter('name')
                )
            ]
        return self._children

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
    def path(self):
        return self._path

    @property
    def row(self):
        return self.parent.children.index(self)

    @property
    def type(self):
        return self._type

    def __init__(self, file, node, parent=None):
        self._file = file
        self._name = node.name
        self._parent = parent
        self._path = node.path
        self._type = type(node).__name__
        self._hasChildren = isinstance(node, phynx.Group)
        self._children = []

    def clearChildren(self):
        self._children = []

    def getNode(self, path=None):
        if not path:
            path = self.path
        return self.file[path]

    def __len__(self):
        return len(self.children)


class H5FileProxy(H5NodeProxy):

    @property
    def path(self):
        return '/'

    def __init__(self, file, parent=None):
        super(H5FileProxy, self).__init__(file, file, parent)

    def close(self):
        return self.file.close()


class FileModel(QtCore.QAbstractItemModel):

    """
    """

    def __init__(self, parent=None):
        super(FileModel, self).__init__(parent)
        self.rootItem = RootItem(['File/Group/Dataset', 'Description'])

    def canFetchMore(self, index):
        parentItem = index.internalPointer()
        if parentItem is not None and parentItem.hasChildren:
            return len(parentItem) == 0
        else:
            return False

    def clearRows(self, index):
        parent = index.internalPointer()
        self.beginRemoveRows(index, 0, len(parent)-1)
        parent.clearChildren()
        self.endRemoveRows()

    def close(self):
        for item in self.rootItem:
            item.close()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = index.internalPointer()
        column = index.column()
        try:
            if column == 0:
                return QtCore.QVariant(item.name)
            if column == 1:
                return QtCore.QVariant(item.type)
            return QtCore.QVariant()
        except AttributeError:
            return QtCore.QVariant()

    def fetchMore(self, index):
        parent = index.internalPointer()
        if parent is not None:
            self.beginInsertRows(index, 0, len(parent))
            parent.children
            self.endInsertRows()

    def hasChildren(self, index):
        parentItem = index.internalPointer()
        if parentItem is None:
            parentItem = self.rootItem
        return parentItem.hasChildren

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and \
                role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.rootItem.header[section])

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.rootItem

        child = parentItem.children[row]
        return self.createIndex(row, column, child)

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child = index.internalPointer()
        parent = child.parent

        if parent == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parent.row, 0, parent)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return len(parentItem)

    def _openFile(self, filename):
        f = phynx.File(filename, 'a', lock=QRLock())
        try:
            if f.creator == 'phynx':
                return f
        except RuntimeError:
            pass

        print 'this is an old file whose format is no longer supported'
        try:
            format = f.attrs['format']
            if format == 'h5py transitional':
                from xpaxs.io.compat.transitional import convert_to_phynx
            else:
                from xpaxs.io.compat.original import convert_to_phynx
        except:
            from xpaxs.io.compat.original import convert_to_phynx
        f.close()

        backup = '%s.old'%filename
        if os.path.exists(backup):
            backup = '%s.backup'%filename
            print 'moving old file to %s'%backup
            shutil.move(filename, backup)
        else:
            print 'moving old file to %s'%backup
            shutil.move(filename, backup)
        specfile = filename.rstrip('.hdf5').rstrip('.h5')
        f = convert_to_phynx(specfile)
        f.close()
        return phynx.File(filename, 'a', lock=QRLock())

    def openFile(self, filename):
        for item in self.rootItem:
            if item.name == filename:
                return item

        phynxFile = self._openFile(filename)
        self.rootItem.appendChild(phynxFile)
        self.emit(QtCore.SIGNAL('fileAppended'))
        return phynxFile

    def itemActivated(self, index):
        scanData = index.internalPointer().getNode()
        self.emit(QtCore.SIGNAL('scanActivated'), scanData)


class FileView(QtGui.QTreeView):

    def __init__(self, model=None, parent=None):
        super(FileView, self).__init__(parent)

        self.setModel(model)

        self.connect(
            self,
            QtCore.SIGNAL('activated(QModelIndex)'),
            model.itemActivated
        )
        self.connect(
            self,
            QtCore.SIGNAL('collapsed(QModelIndex)'),
            model.clearRows
        )

#    def appendItem(self, index):
#        self.expand(index)
#        self.resizeColumnToContents(0)
#        self.resizeColumnToContents(1)
#        self.resizeColumnToContents(2)


class FileInterface(QtCore.QObject):

    @property
    def fileModel(self):
        return self._fileModel

    @property
    def fileView(self):
        return self._fileView

    def __init__(self, parent=None):
        super(FileInterface, self).__init__(parent)
        self.dockWidgets = {}
        self.mainWindow = parent

        self._fileModel = FileModel(parent=self)
        self._fileView = FileView(self.fileModel)

        self._fileRegistry = {}

        self.connect(self._fileModel,
                     QtCore.SIGNAL('fileAppended'),
                     self._fileView.doItemsLayout)
        self.connect(self._fileModel,
                     QtCore.SIGNAL('scanActivated'),
                     self.mainWindow.newScanWindow)
        self.addDockWidget(self._fileView, 'File View',
                           QtCore.Qt.AllDockWidgetAreas,
                           QtCore.Qt.LeftDockWidgetArea,
                           'FileViewDock')

        self._registerService()

    def _registerService(self):
        import xpaxs
        xpaxs.application.registerService('FileInterface', self)

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

    def getH5FileFromKey(self, key):
        h5File = self._fileRegistry.get(key, None)

        if not h5File:
            default = key.split(os.path.sep)[-1] + '.h5'
            h5File = self.openFile(default)
            self._fileRegistry[key] = h5File

        return h5File

    def openFile(self, filename):
        if os.path.isfile(filename):
            return self.fileModel.openFile(filename)
        else:
            newfilename = QtGui.QFileDialog.getSaveFileName(self.mainWindow,
                    "Save File", filename, "hdf5 files (*.h5 *.hdf5 *.nxs)")
            if newfilename:
                newfilename = str(newfilename)
                if newfilename.split('.')[-1] not in ('h5', 'hdf5', 'nxs'):
                    newfilename = newfilename + '.h5'
                return self.fileModel.openFile(newfilename)
            else: self.openFile(filename)
