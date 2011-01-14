# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\associate_pkqq.ui'
#
# Created: Mon Jun 14 16:20:35 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_peakqqassociationDialog(object):
    def setupUi(self, peakqqassociationDialog):
        peakqqassociationDialog.setObjectName("peakqqassociationDialog")
        peakqqassociationDialog.resize(387, 112)
        self.buttonBox = QtGui.QDialogButtonBox(peakqqassociationDialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 70, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.qqnorm_spinBox = QtGui.QDoubleSpinBox(peakqqassociationDialog)
        self.qqnorm_spinBox.setGeometry(QtCore.QRect(290, 40, 61, 22))
        self.qqnorm_spinBox.setSingleStep(0.1)
        self.qqnorm_spinBox.setProperty("value", QtCore.QVariant(0.7))
        self.qqnorm_spinBox.setObjectName("qqnorm_spinBox")
        self.label = QtGui.QLabel(peakqqassociationDialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(peakqqassociationDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 51, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(peakqqassociationDialog)
        self.label_3.setGeometry(QtCore.QRect(290, 10, 73, 31))
        self.label_3.setObjectName("label_3")
        self.qqsig_spinBox = QtGui.QDoubleSpinBox(peakqqassociationDialog)
        self.qqsig_spinBox.setGeometry(QtCore.QRect(10, 40, 71, 22))
        self.qqsig_spinBox.setSingleStep(0.1)
        self.qqsig_spinBox.setProperty("value", QtCore.QVariant(2.0))
        self.qqsig_spinBox.setObjectName("qqsig_spinBox")
        self.qalloyfrac_spinBox = QtGui.QDoubleSpinBox(peakqqassociationDialog)
        self.qalloyfrac_spinBox.setGeometry(QtCore.QRect(170, 40, 71, 22))
        self.qalloyfrac_spinBox.setDecimals(3)
        self.qalloyfrac_spinBox.setSingleStep(0.01)
        self.qalloyfrac_spinBox.setProperty("value", QtCore.QVariant(0.05))
        self.qalloyfrac_spinBox.setObjectName("qalloyfrac_spinBox")
        self.label_4 = QtGui.QLabel(peakqqassociationDialog)
        self.label_4.setGeometry(QtCore.QRect(180, 10, 41, 28))
        self.label_4.setObjectName("label_4")
        self.qanisofrac_spinBox = QtGui.QDoubleSpinBox(peakqqassociationDialog)
        self.qanisofrac_spinBox.setGeometry(QtCore.QRect(90, 40, 71, 22))
        self.qanisofrac_spinBox.setDecimals(3)
        self.qanisofrac_spinBox.setSingleStep(0.01)
        self.qanisofrac_spinBox.setProperty("value", QtCore.QVariant(0.01))
        self.qanisofrac_spinBox.setObjectName("qanisofrac_spinBox")
        self.label_5 = QtGui.QLabel(peakqqassociationDialog)
        self.label_5.setGeometry(QtCore.QRect(100, 10, 61, 28))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(peakqqassociationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), peakqqassociationDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), peakqqassociationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(peakqqassociationDialog)

    def retranslateUi(self, peakqqassociationDialog):
        peakqqassociationDialog.setWindowTitle(QtGui.QApplication.translate("peakqqassociationDialog", "Select values for association", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("peakqqassociationDialog", "critical separation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("peakqqassociationDialog", "qq-sigma", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("peakqqassociationDialog", "critical\n"
"qqnorm value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("peakqqassociationDialog", "q alloy\n"
"fraction", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("peakqqassociationDialog", "q anisotropic\n"
"fraction", None, QtGui.QApplication.UnicodeUTF8))

