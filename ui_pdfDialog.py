# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python_11June2010Release\pdfDialog.ui'
#
# Created: Fri Jun 18 10:18:01 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_pdfDialog(object):
    def setupUi(self, pdfDialog):
        pdfDialog.setObjectName("pdfDialog")
        pdfDialog.resize(462, 158)
        self.buttonBox = QtGui.QDialogButtonBox(pdfDialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 110, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.colorlineEdit = QtGui.QLineEdit(pdfDialog)
        self.colorlineEdit.setGeometry(QtCore.QRect(220, 80, 151, 20))
        self.colorlineEdit.setObjectName("colorlineEdit")
        self.pdfcomboBox = QtGui.QComboBox(pdfDialog)
        self.pdfcomboBox.setGeometry(QtCore.QRect(10, 30, 261, 22))
        self.pdfcomboBox.setObjectName("pdfcomboBox")
        self.labellineEdit = QtGui.QLineEdit(pdfDialog)
        self.labellineEdit.setGeometry(QtCore.QRect(10, 80, 181, 20))
        self.labellineEdit.setObjectName("labellineEdit")
        self.heightSpinBox = QtGui.QDoubleSpinBox(pdfDialog)
        self.heightSpinBox.setGeometry(QtCore.QRect(315, 30, 81, 22))
        self.heightSpinBox.setMinimum(-999999.0)
        self.heightSpinBox.setMaximum(99999.0)
        self.heightSpinBox.setProperty("value", QtCore.QVariant(0.0))
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.label = QtGui.QLabel(pdfDialog)
        self.label.setGeometry(QtCore.QRect(280, 10, 166, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(pdfDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 171, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(pdfDialog)
        self.label_3.setGeometry(QtCore.QRect(220, 60, 161, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(pdfDialog)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 201, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(pdfDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), pdfDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), pdfDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(pdfDialog)

    def retranslateUi(self, pdfDialog):
        pdfDialog.setWindowTitle(QtGui.QApplication.translate("pdfDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.colorlineEdit.setToolTip(QtGui.QApplication.translate("pdfDialog", "see matplotlib documentation, do not include quotation marks", None, QtGui.QApplication.UnicodeUTF8))
        self.pdfcomboBox.setToolTip(QtGui.QApplication.translate("pdfDialog", "These are the Powder Diffraction File names given in the .txt database", None, QtGui.QApplication.UnicodeUTF8))
        self.labellineEdit.setToolTip(QtGui.QApplication.translate("pdfDialog", "Where applicable, this label will appear on the graph.", None, QtGui.QApplication.UnicodeUTF8))
        self.heightSpinBox.setToolTip(QtGui.QApplication.translate("pdfDialog", "The height of the largest peak in the PDF entry, in diffraction intensity units.\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("pdfDialog", "height (0 for autoscale)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("pdfDialog", "Choose a PDF entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("pdfDialog", "matplotlib color string", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("pdfDialog", "label to appear in upper left", None, QtGui.QApplication.UnicodeUTF8))

