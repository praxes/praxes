# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python\editrawxrdDialog.ui'
#
# Created: Tue Jan 11 22:49:17 2011
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_editrawxrdDialog(object):
    def setupUi(self, editrawxrdDialog):
        editrawxrdDialog.setObjectName("editrawxrdDialog")
        editrawxrdDialog.resize(420, 183)
        self.buttonBox = QtGui.QDialogButtonBox(editrawxrdDialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 145, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dezingCheckBox = QtGui.QCheckBox(editrawxrdDialog)
        self.dezingCheckBox.setGeometry(QtCore.QRect(15, 20, 146, 22))
        self.dezingCheckBox.setObjectName("dezingCheckBox")
        self.normComboBox = QtGui.QComboBox(editrawxrdDialog)
        self.normComboBox.setGeometry(QtCore.QRect(190, 60, 201, 31))
        self.normComboBox.setObjectName("normComboBox")
        self.normCheckBox = QtGui.QCheckBox(editrawxrdDialog)
        self.normCheckBox.setGeometry(QtCore.QRect(15, 65, 166, 22))
        self.normCheckBox.setObjectName("normCheckBox")
        self.multCheckBox = QtGui.QCheckBox(editrawxrdDialog)
        self.multCheckBox.setGeometry(QtCore.QRect(15, 105, 166, 22))
        self.multCheckBox.setObjectName("multCheckBox")
        self.multSpinBox = QtGui.QDoubleSpinBox(editrawxrdDialog)
        self.multSpinBox.setGeometry(QtCore.QRect(195, 105, 191, 27))
        self.multSpinBox.setDecimals(8)
        self.multSpinBox.setMaximum(999999999.0)
        self.multSpinBox.setProperty("value", QtCore.QVariant(10000000.0))
        self.multSpinBox.setObjectName("multSpinBox")
        self.dezingComboBox = QtGui.QComboBox(editrawxrdDialog)
        self.dezingComboBox.setGeometry(QtCore.QRect(140, 15, 131, 31))
        self.dezingComboBox.setObjectName("dezingComboBox")
        self.dezingSpinBox = QtGui.QDoubleSpinBox(editrawxrdDialog)
        self.dezingSpinBox.setGeometry(QtCore.QRect(275, 20, 121, 27))
        self.dezingSpinBox.setDecimals(3)
        self.dezingSpinBox.setMinimum(1.0)
        self.dezingSpinBox.setMaximum(999999999.0)
        self.dezingSpinBox.setProperty("value", QtCore.QVariant(1.5))
        self.dezingSpinBox.setObjectName("dezingSpinBox")
        self.dezingLabel = QtGui.QLabel(editrawxrdDialog)
        self.dezingLabel.setGeometry(QtCore.QRect(275, 5, 136, 17))
        self.dezingLabel.setObjectName("dezingLabel")

        self.retranslateUi(editrawxrdDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), editrawxrdDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), editrawxrdDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(editrawxrdDialog)

    def retranslateUi(self, editrawxrdDialog):
        editrawxrdDialog.setWindowTitle(QtGui.QApplication.translate("editrawxrdDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.dezingCheckBox.setText(QtGui.QApplication.translate("editrawxrdDialog", "dezing images", None, QtGui.QApplication.UnicodeUTF8))
        self.normCheckBox.setText(QtGui.QApplication.translate("editrawxrdDialog", "normalize by counter", None, QtGui.QApplication.UnicodeUTF8))
        self.multCheckBox.setText(QtGui.QApplication.translate("editrawxrdDialog", "multiply by factor", None, QtGui.QApplication.UnicodeUTF8))
        self.dezingLabel.setText(QtGui.QApplication.translate("editrawxrdDialog", "crit ratio to nieghs.", None, QtGui.QApplication.UnicodeUTF8))

