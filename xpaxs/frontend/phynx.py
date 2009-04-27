"""
"""
from __future__ import with_statement

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
            # obtaining the lock here is necessary, otherwise application can
            # freeze if navigating tree while data is processing
            with self.file.plock:
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
        with self.file.plock:
            return self.parent.children.index(self)

    @property
    def type(self):
        return self._type

    def __init__(self, file, node, parent=None):
        with file.plock:
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
        with self.file.plock:
            return self.file.close()

    def __getitem__(self, path):
        if path == '/':
            return self
        else:
            return H5NodeProxy(self.file, self.file[path], self)


class FileModel(QtCore.QAbstractItemModel):

    """
    """

    def __init__(self, parent=None):
        super(FileModel, self).__init__(parent)
        self.rootItem = RootItem(['File/Group/Dataset', 'Description'])
        self._idMap = {QtCore.QModelIndex().internalId(): self.rootItem}

    def clearRows(self, index):
        self.getItemFromIndex(index).clearChildren()

    def close(self):
        for item in self.rootItem:
            item.close()
        self._idMap = {}

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = self.getItemFromIndex(index)
        column = index.column()
        if column == 0:
            return QtCore.QVariant(item.name)
        if column == 1:
            return QtCore.QVariant(item.type)
        return QtCore.QVariant()

    def getItemFromIndex(self, index):
        try:
            return self._idMap[index.internalId()]
        except KeyError:
            return self.rootItem

    def hasChildren(self, index):
        return self.getItemFromIndex(index).hasChildren

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and \
                role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.rootItem.header[section])

        return QtCore.QVariant()

    def index(self, row, column, parent):
        parentItem = self.getItemFromIndex(parent)

        child = parentItem.children[row]
        index = self.createIndex(row, column, id(child))
        self._idMap.setdefault(index.internalId(), child)
        return index

    def parent(self, index):
        child = self.getItemFromIndex(index)
        parent = child.parent
        if parent == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parent.row, 0, id(parent))

    def rowCount(self, index):
        return len(self.getItemFromIndex(index))

    def _convertFile(self, filename):
        print 'this is an old file whose format is no longer supported'
        f = phynx.File(filename, 'a', lock=QRLock())
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

    def _openFile(self, filename):
        f = phynx.File(filename, 'a', lock=QRLock())
        try:
            if f.creator == 'phynx':
                return f
        except RuntimeError:
            pass

        # if we got this far, the format is old and needs to be converted
        f.close()
        self._convertFile(filename)

        return phynx.File(filename, 'a', lock=QRLock())

    def openFile(self, filename):
        for item in self.rootItem:
            if item.name == filename:
                return item.file

        phynxFile = self._openFile(filename)
        self.rootItem.appendChild(phynxFile)
        self.emit(QtCore.SIGNAL('fileAppended'))
        return phynxFile

    def itemActivated(self, index):
        scanData = self.getItemFromIndex(index).getNode()
        self.emit(QtCore.SIGNAL('scanActivated'), scanData)
