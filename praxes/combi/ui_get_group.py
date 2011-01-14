# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\get_group.ui'
#
# Created: Mon Jun 14 16:20:36 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_getgroupDialog(object):
    def setupUi(self, getgroupDialog):
        getgroupDialog.setObjectName("getgroupDialog")
        getgroupDialog.resize(355, 69)
        self.buttonBox = QtGui.QDialogButtonBox(getgroupDialog)
        self.buttonBox.setGeometry(QtCore.QRect(5, 35, 343, 26))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupsComboBox = QtGui.QComboBox(getgroupDialog)
        self.groupsComboBox.setGeometry(QtCore.QRect(5, 9, 343, 20))
        self.groupsComboBox.setObjectName("groupsComboBox")

        self.retranslateUi(getgroupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), getgroupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), getgroupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(getgroupDialog)

    def retranslateUi(self, getgroupDialog):
        getgroupDialog.setWindowTitle(QtGui.QApplication.translate("getgroupDialog", "select XRD dataset", None, QtGui.QApplication.UnicodeUTF8))

