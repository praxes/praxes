# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\chiqDialog.ui'
#
# Created: Mon Jun 14 16:20:36 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_chiqDialog(object):
    def setupUi(self, chiqDialog):
        chiqDialog.setObjectName("chiqDialog")
        chiqDialog.resize(659, 157)
        self.buttonBox = QtGui.QDialogButtonBox(chiqDialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 120, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.imagebinSpinBox = QtGui.QSpinBox(chiqDialog)
        self.imagebinSpinBox.setGeometry(QtCore.QRect(40, 80, 42, 22))
        self.imagebinSpinBox.setMinimum(1)
        self.imagebinSpinBox.setObjectName("imagebinSpinBox")
        self.gridLabel = QtGui.QLabel(chiqDialog)
        self.gridLabel.setGeometry(QtCore.QRect(30, 10, 571, 31))
        self.gridLabel.setObjectName("gridLabel")
        self.label = QtGui.QLabel(chiqDialog)
        self.label.setGeometry(QtCore.QRect(30, 60, 71, 16))
        self.label.setObjectName("label")
        self.qbinSpinBox = QtGui.QSpinBox(chiqDialog)
        self.qbinSpinBox.setGeometry(QtCore.QRect(140, 80, 42, 22))
        self.qbinSpinBox.setMinimum(1)
        self.qbinSpinBox.setProperty("value", QtCore.QVariant(2))
        self.qbinSpinBox.setObjectName("qbinSpinBox")
        self.label_2 = QtGui.QLabel(chiqDialog)
        self.label_2.setGeometry(QtCore.QRect(140, 60, 71, 16))
        self.label_2.setObjectName("label_2")
        self.chibinSpinBox = QtGui.QSpinBox(chiqDialog)
        self.chibinSpinBox.setGeometry(QtCore.QRect(240, 80, 42, 22))
        self.chibinSpinBox.setMinimum(1)
        self.chibinSpinBox.setProperty("value", QtCore.QVariant(2))
        self.chibinSpinBox.setObjectName("chibinSpinBox")
        self.label_3 = QtGui.QLabel(chiqDialog)
        self.label_3.setGeometry(QtCore.QRect(230, 60, 86, 16))
        self.label_3.setObjectName("label_3")
        self.solidangleCheckBox = QtGui.QCheckBox(chiqDialog)
        self.solidangleCheckBox.setGeometry(QtCore.QRect(330, 80, 216, 18))
        self.solidangleCheckBox.setChecked(True)
        self.solidangleCheckBox.setObjectName("solidangleCheckBox")

        self.retranslateUi(chiqDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), chiqDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), chiqDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(chiqDialog)

    def retranslateUi(self, chiqDialog):
        chiqDialog.setWindowTitle(QtGui.QApplication.translate("chiqDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLabel.setText(QtGui.QApplication.translate("chiqDialog", "Q is currently starting at ?, with ? interval. Approximately ? pts\n"
"Chi is currently starting at ?, with ? interval. Approximately ? pts", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("chiqDialog", "image size bin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("chiqDialog", "qgrid bin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("chiqDialog", "chiqgrid bin", None, QtGui.QApplication.UnicodeUTF8))
        self.solidangleCheckBox.setText(QtGui.QApplication.translate("chiqDialog", "counts/powder sterradian", None, QtGui.QApplication.UnicodeUTF8))

