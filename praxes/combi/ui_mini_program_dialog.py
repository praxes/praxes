# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python_11June2010Release\mini_program_dialog.ui'
#
# Created: Fri Jun 18 10:18:00 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mini_program_dialog(object):
    def setupUi(self, mini_program_dialog):
        mini_program_dialog.setObjectName("mini_program_dialog")
        mini_program_dialog.resize(902, 452)
        self.buttonBox = QtGui.QDialogButtonBox(mini_program_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(550, 10, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.opentxtPushButton = QtGui.QPushButton(mini_program_dialog)
        self.opentxtPushButton.setGeometry(QtCore.QRect(20, 10, 251, 24))
        self.opentxtPushButton.setObjectName("opentxtPushButton")
        self.appendPushButton = QtGui.QPushButton(mini_program_dialog)
        self.appendPushButton.setGeometry(QtCore.QRect(280, 10, 241, 24))
        self.appendPushButton.setObjectName("appendPushButton")
        self.programComboBox = QtGui.QComboBox(mini_program_dialog)
        self.programComboBox.setGeometry(QtCore.QRect(10, 50, 881, 401))
        self.programComboBox.setObjectName("programComboBox")

        self.retranslateUi(mini_program_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), mini_program_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), mini_program_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(mini_program_dialog)

    def retranslateUi(self, mini_program_dialog):
        mini_program_dialog.setWindowTitle(QtGui.QApplication.translate("mini_program_dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.opentxtPushButton.setText(QtGui.QApplication.translate("mini_program_dialog", "open different program database txt", None, QtGui.QApplication.UnicodeUTF8))
        self.appendPushButton.setText(QtGui.QApplication.translate("mini_program_dialog", "append miniprogram", None, QtGui.QApplication.UnicodeUTF8))
        self.programComboBox.setToolTip(QtGui.QApplication.translate("mini_program_dialog", "This is the list of \"mini programs\" in the default .txt database, or that opened with the \"open different ...\" button. This is a menu where each possible entry is a set of commands. You can append as many sets of commands as you like using the \"append miniprogram\" button - these commands will be in the queue in the main menu window.", None, QtGui.QApplication.UnicodeUTF8))

