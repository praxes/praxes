# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\spatial_phases_menu.ui'
#
# Created: Mon Jun 14 16:20:39 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_spatialphasesDialog(object):
    def setupUi(self, spatialphasesDialog):
        spatialphasesDialog.setObjectName("spatialphasesDialog")
        spatialphasesDialog.resize(364, 112)
        self.buttonBox = QtGui.QDialogButtonBox(spatialphasesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 70, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtGui.QLabel(spatialphasesDialog)
        self.label_2.setGeometry(QtCore.QRect(5, 0, 136, 71))
        self.label_2.setObjectName("label_2")
        self.critblobsepSpinBox = QtGui.QDoubleSpinBox(spatialphasesDialog)
        self.critblobsepSpinBox.setGeometry(QtCore.QRect(20, 70, 71, 22))
        self.critblobsepSpinBox.setMaximum(100.0)
        self.critblobsepSpinBox.setSingleStep(0.1)
        self.critblobsepSpinBox.setProperty("value", QtCore.QVariant(1.0))
        self.critblobsepSpinBox.setObjectName("critblobsepSpinBox")
        self.label_5 = QtGui.QLabel(spatialphasesDialog)
        self.label_5.setGeometry(QtCore.QRect(120, 10, 70, 20))
        self.label_5.setObjectName("label_5")
        self.numqqpksSpinBox = QtGui.QSpinBox(spatialphasesDialog)
        self.numqqpksSpinBox.setGeometry(QtCore.QRect(130, 30, 42, 22))
        self.numqqpksSpinBox.setProperty("value", QtCore.QVariant(3))
        self.numqqpksSpinBox.setObjectName("numqqpksSpinBox")
        self.numptsSpinBox = QtGui.QSpinBox(spatialphasesDialog)
        self.numptsSpinBox.setGeometry(QtCore.QRect(235, 40, 42, 22))
        self.numptsSpinBox.setProperty("value", QtCore.QVariant(3))
        self.numptsSpinBox.setObjectName("numptsSpinBox")
        self.label_6 = QtGui.QLabel(spatialphasesDialog)
        self.label_6.setGeometry(QtCore.QRect(200, 10, 141, 28))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(spatialphasesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), spatialphasesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), spatialphasesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(spatialphasesDialog)

    def retranslateUi(self, spatialphasesDialog):
        spatialphasesDialog.setWindowTitle(QtGui.QApplication.translate("spatialphasesDialog", "Select values for association", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("spatialphasesDialog", "crit spatial\n"
"separation for\n"
"cts blob\n"
"(units=xgrid sep)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("spatialphasesDialog", "min num qqpks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("spatialphasesDialog", "min num substrate\n"
"points in blob", None, QtGui.QApplication.UnicodeUTF8))

