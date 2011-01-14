# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\plotsomenu.ui'
#
# Created: Mon Jun 14 16:20:39 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_plotsoDialog(object):
    def setupUi(self, plotsoDialog):
        plotsoDialog.setObjectName("plotsoDialog")
        plotsoDialog.resize(371, 200)
        self.buttonBox = QtGui.QDialogButtonBox(plotsoDialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 130, 343, 26))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.typeComboBox = QtGui.QComboBox(plotsoDialog)
        self.typeComboBox.setGeometry(QtCore.QRect(5, 9, 343, 20))
        self.typeComboBox.setObjectName("typeComboBox")
        self.lowSpinBox = QtGui.QDoubleSpinBox(plotsoDialog)
        self.lowSpinBox.setGeometry(QtCore.QRect(10, 70, 62, 22))
        self.lowSpinBox.setMaximum(999999.0)
        self.lowSpinBox.setObjectName("lowSpinBox")
        self.highSpinBox = QtGui.QDoubleSpinBox(plotsoDialog)
        self.highSpinBox.setGeometry(QtCore.QRect(100, 70, 62, 22))
        self.highSpinBox.setMaximum(99999.0)
        self.highSpinBox.setObjectName("highSpinBox")
        self.label = QtGui.QLabel(plotsoDialog)
        self.label.setGeometry(QtCore.QRect(10, 50, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(plotsoDialog)
        self.label_2.setGeometry(QtCore.QRect(100, 50, 76, 16))
        self.label_2.setObjectName("label_2")
        self.densityCheckBox = QtGui.QCheckBox(plotsoDialog)
        self.densityCheckBox.setGeometry(QtCore.QRect(200, 70, 171, 18))
        self.densityCheckBox.setChecked(False)
        self.densityCheckBox.setObjectName("densityCheckBox")

        self.retranslateUi(plotsoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), plotsoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), plotsoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(plotsoDialog)

    def retranslateUi(self, plotsoDialog):
        plotsoDialog.setWindowTitle(QtGui.QApplication.translate("plotsoDialog", "select XRD dataset", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("plotsoDialog", "low Q val", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("plotsoDialog", "high Q val", None, QtGui.QApplication.UnicodeUTF8))
        self.densityCheckBox.setText(QtGui.QApplication.translate("plotsoDialog", "scale by nmol/cm^2", None, QtGui.QApplication.UnicodeUTF8))

