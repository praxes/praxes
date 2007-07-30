# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XpMaster.ui'
#
# Created: Mon Jul 30 17:16:20 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_XpMaster(object):
    def setupUi(self, XpMaster):
        XpMaster.setObjectName("XpMaster")
        XpMaster.resize(QtCore.QSize(QtCore.QRect(0,0,1272,762).size()).expandedTo(XpMaster.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(XpMaster.sizePolicy().hasHeightForWidth())
        XpMaster.setSizePolicy(sizePolicy)
        XpMaster.setSizeIncrement(QtCore.QSize(1,1))

        self.XpCentral = QtGui.QWidget(XpMaster)
        self.XpCentral.setObjectName("XpCentral")

        self.MotorBox = QtGui.QFrame(self.XpCentral)
        self.MotorBox.setGeometry(QtCore.QRect(0,0,331,741))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MotorBox.sizePolicy().hasHeightForWidth())
        self.MotorBox.setSizePolicy(sizePolicy)
        self.MotorBox.setFrameShape(QtGui.QFrame.StyledPanel)
        self.MotorBox.setFrameShadow(QtGui.QFrame.Raised)
        self.MotorBox.setObjectName("MotorBox")

        self.MotorLabels = QtGui.QFrame(self.MotorBox)
        self.MotorLabels.setGeometry(QtCore.QRect(0,310,61,321))
        self.MotorLabels.setFrameShape(QtGui.QFrame.StyledPanel)
        self.MotorLabels.setFrameShadow(QtGui.QFrame.Raised)
        self.MotorLabels.setObjectName("MotorLabels")

        self.label_13 = QtGui.QLabel(self.MotorLabels)
        self.label_13.setGeometry(QtCore.QRect(20,130,33,16))
        self.label_13.setObjectName("label_13")

        self.label_9 = QtGui.QLabel(self.MotorLabels)
        self.label_9.setGeometry(QtCore.QRect(20,100,22,16))
        self.label_9.setObjectName("label_9")

        self.label_5 = QtGui.QLabel(self.MotorLabels)
        self.label_5.setGeometry(QtCore.QRect(20,70,21,16))
        self.label_5.setObjectName("label_5")

        self.label_14 = QtGui.QLabel(self.MotorLabels)
        self.label_14.setGeometry(QtCore.QRect(20,40,33,20))
        self.label_14.setObjectName("label_14")

        self.label_16 = QtGui.QLabel(self.MotorLabels)
        self.label_16.setGeometry(QtCore.QRect(30,10,23,16))
        self.label_16.setObjectName("label_16")

        self.label_8 = QtGui.QLabel(self.MotorLabels)
        self.label_8.setGeometry(QtCore.QRect(10,290,45,16))
        self.label_8.setObjectName("label_8")

        self.label_6 = QtGui.QLabel(self.MotorBox)
        self.label_6.setGeometry(QtCore.QRect(70,70,57,21))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtGui.QLabel(self.MotorBox)
        self.label_7.setGeometry(QtCore.QRect(90,100,33,21))
        self.label_7.setObjectName("label_7")

        self.ScanBox = QtGui.QComboBox(self.MotorBox)
        self.ScanBox.setGeometry(QtCore.QRect(140,70,91,22))
        self.ScanBox.setObjectName("ScanBox")

        self.Counter = QtGui.QSpinBox(self.MotorBox)
        self.Counter.setGeometry(QtCore.QRect(140,100,91,23))
        self.Counter.setMaximum(1000000)
        self.Counter.setMinimum(1)
        self.Counter.setProperty("value",QtCore.QVariant(1))
        self.Counter.setObjectName("Counter")

        self.label_10 = QtGui.QLabel(self.MotorBox)
        self.label_10.setGeometry(QtCore.QRect(110,10,84,20))
        self.label_10.setObjectName("label_10")

        self.Run = QtGui.QPushButton(self.MotorBox)
        self.Run.setGeometry(QtCore.QRect(50,130,231,41))
        self.Run.setObjectName("Run")

        self.Pause = QtGui.QPushButton(self.MotorBox)
        self.Pause.setGeometry(QtCore.QRect(50,190,231,41))
        self.Pause.setObjectName("Pause")

        self.pushButton_2 = QtGui.QPushButton(self.MotorBox)
        self.pushButton_2.setGeometry(QtCore.QRect(30,660,271,51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.ImageFrame = QtGui.QTabWidget(self.XpCentral)
        self.ImageFrame.setGeometry(QtCore.QRect(330,0,941,741))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ImageFrame.sizePolicy().hasHeightForWidth())
        self.ImageFrame.setSizePolicy(sizePolicy)
        self.ImageFrame.setMinimumSize(QtCore.QSize(100,100))
        self.ImageFrame.setSizeIncrement(QtCore.QSize(1,1))
        self.ImageFrame.setBaseSize(QtCore.QSize(1,1))
        self.ImageFrame.setObjectName("ImageFrame")

        self.ElementTab = QtGui.QWidget()
        self.ElementTab.setObjectName("ElementTab")

        self.Message = QtGui.QLabel(self.ElementTab)
        self.Message.setGeometry(QtCore.QRect(420,280,281,111))
        self.Message.setObjectName("Message")

        self.ImageControls = QtGui.QFrame(self.ElementTab)
        self.ImageControls.setGeometry(QtCore.QRect(0,0,171,721))
        self.ImageControls.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ImageControls.setFrameShadow(QtGui.QFrame.Raised)
        self.ImageControls.setObjectName("ImageControls")

        self.ShellText = QtGui.QLineEdit(self.ImageControls)
        self.ShellText.setGeometry(QtCore.QRect(20,150,23,24))
        self.ShellText.setObjectName("ShellText")

        self.label = QtGui.QLabel(self.ImageControls)
        self.label.setGeometry(QtCore.QRect(100,250,62,20))
        self.label.setObjectName("label")

        self.label_2 = QtGui.QLabel(self.ImageControls)
        self.label_2.setGeometry(QtCore.QRect(10,250,59,20))
        self.label_2.setObjectName("label_2")

        self.ElementText = QtGui.QLineEdit(self.ImageControls)
        self.ElementText.setGeometry(QtCore.QRect(20,80,23,24))
        self.ElementText.setObjectName("ElementText")

        self.ElementShell = QtGui.QComboBox(self.ImageControls)
        self.ElementShell.setGeometry(QtCore.QRect(20,150,141,22))
        self.ElementShell.setObjectName("ElementShell")

        self.label_3 = QtGui.QLabel(self.ImageControls)
        self.label_3.setGeometry(QtCore.QRect(50,130,91,20))
        self.label_3.setObjectName("label_3")

        self.label_12 = QtGui.QLabel(self.ImageControls)
        self.label_12.setGeometry(QtCore.QRect(30,60,111,16))
        self.label_12.setObjectName("label_12")

        self.MinValSpin = QtGui.QSpinBox(self.ImageControls)
        self.MinValSpin.setGeometry(QtCore.QRect(10,270,51,23))
        self.MinValSpin.setMaximum(10000)
        self.MinValSpin.setObjectName("MinValSpin")

        self.MaxValSpin = QtGui.QSpinBox(self.ImageControls)
        self.MaxValSpin.setGeometry(QtCore.QRect(100,270,51,23))
        self.MaxValSpin.setMaximum(10000)
        self.MaxValSpin.setProperty("value",QtCore.QVariant(0))
        self.MaxValSpin.setObjectName("MaxValSpin")

        self.label_4 = QtGui.QLabel(self.ImageControls)
        self.label_4.setGeometry(QtCore.QRect(10,310,61,21))
        self.label_4.setObjectName("label_4")

        self.CountMax = QtGui.QSpinBox(self.ImageControls)
        self.CountMax.setGeometry(QtCore.QRect(80,310,71,23))
        self.CountMax.setMaximum(100000)
        self.CountMax.setMinimum(100)
        self.CountMax.setSingleStep(100)
        self.CountMax.setObjectName("CountMax")

        self.SaveImage = QtGui.QPushButton(self.ImageControls)
        self.SaveImage.setGeometry(QtCore.QRect(20,350,131,31))
        self.SaveImage.setObjectName("SaveImage")

        self.pushButton = QtGui.QPushButton(self.ImageControls)
        self.pushButton.setGeometry(QtCore.QRect(20,220,131,26))
        self.pushButton.setObjectName("pushButton")

        self.ElementSelect = QtGui.QComboBox(self.ImageControls)
        self.ElementSelect.setGeometry(QtCore.QRect(20,80,141,22))
        self.ElementSelect.setObjectName("ElementSelect")
        self.ImageFrame.addTab(self.ElementTab,"")

        self.Cartoon = QtGui.QWidget()
        self.Cartoon.setObjectName("Cartoon")
        self.ImageFrame.addTab(self.Cartoon,"")

        self.Video = QtGui.QWidget()
        self.Video.setObjectName("Video")
        self.ImageFrame.addTab(self.Video,"")
        XpMaster.setCentralWidget(self.XpCentral)

        self.retranslateUi(XpMaster)
        self.ImageFrame.setCurrentIndex(0)
        QtCore.QObject.connect(self.ScanBox,QtCore.SIGNAL("activated(int)"),XpMaster.update)
        QtCore.QMetaObject.connectSlotsByName(XpMaster)

    def retranslateUi(self, XpMaster):
        XpMaster.setWindowTitle(QtGui.QApplication.translate("XpMaster", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("XpMaster", "Steps", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("XpMaster", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("XpMaster", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("XpMaster", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("XpMaster", "Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("XpMaster", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("XpMaster", "Scan Type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("XpMaster", "Count", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("XpMaster", "Motor Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.Run.setText(QtGui.QApplication.translate("XpMaster", "Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.Pause.setText(QtGui.QApplication.translate("XpMaster", "Emergancy Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("XpMaster", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.Message.setText(QtGui.QApplication.translate("XpMaster", "       Thank you for Using SpectroMicroscoPy\n"
        "    Please Begin a Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("XpMaster", "Max Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("XpMaster", "Min Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("XpMaster", "Element Shell", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("XpMaster", "Element to Watch", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("XpMaster", "Max Count", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveImage.setText(QtGui.QApplication.translate("XpMaster", "Save Image", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("XpMaster", "Auto Range", None, QtGui.QApplication.UnicodeUTF8))
        self.ImageFrame.setTabText(self.ImageFrame.indexOf(self.ElementTab), QtGui.QApplication.translate("XpMaster", "Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.ImageFrame.setTabText(self.ImageFrame.indexOf(self.Cartoon), QtGui.QApplication.translate("XpMaster", "Cartoon", None, QtGui.QApplication.UnicodeUTF8))
        self.ImageFrame.setTabText(self.ImageFrame.indexOf(self.Video), QtGui.QApplication.translate("XpMaster", "Video", None, QtGui.QApplication.UnicodeUTF8))

