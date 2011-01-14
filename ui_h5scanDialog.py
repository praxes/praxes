# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python_11June2010Release\h5scanDialog.ui'
#
# Created: Fri Jun 18 10:17:59 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_h5scanDialog(object):
    def setupUi(self, h5scanDialog):
        h5scanDialog.setObjectName("h5scanDialog")
        h5scanDialog.resize(566, 82)
        self.buttonBox = QtGui.QDialogButtonBox(h5scanDialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 40, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.scanComboBox = QtGui.QComboBox(h5scanDialog)
        self.scanComboBox.setGeometry(QtCore.QRect(10, 10, 531, 22))
        self.scanComboBox.setObjectName("scanComboBox")

        self.retranslateUi(h5scanDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), h5scanDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), h5scanDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(h5scanDialog)

    def retranslateUi(self, h5scanDialog):
        h5scanDialog.setWindowTitle(QtGui.QApplication.translate("h5scanDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.scanComboBox.setToolTip(QtGui.QApplication.translate("h5scanDialog", "This is the list of spec commands identified as relevant for combi XRD/XRF analysis. The format is <spec group name>:<spec command> and, for eaxmple, \"tseries\" commands are no included in this list.", None, QtGui.QApplication.UnicodeUTF8))

