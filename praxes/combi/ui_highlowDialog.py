# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\highlowDialog.ui'
#
# Created: Mon Jun 14 16:20:37 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_highlowDialog(object):
    def setupUi(self, highlowDialog):
        highlowDialog.setObjectName("highlowDialog")
        highlowDialog.resize(352, 128)
        self.buttonBox = QtGui.QDialogButtonBox(highlowDialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 70, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lowSpinBox = QtGui.QDoubleSpinBox(highlowDialog)
        self.lowSpinBox.setGeometry(QtCore.QRect(20, 40, 62, 22))
        self.lowSpinBox.setMinimum(-1000000.0)
        self.lowSpinBox.setMaximum(1000000.0)
        self.lowSpinBox.setObjectName("lowSpinBox")
        self.highSpinBox = QtGui.QDoubleSpinBox(highlowDialog)
        self.highSpinBox.setGeometry(QtCore.QRect(100, 40, 62, 20))
        self.highSpinBox.setMinimum(-1000000.0)
        self.highSpinBox.setMaximum(1000000.0)
        self.highSpinBox.setObjectName("highSpinBox")
        self.label = QtGui.QLabel(highlowDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(highlowDialog)
        self.label_2.setGeometry(QtCore.QRect(100, 20, 76, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(highlowDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), highlowDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), highlowDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(highlowDialog)

    def retranslateUi(self, highlowDialog):
        highlowDialog.setWindowTitle(QtGui.QApplication.translate("highlowDialog", "Enter range for colorbar", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("highlowDialog", "low value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("highlowDialog", "high value", None, QtGui.QApplication.UnicodeUTF8))

