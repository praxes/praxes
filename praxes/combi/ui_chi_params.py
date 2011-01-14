# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\chi_params.ui'
#
# Created: Mon Jun 14 16:20:36 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_chiparamDialog(object):
    def setupUi(self, chiparamDialog):
        chiparamDialog.setObjectName("chiparamDialog")
        chiparamDialog.resize(312, 119)
        self.layoutWidget = QtGui.QWidget(chiparamDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(12, 4, 293, 108))
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
        self.chiminSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.chiminSpinBox.setMaximum(99999.0)
        self.chiminSpinBox.setObjectName("chiminSpinBox")
        self.gridlayout.addWidget(self.chiminSpinBox, 2, 0, 1, 1)
        self.chimaxSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.chimaxSpinBox.setMaximum(99999.0)
        self.chimaxSpinBox.setObjectName("chimaxSpinBox")
        self.gridlayout.addWidget(self.chimaxSpinBox, 2, 1, 1, 1)
        self.chiintSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.chiintSpinBox.setMaximum(99999.0)
        self.chiintSpinBox.setProperty("value", QtCore.QVariant(0.1))
        self.chiintSpinBox.setObjectName("chiintSpinBox")
        self.gridlayout.addWidget(self.chiintSpinBox, 2, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 3)

        self.retranslateUi(chiparamDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), chiparamDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), chiparamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(chiparamDialog)

    def retranslateUi(self, chiparamDialog):
        chiparamDialog.setWindowTitle(QtGui.QApplication.translate("chiparamDialog", "Enter chi map parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("chiparamDialog", "ENTER ALL VALUES IN degrees", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("chiparamDialog", "chi min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("chiparamDialog", "chi max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("chiparamDialog", "chi interval", None, QtGui.QApplication.UnicodeUTF8))

