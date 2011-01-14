# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\import_image.ui'
#
# Created: Mon Jun 14 16:20:37 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_importDialog(object):
    def setupUi(self, importDialog):
        importDialog.setObjectName("importDialog")
        importDialog.resize(523, 128)
        icon = QtGui.QIcon()
        icon.addFile("CUIcon.png")
        importDialog.setWindowIcon(icon)
        self.groupLabel = QtGui.QLabel(importDialog)
        self.groupLabel.setGeometry(QtCore.QRect(10, 74, 79, 20))
        self.groupLabel.setObjectName("groupLabel")
        self.groupLineEdit = QtGui.QLineEdit(importDialog)
        self.groupLineEdit.setGeometry(QtCore.QRect(95, 74, 402, 20))
        self.groupLineEdit.setObjectName("groupLineEdit")
        self.buttonBox = QtGui.QDialogButtonBox(importDialog)
        self.buttonBox.setGeometry(QtCore.QRect(332, 100, 165, 26))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.statusLabel = QtGui.QLabel(importDialog)
        self.statusLabel.setGeometry(QtCore.QRect(20, 100, 301, 26))
        self.statusLabel.setObjectName("statusLabel")
        self.widget = QtGui.QWidget(importDialog)
        self.widget.setGeometry(QtCore.QRect(1, 11, 165, 60))
        self.widget.setObjectName("widget")
        self.vboxlayout = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout.setObjectName("vboxlayout")
        self.binaryButton = QtGui.QPushButton(self.widget)
        self.binaryButton.setObjectName("binaryButton")
        self.vboxlayout.addWidget(self.binaryButton)
        self.h5Button = QtGui.QPushButton(self.widget)
        self.h5Button.setObjectName("h5Button")
        self.vboxlayout.addWidget(self.h5Button)
        self.binarynameLabel = QtGui.QLabel(importDialog)
        self.binarynameLabel.setGeometry(QtCore.QRect(172, 12, 349, 27))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.binarynameLabel.setFont(font)
        self.binarynameLabel.setObjectName("binarynameLabel")
        self.h5nameLabel = QtGui.QLabel(importDialog)
        self.h5nameLabel.setGeometry(QtCore.QRect(172, 43, 349, 26))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.h5nameLabel.setFont(font)
        self.h5nameLabel.setObjectName("h5nameLabel")

        self.retranslateUi(importDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), importDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), importDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(importDialog)

    def retranslateUi(self, importDialog):
        importDialog.setWindowTitle(QtGui.QApplication.translate("importDialog", "Select files for importing binary image data to .h5 file", None, QtGui.QApplication.UnicodeUTF8))
        self.groupLabel.setText(QtGui.QApplication.translate("importDialog", "group in .h5 file:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupLineEdit.setText(QtGui.QApplication.translate("importDialog", ".root.XRD.PrimDataset.Raw", None, QtGui.QApplication.UnicodeUTF8))
        self.statusLabel.setStyleSheet(QtGui.QApplication.translate("importDialog", "color:red", None, QtGui.QApplication.UnicodeUTF8))
        self.statusLabel.setText(QtGui.QApplication.translate("importDialog", "File Status", None, QtGui.QApplication.UnicodeUTF8))
        self.binaryButton.setText(QtGui.QApplication.translate("importDialog", "select different binary file", None, QtGui.QApplication.UnicodeUTF8))
        self.h5Button.setText(QtGui.QApplication.translate("importDialog", "select different .h5 save file", None, QtGui.QApplication.UnicodeUTF8))
        self.binarynameLabel.setText(QtGui.QApplication.translate("importDialog", ".dat", None, QtGui.QApplication.UnicodeUTF8))
        self.h5nameLabel.setText(QtGui.QApplication.translate("importDialog", ".h5", None, QtGui.QApplication.UnicodeUTF8))

