# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\make_phases_menu.ui'
#
# Created: Mon Jun 14 16:20:38 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_makephasesDialog(object):
    def setupUi(self, makephasesDialog):
        makephasesDialog.setObjectName("makephasesDialog")
        makephasesDialog.resize(364, 112)
        self.buttonBox = QtGui.QDialogButtonBox(makephasesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 70, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtGui.QLabel(makephasesDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 81, 21))
        self.label_2.setObjectName("label_2")
        self.critqqnormSpinBox = QtGui.QDoubleSpinBox(makephasesDialog)
        self.critqqnormSpinBox.setGeometry(QtCore.QRect(10, 40, 101, 22))
        self.critqqnormSpinBox.setMaximum(1.0)
        self.critqqnormSpinBox.setSingleStep(0.1)
        self.critqqnormSpinBox.setProperty("value", QtCore.QVariant(0.7))
        self.critqqnormSpinBox.setObjectName("critqqnormSpinBox")
        self.label_5 = QtGui.QLabel(makephasesDialog)
        self.label_5.setGeometry(QtCore.QRect(120, 20, 111, 20))
        self.label_5.setObjectName("label_5")
        self.numqqpksSpinBox = QtGui.QSpinBox(makephasesDialog)
        self.numqqpksSpinBox.setGeometry(QtCore.QRect(130, 40, 42, 22))
        self.numqqpksSpinBox.setProperty("value", QtCore.QVariant(3))
        self.numqqpksSpinBox.setObjectName("numqqpksSpinBox")
        self.label_6 = QtGui.QLabel(makephasesDialog)
        self.label_6.setGeometry(QtCore.QRect(250, 20, 96, 20))
        self.label_6.setObjectName("label_6")
        self.numipksSpinBox = QtGui.QSpinBox(makephasesDialog)
        self.numipksSpinBox.setGeometry(QtCore.QRect(260, 40, 42, 22))
        self.numipksSpinBox.setProperty("value", QtCore.QVariant(3))
        self.numipksSpinBox.setObjectName("numipksSpinBox")

        self.retranslateUi(makephasesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), makephasesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), makephasesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(makephasesDialog)

    def retranslateUi(self, makephasesDialog):
        makephasesDialog.setWindowTitle(QtGui.QApplication.translate("makephasesDialog", "Select values for association", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("makephasesDialog", "crit qqnorm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("makephasesDialog", "min num qqpks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("makephasesDialog", "min num ipks", None, QtGui.QApplication.UnicodeUTF8))

