# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\peak_1d.ui'
#
# Created: Mon Jun 14 16:20:38 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_peak1dDialog(object):
    def setupUi(self, peak1dDialog):
        peak1dDialog.setObjectName("peak1dDialog")
        peak1dDialog.resize(541, 120)
        self.buttonBox = QtGui.QDialogButtonBox(peak1dDialog)
        self.buttonBox.setGeometry(QtCore.QRect(270, 90, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout = QtGui.QWidget(peak1dDialog)
        self.horizontalLayout.setGeometry(QtCore.QRect(10, 10, 311, 51))
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName("hboxlayout")
        self.label_2 = QtGui.QLabel(self.horizontalLayout)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)
        self.label = QtGui.QLabel(self.horizontalLayout)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.label_3 = QtGui.QLabel(self.horizontalLayout)
        self.label_3.setObjectName("label_3")
        self.hboxlayout.addWidget(self.label_3)
        self.horizontalLayout_2 = QtGui.QWidget(peak1dDialog)
        self.horizontalLayout_2.setGeometry(QtCore.QRect(10, 60, 311, 31))
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.hboxlayout1 = QtGui.QHBoxLayout(self.horizontalLayout_2)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.curve_spinBox = QtGui.QSpinBox(self.horizontalLayout_2)
        self.curve_spinBox.setMaximum(100000000)
        self.curve_spinBox.setSingleStep(10000)
        self.curve_spinBox.setProperty("value", QtCore.QVariant(16))
        self.curve_spinBox.setObjectName("curve_spinBox")
        self.hboxlayout1.addWidget(self.curve_spinBox)
        self.cts_spinBox = QtGui.QSpinBox(self.horizontalLayout_2)
        self.cts_spinBox.setMaximum(1000000)
        self.cts_spinBox.setSingleStep(1000)
        self.cts_spinBox.setProperty("value", QtCore.QVariant(20))
        self.cts_spinBox.setObjectName("cts_spinBox")
        self.hboxlayout1.addWidget(self.cts_spinBox)
        self.clust_spinBox = QtGui.QDoubleSpinBox(self.horizontalLayout_2)
        self.clust_spinBox.setSingleStep(0.1)
        self.clust_spinBox.setProperty("value", QtCore.QVariant(0.5))
        self.clust_spinBox.setObjectName("clust_spinBox")
        self.hboxlayout1.addWidget(self.clust_spinBox)
        self.typeComboBox = QtGui.QComboBox(peak1dDialog)
        self.typeComboBox.setGeometry(QtCore.QRect(340, 30, 191, 22))
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeLabel = QtGui.QLabel(peak1dDialog)
        self.typeLabel.setGeometry(QtCore.QRect(340, 10, 46, 14))
        self.typeLabel.setObjectName("typeLabel")

        self.retranslateUi(peak1dDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), peak1dDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), peak1dDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(peak1dDialog)

    def retranslateUi(self, peak1dDialog):
        peak1dDialog.setWindowTitle(QtGui.QApplication.translate("peak1dDialog", "select values for 1d peak search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("peak1dDialog", "max negative\n"
"curvature\n"
"(counts nm^2)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("peak1dDialog", "minimum\n"
"counts", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("peak1dDialog", "q cluster radius\n"
"(1/nm)", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLabel.setText(QtGui.QApplication.translate("peak1dDialog", "select", None, QtGui.QApplication.UnicodeUTF8))

