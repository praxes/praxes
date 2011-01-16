# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python\bckndinventoryDialog.ui'
#
# Created: Sun Jan 09 18:39:36 2011
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_bckndinventoryDialog(object):
    def setupUi(self, bckndinventoryDialog):
        bckndinventoryDialog.setObjectName("bckndinventoryDialog")
        bckndinventoryDialog.resize(400, 220)
        self.buttonBox = QtGui.QDialogButtonBox(bckndinventoryDialog)
        self.buttonBox.setGeometry(QtCore.QRect(25, 145, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.newnameLineEdit = QtGui.QLineEdit(bckndinventoryDialog)
        self.newnameLineEdit.setGeometry(QtCore.QRect(210, 50, 181, 27))
        self.newnameLineEdit.setObjectName("newnameLineEdit")
        self.MsgLabel = QtGui.QLabel(bckndinventoryDialog)
        self.MsgLabel.setGeometry(QtCore.QRect(25, 185, 341, 17))
        self.MsgLabel.setObjectName("MsgLabel")
        self.imageComboBox = QtGui.QComboBox(bckndinventoryDialog)
        self.imageComboBox.setGeometry(QtCore.QRect(5, 50, 186, 31))
        self.imageComboBox.setObjectName("imageComboBox")
        self.label = QtGui.QLabel(bckndinventoryDialog)
        self.label.setGeometry(QtCore.QRect(10, 25, 156, 17))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(bckndinventoryDialog)
        self.label_2.setGeometry(QtCore.QRect(210, 25, 176, 16))
        self.label_2.setObjectName("label_2")
        self.copyPushButton = QtGui.QPushButton(bckndinventoryDialog)
        self.copyPushButton.setGeometry(QtCore.QRect(25, 100, 216, 27))
        self.copyPushButton.setObjectName("copyPushButton")
        self.overwriteCheckBox = QtGui.QCheckBox(bckndinventoryDialog)
        self.overwriteCheckBox.setGeometry(QtCore.QRect(250, 100, 141, 22))
        self.overwriteCheckBox.setObjectName("overwriteCheckBox")

        self.retranslateUi(bckndinventoryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), bckndinventoryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), bckndinventoryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(bckndinventoryDialog)

    def retranslateUi(self, bckndinventoryDialog):
        bckndinventoryDialog.setWindowTitle(QtGui.QApplication.translate("bckndinventoryDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("bckndinventoryDialog", "image in sample file", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("bckndinventoryDialog", "name in Bcknd Inventory", None, QtGui.QApplication.UnicodeUTF8))
        self.copyPushButton.setText(QtGui.QApplication.translate("bckndinventoryDialog", "Copy Image To Inventory", None, QtGui.QApplication.UnicodeUTF8))
        self.overwriteCheckBox.setText(QtGui.QApplication.translate("bckndinventoryDialog", "Allow Overwrite", None, QtGui.QApplication.UnicodeUTF8))

