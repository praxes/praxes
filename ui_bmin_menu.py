# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python_11June2010Release\bmin_menu.ui'
#
# Created: Wed Jun 16 12:45:38 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_bmin_menu(object):
    def setupUi(self, bmin_menu):
        bmin_menu.setObjectName("bmin_menu")
        bmin_menu.resize(316, 112)
        self.buttonBox = QtGui.QDialogButtonBox(bmin_menu)
        self.buttonBox.setGeometry(QtCore.QRect(50, 70, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtGui.QLabel(bmin_menu)
        self.label_2.setGeometry(QtCore.QRect(90, 10, 181, 28))
        self.label_2.setObjectName("label_2")
        self.bminpercSpinBox = QtGui.QDoubleSpinBox(bmin_menu)
        self.bminpercSpinBox.setGeometry(QtCore.QRect(120, 40, 71, 22))
        self.bminpercSpinBox.setDecimals(3)
        self.bminpercSpinBox.setMaximum(1.0)
        self.bminpercSpinBox.setSingleStep(0.01)
        self.bminpercSpinBox.setProperty("value", QtCore.QVariant(0.05))
        self.bminpercSpinBox.setObjectName("bminpercSpinBox")

        self.retranslateUi(bmin_menu)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), bmin_menu.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), bmin_menu.reject)
        QtCore.QMetaObject.connectSlotsByName(bmin_menu)

    def retranslateUi(self, bmin_menu):
        bmin_menu.setWindowTitle(QtGui.QApplication.translate("bmin_menu", "Select values for association", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("bmin_menu", "percentile fraction of\n"
"counts for each pixel", None, QtGui.QApplication.UnicodeUTF8))
        self.bminpercSpinBox.setToolTip(QtGui.QApplication.translate("bmin_menu", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This is the fractional percentile rank for calculating the bmin image. For each detetector pixel, the intensity from each diffraciton image will be ordered and the value at the specified percentile rank will be chosen. In the background-subtracted images, the intensities below this chosen value will be zero.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

