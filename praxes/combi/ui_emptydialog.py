# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\emptydialog.ui'
#
# Created: Mon Jun 14 16:20:36 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_emptyDialog(object):
    def setupUi(self, emptyDialog):
        emptyDialog.setObjectName("emptyDialog")
        emptyDialog.resize(911, 403)
        self.buttonBox = QtGui.QDialogButtonBox(emptyDialog)
        self.buttonBox.setGeometry(QtCore.QRect(560, 370, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(emptyDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), emptyDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), emptyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(emptyDialog)

    def retranslateUi(self, emptyDialog):
        emptyDialog.setWindowTitle(QtGui.QApplication.translate("emptyDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

