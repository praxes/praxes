# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XpWatcher.ui'
#
# Created: Thu Jul 26 17:41:05 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_XPrun(object):
    def setupUi(self, XPrun):
        XPrun.setObjectName("XPrun")
        XPrun.resize(QtCore.QSize(QtCore.QRect(0,0,741,689).size()).expandedTo(XPrun.minimumSizeHint()))

        self.main = QtGui.QWidget(XPrun)
        self.main.setObjectName("main")

        self.MaxVal = QtGui.QSlider(self.main)
        self.MaxVal.setGeometry(QtCore.QRect(130,180,25,161))
        self.MaxVal.setOrientation(QtCore.Qt.Vertical)
        self.MaxVal.setTickPosition(QtGui.QSlider.TicksAbove)
        self.MaxVal.setObjectName("MaxVal")

        self.label = QtGui.QLabel(self.main)
        self.label.setGeometry(QtCore.QRect(120,160,62,20))
        self.label.setObjectName("label")

        self.MinVal = QtGui.QSlider(self.main)
        self.MinVal.setGeometry(QtCore.QRect(50,180,25,161))
        self.MinVal.setOrientation(QtCore.Qt.Vertical)
        self.MinVal.setTickPosition(QtGui.QSlider.TicksBelow)
        self.MinVal.setObjectName("MinVal")

        self.MinValSpin = QtGui.QSpinBox(self.main)
        self.MinValSpin.setGeometry(QtCore.QRect(40,350,51,23))
        self.MinValSpin.setObjectName("MinValSpin")

        self.MinValSpin1 = QtGui.QSpinBox(self.main)
        self.MinValSpin1.setGeometry(QtCore.QRect(120,350,46,23))
        self.MinValSpin1.setObjectName("MinValSpin1")

        self.Run = QtGui.QPushButton(self.main)
        self.Run.setGeometry(QtCore.QRect(50,420,111,41))
        self.Run.setObjectName("Run")

        self.Pause = QtGui.QPushButton(self.main)
        self.Pause.setGeometry(QtCore.QRect(50,480,111,41))
        self.Pause.setObjectName("Pause")

        self.SaveImage = QtGui.QPushButton(self.main)
        self.SaveImage.setGeometry(QtCore.QRect(50,540,111,41))
        self.SaveImage.setObjectName("SaveImage")

        self.label_12 = QtGui.QLabel(self.main)
        self.label_12.setGeometry(QtCore.QRect(50,20,111,16))
        self.label_12.setObjectName("label_12")

        self.label_2 = QtGui.QLabel(self.main)
        self.label_2.setGeometry(QtCore.QRect(30,160,59,20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtGui.QLabel(self.main)
        self.label_3.setGeometry(QtCore.QRect(60,90,91,20))
        self.label_3.setObjectName("label_3")

        self.ElementSelect = QtGui.QComboBox(self.main)
        self.ElementSelect.setGeometry(QtCore.QRect(30,40,141,22))
        self.ElementSelect.setObjectName("ElementSelect")

        self.ElementShell = QtGui.QComboBox(self.main)
        self.ElementShell.setGeometry(QtCore.QRect(31,110,141,22))
        self.ElementShell.setObjectName("ElementShell")

        self.ElementText = QtGui.QLineEdit(self.main)
        self.ElementText.setGeometry(QtCore.QRect(30,60,141,24))
        self.ElementText.setObjectName("ElementText")

        self.ImageFrame = QtGui.QTabWidget(self.main)
        self.ImageFrame.setGeometry(QtCore.QRect(190,20,541,571))
        self.ImageFrame.setObjectName("ImageFrame")

        self.one = QtGui.QWidget()
        self.one.setObjectName("one")

        self.Message = QtGui.QLabel(self.one)
        self.Message.setGeometry(QtCore.QRect(140,190,281,111))
        self.Message.setObjectName("Message")
        self.ImageFrame.addTab(self.one,"")
        XPrun.setCentralWidget(self.main)

        self.Bar = QtGui.QMenuBar(XPrun)
        self.Bar.setGeometry(QtCore.QRect(0,0,741,28))
        self.Bar.setDefaultUp(False)
        self.Bar.setObjectName("Bar")
        XPrun.setMenuBar(self.Bar)
        self.label.setBuddy(self.MaxVal)
        self.label_2.setBuddy(self.MinVal)

        self.retranslateUi(XPrun)
        self.ImageFrame.setCurrentIndex(0)
        QtCore.QObject.connect(self.MinVal,QtCore.SIGNAL("valueChanged(int)"),self.MinValSpin.setValue)
        QtCore.QObject.connect(self.MaxVal,QtCore.SIGNAL("valueChanged(int)"),self.MinValSpin.setValue)
        QtCore.QMetaObject.connectSlotsByName(XPrun)

    def retranslateUi(self, XPrun):
        XPrun.setWindowTitle(QtGui.QApplication.translate("XPrun", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("XPrun", "Max Value", None, QtGui.QApplication.UnicodeUTF8))
        self.Run.setText(QtGui.QApplication.translate("XPrun", "Watch Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.Pause.setText(QtGui.QApplication.translate("XPrun", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveImage.setText(QtGui.QApplication.translate("XPrun", "Save Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("XPrun", "Element to Watch", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("XPrun", "Min Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("XPrun", "Element Shell", None, QtGui.QApplication.UnicodeUTF8))
        self.Message.setText(QtGui.QApplication.translate("XPrun", "       Thank you for Using SpectroMicroscoPy\n"
        "    Please Begin a Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.ImageFrame.setTabText(self.ImageFrame.indexOf(self.one), QtGui.QApplication.translate("XPrun", ":)", None, QtGui.QApplication.UnicodeUTF8))

