# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\qq_params.ui'
#
# Created: Mon Jun 14 16:20:39 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_qqparamDialog(object):
    def setupUi(self, qqparamDialog):
        qqparamDialog.setObjectName("qqparamDialog")
        qqparamDialog.resize(545, 167)
        self.layoutWidget = QtGui.QWidget(qqparamDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 309, 124))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridlayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout.setObjectName("gridlayout")
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4, 0, 0, 1, 2)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.qminSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.qminSpinBox.setMaximum(99999.0)
        self.qminSpinBox.setObjectName("qminSpinBox")
        self.gridlayout.addWidget(self.qminSpinBox, 2, 0, 1, 1)
        self.qmaxSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.qmaxSpinBox.setMaximum(99999.0)
        self.qmaxSpinBox.setObjectName("qmaxSpinBox")
        self.gridlayout.addWidget(self.qmaxSpinBox, 2, 1, 1, 1)
        self.qintSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.qintSpinBox.setMaximum(99999.0)
        self.qintSpinBox.setObjectName("qintSpinBox")
        self.gridlayout.addWidget(self.qintSpinBox, 2, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 3)
        self.typeComboBox = QtGui.QComboBox(qqparamDialog)
        self.typeComboBox.setGeometry(QtCore.QRect(335, 35, 191, 22))
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeLabel = QtGui.QLabel(qqparamDialog)
        self.typeLabel.setGeometry(QtCore.QRect(335, 15, 191, 16))
        self.typeLabel.setObjectName("typeLabel")

        self.retranslateUi(qqparamDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), qqparamDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), qqparamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(qqparamDialog)

    def retranslateUi(self, qqparamDialog):
        qqparamDialog.setWindowTitle(QtGui.QApplication.translate("qqparamDialog", "Enter qq calculation parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("qqparamDialog", "ENTER ALL VALUES IN 2pi/nm\n"
"q interval should not be changed", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("qqparamDialog", "q min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("qqparamDialog", "q max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("qqparamDialog", "q interval", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLabel.setText(QtGui.QApplication.translate("qqparamDialog", "select", None, QtGui.QApplication.UnicodeUTF8))

