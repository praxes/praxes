"""
"""

import logging
import os
import shutil

from PyQt4 import QtCore, QtGui

from xpaxs.io import phynx


logger = logging.getLogger(__file__)


class RootItem(object):

    def __init__(self, header):
        self._header = header
        self._children = []

    @property
    def children(self):
        return self._children

    @property
    def header(self):
        return self._header

    @property
    def parent(self):
        return None

    def __iter__(self):
        def iter_files(files):
            for f in files:
                yield f
        return iter_files(self.children)

    def __len__(self):
        return len(self.children)

    def appendChild(self, item):
        item.parent = self
        self.children.append(item)


class FileModel(QtCore.QAbstractItemModel):

    """
    """

    def __init__(self, parent=None):
        super(FileModel, self).__init__(parent)
        self.rootItem = RootItem(['File/Group/Dataset', 'Description'])

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
                return QtCore.QVariant(type(item).__name__)
            return QtCore.QVariant()
        except AttributeError:
            return QtCore.QVariant()

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and \
                role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.rootItem.header[section])

        return QtCore.QVariant()

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QtCore.QModelIndex()

        if not parentIndex.isValid():
            parent = self.rootItem
        else:
            parent = parentIndex.internalPointer()

        child = parent.children[row]
        if child:
            return self.createIndex(row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child = index.internalPointer()
        parent = child.parent

        if parent == self.rootItem:
            return QtCore.QModelIndex()

        row = parent.parent.children.index(parent)

        return self.createIndex(row, 0, parent)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        try:
            return len(parentItem.children)
        except (TypeError, AttributeError):
            return 0

    def _openFile(self, filename):
        f = phynx.File(filename, 'a')
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
        return convert_to_phynx(specfile)

    def openFile(self, filename):
        for item in self.rootItem:
            if item.name == filename:
                return item

        phynxFile = self._openFile(filename)
        self.rootItem.appendChild(phynxFile)
        self.emit(QtCore.SIGNAL('fileAppended'))
        return phynxFile

#    def itemActivated(self, index):
#        scanData = index.internalPointer().itemActivated()
#        self.emit(QtCore.SIGNAL('scanActivated'), scanData)


class FileView(QtGui.QTreeView):

    def __init__(self, model=None, parent=None):
        super(FileView, self).__init__(parent)

        self.setModel(model)

#        self.connect(self,
#                     QtCore.SIGNAL('activated(QModelIndex)'),
#                     model.itemActivated)

#    def appendItem(self, index):
#        self.expand(index)
#        self.resizeColumnToContents(0)
#        self.resizeColumnToContents(1)
#        self.resizeColumnToContents(2)


class FileInterface(QtCore.QObject):

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
#        self.connect(self._fileModel,
#                     QtCore.SIGNAL('scanActivated'),
#                     self.mainWindow.newScanWindow)
        self.addDockWidget(self._fileView, 'File View',
                           QtCore.Qt.AllDockWidgetAreas,
                           QtCore.Qt.LeftDockWidgetArea,
                           'FileViewDock')

        self._registerService()

    def _registerService(self):
        import xpaxs
        xpaxs.application.registerService('FileInterface', self)

    @property
    def fileModel(self):
        return self._fileModel

    @property
    def fileView(self):
        return self._fileView

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


#class QRLock(QtCore.QMutex):
#
#    """
#    """
#
#    def __init__(self):
#        QtCore.QMutex.__init__(self, QtCore.QMutex.Recursive)
#
#    def __enter__(self):
#        self.lock()
#        return self
#
#    def __exit__(self, type, value, traceback):
#        self.unlock()
#
#    def acquire(self):
#        return self.lock()
#
#    def release(self):
#        self.unlock()
#
#from h5py.highlevel import LockableObject
#LockableObject._lock = QRLock()
