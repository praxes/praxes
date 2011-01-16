# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python\LinBckndDialog.ui'
#
# Created: Sun Jan 09 18:39:36 2011
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LinBckndDialog(object):
    def setupUi(self, LinBckndDialog):
        LinBckndDialog.setObjectName("LinBckndDialog")
        LinBckndDialog.resize(735, 266)
        self.buttonBox = QtGui.QDialogButtonBox(LinBckndDialog)
        self.buttonBox.setGeometry(QtCore.QRect(520, 210, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.imageComboBox0 = QtGui.QComboBox(LinBckndDialog)
        self.imageComboBox0.setGeometry(QtCore.QRect(385, 80, 346, 31))
        self.imageComboBox0.setObjectName("imageComboBox0")
        self.normrankSpinBox = QtGui.QDoubleSpinBox(LinBckndDialog)
        self.normrankSpinBox.setGeometry(QtCore.QRect(360, 10, 62, 27))
        self.normrankSpinBox.setMaximum(1.0)
        self.normrankSpinBox.setSingleStep(0.1)
        self.normrankSpinBox.setProperty("value", QtCore.QVariant(0.5))
        self.normrankSpinBox.setObjectName("normrankSpinBox")
        self.label = QtGui.QLabel(LinBckndDialog)
        self.label.setGeometry(QtCore.QRect(20, 15, 346, 17))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(LinBckndDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 55, 341, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(LinBckndDialog)
        self.label_3.setGeometry(QtCore.QRect(390, 55, 246, 17))
        self.label_3.setObjectName("label_3")
        self.imagefracLineEdit0 = QtGui.QLineEdit(LinBckndDialog)
        self.imagefracLineEdit0.setGeometry(QtCore.QRect(0, 85, 376, 27))
        self.imagefracLineEdit0.setObjectName("imagefracLineEdit0")
        self.imagefracLineEdit1 = QtGui.QLineEdit(LinBckndDialog)
        self.imagefracLineEdit1.setGeometry(QtCore.QRect(0, 125, 376, 27))
        self.imagefracLineEdit1.setObjectName("imagefracLineEdit1")
        self.imageComboBox1 = QtGui.QComboBox(LinBckndDialog)
        self.imageComboBox1.setGeometry(QtCore.QRect(385, 120, 346, 31))
        self.imageComboBox1.setObjectName("imageComboBox1")
        self.precisionSpinBox = QtGui.QDoubleSpinBox(LinBckndDialog)
        self.precisionSpinBox.setGeometry(QtCore.QRect(285, 180, 76, 27))
        self.precisionSpinBox.setDecimals(3)
        self.precisionSpinBox.setSingleStep(0.01)
        self.precisionSpinBox.setProperty("value", QtCore.QVariant(0.01))
        self.precisionSpinBox.setObjectName("precisionSpinBox")
        self.label_4 = QtGui.QLabel(LinBckndDialog)
        self.label_4.setGeometry(QtCore.QRect(30, 185, 251, 17))
        self.label_4.setObjectName("label_4")
        self.zerofracSpinBox = QtGui.QDoubleSpinBox(LinBckndDialog)
        self.zerofracSpinBox.setGeometry(QtCore.QRect(285, 215, 76, 27))
        self.zerofracSpinBox.setDecimals(3)
        self.zerofracSpinBox.setSingleStep(0.01)
        self.zerofracSpinBox.setProperty("value", QtCore.QVariant(0.05))
        self.zerofracSpinBox.setObjectName("zerofracSpinBox")
        self.label_5 = QtGui.QLabel(LinBckndDialog)
        self.label_5.setGeometry(QtCore.QRect(80, 220, 206, 17))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(LinBckndDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), LinBckndDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), LinBckndDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LinBckndDialog)

    def retranslateUi(self, LinBckndDialog):
        LinBckndDialog.setWindowTitle(QtGui.QApplication.translate("LinBckndDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LinBckndDialog", "intensity rank to use for mean intensity calibration:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LinBckndDialog", "trial background weights for search algorithm:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("LinBckndDialog", "background images:", None, QtGui.QApplication.UnicodeUTF8))
        self.imagefracLineEdit0.setText(QtGui.QApplication.translate("LinBckndDialog", "0.00001, 0.1, 0.4, 0.6, 0.75, 0.88, 0.96, 1.05, 1.2, 1.8", None, QtGui.QApplication.UnicodeUTF8))
        self.imagefracLineEdit1.setText(QtGui.QApplication.translate("LinBckndDialog", "0.00001, 0.1, 0.4, 0.6, 0.75, 0.88, 0.96, 1.05, 1.2, 1.8", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("LinBckndDialog", "precision for final background weights:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("LinBckndDialog", "fraction of pixels to be zeroed:", None, QtGui.QApplication.UnicodeUTF8))

