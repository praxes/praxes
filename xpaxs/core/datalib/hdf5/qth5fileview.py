"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.datalib.hdf5.qth5fileview')


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
