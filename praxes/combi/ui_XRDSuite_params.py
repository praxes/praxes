# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\XRDSuite_params.ui'
#
# Created: Mon Jun 14 16:20:40 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_XRDSuite_params(object):
    def setupUi(self, XRDSuite_params):
        XRDSuite_params.setObjectName("XRDSuite_params")
        XRDSuite_params.resize(446, 132)
        self.imtypeComboBox = QtGui.QComboBox(XRDSuite_params)
        self.imtypeComboBox.setGeometry(QtCore.QRect(240, 30, 191, 22))
        self.imtypeComboBox.setObjectName("imtypeComboBox")
        self.imtypeLabel = QtGui.QLabel(XRDSuite_params)
        self.imtypeLabel.setGeometry(QtCore.QRect(240, 10, 191, 16))
        self.imtypeLabel.setObjectName("imtypeLabel")
        self.xtypeComboBox = QtGui.QComboBox(XRDSuite_params)
        self.xtypeComboBox.setGeometry(QtCore.QRect(10, 30, 201, 20))
        self.xtypeComboBox.setObjectName("xtypeComboBox")
        self.xtypeLabel = QtGui.QLabel(XRDSuite_params)
        self.xtypeLabel.setGeometry(QtCore.QRect(10, 10, 201, 16))
        self.xtypeLabel.setObjectName("xtypeLabel")
        self.scaleCheckBox = QtGui.QCheckBox(XRDSuite_params)
        self.scaleCheckBox.setGeometry(QtCore.QRect(260, 70, 171, 18))
        self.scaleCheckBox.setChecked(True)
        self.scaleCheckBox.setObjectName("scaleCheckBox")
        self.qmaxSpinBox = QtGui.QDoubleSpinBox(XRDSuite_params)
        self.qmaxSpinBox.setGeometry(QtCore.QRect(120, 70, 75, 20))
        self.qmaxSpinBox.setMaximum(99999.0)
        self.qmaxSpinBox.setObjectName("qmaxSpinBox")
        self.label = QtGui.QLabel(XRDSuite_params)
        self.label.setGeometry(QtCore.QRect(38, 50, 76, 20))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(XRDSuite_params)
        self.label_2.setGeometry(QtCore.QRect(120, 50, 75, 20))
        self.label_2.setObjectName("label_2")
        self.buttonBox = QtGui.QDialogButtonBox(XRDSuite_params)
        self.buttonBox.setGeometry(QtCore.QRect(250, 100, 183, 25))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.qminSpinBox = QtGui.QDoubleSpinBox(XRDSuite_params)
        self.qminSpinBox.setGeometry(QtCore.QRect(38, 71, 76, 20))
        self.qminSpinBox.setMaximum(99999.0)
        self.qminSpinBox.setObjectName("qminSpinBox")
        self.CompComboBox = QtGui.QComboBox(XRDSuite_params)
        self.CompComboBox.setGeometry(QtCore.QRect(50, 100, 151, 24))
        self.CompComboBox.setObjectName("CompComboBox")
        self.CompComboBox.addItem(QtCore.QString())
        self.CompComboBox.addItem(QtCore.QString())
        self.CompComboBox.addItem(QtCore.QString())

        self.retranslateUi(XRDSuite_params)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), XRDSuite_params.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), XRDSuite_params.reject)
        QtCore.QMetaObject.connectSlotsByName(XRDSuite_params)

    def retranslateUi(self, XRDSuite_params):
        XRDSuite_params.setWindowTitle(QtGui.QApplication.translate("XRDSuite_params", "Enter qq calculation parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.imtypeLabel.setText(QtGui.QApplication.translate("XRDSuite_params", "select", None, QtGui.QApplication.UnicodeUTF8))
        self.xtypeLabel.setText(QtGui.QApplication.translate("XRDSuite_params", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleCheckBox.setText(QtGui.QApplication.translate("XRDSuite_params", "scale by nmol/cm^2", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("XRDSuite_params", "q min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("XRDSuite_params", "q max", None, QtGui.QApplication.UnicodeUTF8))
        self.CompComboBox.setItemText(0, QtGui.QApplication.translate("XRDSuite_params", "Dep Prof Comps", None, QtGui.QApplication.UnicodeUTF8))
        self.CompComboBox.setItemText(1, QtGui.QApplication.translate("XRDSuite_params", "XRF Comps", None, QtGui.QApplication.UnicodeUTF8))
        self.CompComboBox.setItemText(2, QtGui.QApplication.translate("XRDSuite_params", "none", None, QtGui.QApplication.UnicodeUTF8))

