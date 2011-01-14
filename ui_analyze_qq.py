# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\analyze_qq.ui'
#
# Created: Mon Jun 14 16:20:35 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_qqanalysisDialog(object):
    def setupUi(self, qqanalysisDialog):
        qqanalysisDialog.setObjectName("qqanalysisDialog")
        qqanalysisDialog.resize(331, 126)
        self.buttonBox = QtGui.QDialogButtonBox(qqanalysisDialog)
        self.buttonBox.setGeometry(QtCore.QRect(60, 90, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout = QtGui.QWidget(qqanalysisDialog)
        self.horizontalLayout.setGeometry(QtCore.QRect(10, 10, 311, 44))
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
        self.horizontalLayout_2 = QtGui.QWidget(qqanalysisDialog)
        self.horizontalLayout_2.setGeometry(QtCore.QRect(10, 60, 311, 31))
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.hboxlayout1 = QtGui.QHBoxLayout(self.horizontalLayout_2)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.curve_spinBox = QtGui.QSpinBox(self.horizontalLayout_2)
        self.curve_spinBox.setMaximum(100000000)
        self.curve_spinBox.setSingleStep(10000)
        self.curve_spinBox.setProperty("value", QtCore.QVariant(50000))
        self.curve_spinBox.setObjectName("curve_spinBox")
        self.hboxlayout1.addWidget(self.curve_spinBox)
        self.cts_spinBox = QtGui.QSpinBox(self.horizontalLayout_2)
        self.cts_spinBox.setMaximum(1000000)
        self.cts_spinBox.setSingleStep(1000)
        self.cts_spinBox.setProperty("value", QtCore.QVariant(500))
        self.cts_spinBox.setObjectName("cts_spinBox")
        self.hboxlayout1.addWidget(self.cts_spinBox)
        self.clust_spinBox = QtGui.QDoubleSpinBox(self.horizontalLayout_2)
        self.clust_spinBox.setSingleStep(0.1)
        self.clust_spinBox.setProperty("value", QtCore.QVariant(0.5))
        self.clust_spinBox.setObjectName("clust_spinBox")
        self.hboxlayout1.addWidget(self.clust_spinBox)

        self.retranslateUi(qqanalysisDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), qqanalysisDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), qqanalysisDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(qqanalysisDialog)

    def retranslateUi(self, qqanalysisDialog):
        qqanalysisDialog.setWindowTitle(QtGui.QApplication.translate("qqanalysisDialog", "select values for analysis of qq", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("qqanalysisDialog", "min negative\n"
"curvature\n"
"(counts^2 nm^2)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("qqanalysisDialog", "minimum\n"
"counts^2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("qqanalysisDialog", "q cluster radius\n"
"(1/nm)", None, QtGui.QApplication.UnicodeUTF8))

