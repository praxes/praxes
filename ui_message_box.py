# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\message_box.ui'
#
# Created: Mon Jun 14 16:20:38 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_messageDialog(object):
    def setupUi(self, messageDialog):
        messageDialog.setObjectName("messageDialog")
        messageDialog.resize(309, 104)
        self.buttonBox = QtGui.QDialogButtonBox(messageDialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 55, 181, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.messageLabel = QtGui.QLabel(messageDialog)
        self.messageLabel.setGeometry(QtCore.QRect(4, 12, 296, 36))
        self.messageLabel.setObjectName("messageLabel")

        self.retranslateUi(messageDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), messageDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), messageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(messageDialog)

    def retranslateUi(self, messageDialog):
        messageDialog.setWindowTitle(QtGui.QApplication.translate("messageDialog", "Continue?", None, QtGui.QApplication.UnicodeUTF8))
        self.messageLabel.setText(QtGui.QApplication.translate("messageDialog", "ave background will be calculated\n"
"previous background will be overwritten", None, QtGui.QApplication.UnicodeUTF8))

