# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\textureanalysis.ui'
#
# Created: Mon Jun 14 16:20:39 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(399, 167)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(45, 115, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.savenameLineEdit = QtGui.QLineEdit(Dialog)
        self.savenameLineEdit.setGeometry(QtCore.QRect(35, 25, 346, 25))
        self.savenameLineEdit.setObjectName("savenameLineEdit")
        self.fulltexplotComboBox = QtGui.QComboBox(Dialog)
        self.fulltexplotComboBox.setGeometry(QtCore.QRect(40, 70, 231, 24))
        self.fulltexplotComboBox.setObjectName("fulltexplotComboBox")
        self.fulltexplotComboBox.addItem(QtCore.QString())
        self.fulltexplotComboBox.addItem(QtCore.QString())
        self.fulltexplotComboBox.addItem(QtCore.QString())
        self.fulltexplotComboBox.addItem(QtCore.QString())

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.fulltexplotComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "save LHS and RHS", None, QtGui.QApplication.UnicodeUTF8))
        self.fulltexplotComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "ave LHS+RHS", None, QtGui.QApplication.UnicodeUTF8))
        self.fulltexplotComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "only LHS", None, QtGui.QApplication.UnicodeUTF8))
        self.fulltexplotComboBox.setItemText(3, QtGui.QApplication.translate("Dialog", "only RHS", None, QtGui.QApplication.UnicodeUTF8))

