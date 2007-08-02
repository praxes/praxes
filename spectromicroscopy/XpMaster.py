# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XpMaster.ui'
#
# Created: Thu Aug  2 18:01:35 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_XpMaster(object):
    def setupUi(self, XpMaster):
        XpMaster.setObjectName("XpMaster")
        XpMaster.resize(QtCore.QSize(QtCore.QRect(0,0,1272,903).size()).expandedTo(XpMaster.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(XpMaster.sizePolicy().hasHeightForWidth())
        XpMaster.setSizePolicy(sizePolicy)
        XpMaster.setSizeIncrement(QtCore.QSize(1,1))

        self.XpCentral = QtGui.QWidget(XpMaster)
        self.XpCentral.setObjectName("XpCentral")

        self.ImageFrame = QtGui.QTabWidget(self.XpCentral)
        self.ImageFrame.setGeometry(QtCore.QRect(330,0,941,871))

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
        self.ImageControls.setGeometry(QtCore.QRect(0,0,171,851))
        self.ImageControls.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ImageControls.setFrameShadow(QtGui.QFrame.Raised)
        self.ImageControls.setObjectName("ImageControls")

        self.ElementText = QtGui.QLineEdit(self.ImageControls)
        self.ElementText.setGeometry(QtCore.QRect(20,80,23,24))
        self.ElementText.setObjectName("ElementText")

        self.ElementSelect = QtGui.QComboBox(self.ImageControls)
        self.ElementSelect.setGeometry(QtCore.QRect(20,80,131,21))
        self.ElementSelect.setObjectName("ElementSelect")

        self.Element_Label = QtGui.QLabel(self.ImageControls)
        self.Element_Label.setGeometry(QtCore.QRect(10,60,155,16))
        self.Element_Label.setObjectName("Element_Label")

        self.AutoRanger = QtGui.QPushButton(self.ImageControls)
        self.AutoRanger.setGeometry(QtCore.QRect(20,330,131,26))
        self.AutoRanger.setObjectName("AutoRanger")

        self.Min_Label = QtGui.QLabel(self.ImageControls)
        self.Min_Label.setGeometry(QtCore.QRect(10,380,59,20))
        self.Min_Label.setObjectName("Min_Label")

        self.MaxValSpin = QtGui.QSpinBox(self.ImageControls)
        self.MaxValSpin.setGeometry(QtCore.QRect(100,400,51,23))
        self.MaxValSpin.setMaximum(100000)
        self.MaxValSpin.setProperty("value",QtCore.QVariant(0))
        self.MaxValSpin.setObjectName("MaxValSpin")

        self.Max_label = QtGui.QLabel(self.ImageControls)
        self.Max_label.setGeometry(QtCore.QRect(100,380,62,20))
        self.Max_label.setObjectName("Max_label")

        self.CountMin = QtGui.QSpinBox(self.ImageControls)
        self.CountMin.setGeometry(QtCore.QRect(80,440,71,23))
        self.CountMin.setMaximum(100000)
        self.CountMin.setMinimum(0)
        self.CountMin.setSingleStep(100)
        self.CountMin.setProperty("value",QtCore.QVariant(0))
        self.CountMin.setObjectName("CountMin")

        self.Count_Label = QtGui.QLabel(self.ImageControls)
        self.Count_Label.setGeometry(QtCore.QRect(10,440,61,21))
        self.Count_Label.setObjectName("Count_Label")

        self.SaveImage = QtGui.QPushButton(self.ImageControls)
        self.SaveImage.setGeometry(QtCore.QRect(20,480,131,31))
        self.SaveImage.setObjectName("SaveImage")

        self.MinValSpin = QtGui.QSpinBox(self.ImageControls)
        self.MinValSpin.setGeometry(QtCore.QRect(10,400,51,23))
        self.MinValSpin.setMaximum(100000)
        self.MinValSpin.setObjectName("MinValSpin")

        self.label = QtGui.QLabel(self.ImageControls)
        self.label.setGeometry(QtCore.QRect(60,140,52,16))
        self.label.setObjectName("label")

        self.ScaleBox = QtGui.QComboBox(self.ImageControls)
        self.ScaleBox.setGeometry(QtCore.QRect(21,160,131,22))
        self.ScaleBox.setObjectName("ScaleBox")
        self.ImageFrame.addTab(self.ElementTab,"")

        self.Cartoon = QtGui.QWidget()
        self.Cartoon.setObjectName("Cartoon")
        self.ImageFrame.addTab(self.Cartoon,"")

        self.Video = QtGui.QWidget()
        self.Video.setObjectName("Video")
        self.ImageFrame.addTab(self.Video,"")

        self.MotorBox = QtGui.QFrame(self.XpCentral)
        self.MotorBox.setGeometry(QtCore.QRect(0,0,331,871))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MotorBox.sizePolicy().hasHeightForWidth())
        self.MotorBox.setSizePolicy(sizePolicy)
        self.MotorBox.setFrameShape(QtGui.QFrame.StyledPanel)
        self.MotorBox.setFrameShadow(QtGui.QFrame.Raised)
        self.MotorBox.setObjectName("MotorBox")

        self.Counter = QtGui.QSpinBox(self.MotorBox)
        self.Counter.setGeometry(QtCore.QRect(140,100,91,23))
        self.Counter.setMaximum(1000000)
        self.Counter.setMinimum(1)
        self.Counter.setProperty("value",QtCore.QVariant(1))
        self.Counter.setObjectName("Counter")

        self.Contol_Label = QtGui.QLabel(self.MotorBox)
        self.Contol_Label.setGeometry(QtCore.QRect(110,10,84,20))
        self.Contol_Label.setObjectName("Contol_Label")

        self.Estop = QtGui.QPushButton(self.MotorBox)
        self.Estop.setGeometry(QtCore.QRect(50,190,231,41))
        self.Estop.setObjectName("Estop")

        self.Run = QtGui.QPushButton(self.MotorBox)
        self.Run.setGeometry(QtCore.QRect(50,130,231,41))
        self.Run.setObjectName("Run")

        self.Scan_label = QtGui.QLabel(self.MotorBox)
        self.Scan_label.setGeometry(QtCore.QRect(70,70,57,21))
        self.Scan_label.setObjectName("Scan_label")

        self.Count_label = QtGui.QLabel(self.MotorBox)
        self.Count_label.setGeometry(QtCore.QRect(90,100,33,21))
        self.Count_label.setObjectName("Count_label")

        self.Mover = QtGui.QPushButton(self.MotorBox)
        self.Mover.setGeometry(QtCore.QRect(30,660,271,51))
        self.Mover.setObjectName("Mover")

        self.MotorLabels = QtGui.QFrame(self.MotorBox)
        self.MotorLabels.setGeometry(QtCore.QRect(0,310,61,321))
        self.MotorLabels.setFrameShape(QtGui.QFrame.StyledPanel)
        self.MotorLabels.setFrameShadow(QtGui.QFrame.Raised)
        self.MotorLabels.setObjectName("MotorLabels")

        self.Axis_label = QtGui.QLabel(self.MotorLabels)
        self.Axis_label.setGeometry(QtCore.QRect(30,10,23,16))
        self.Axis_label.setObjectName("Axis_label")

        self.Name_label = QtGui.QLabel(self.MotorLabels)
        self.Name_label.setGeometry(QtCore.QRect(20,40,33,20))
        self.Name_label.setObjectName("Name_label")

        self.Min_label = QtGui.QLabel(self.MotorLabels)
        self.Min_label.setGeometry(QtCore.QRect(20,70,21,16))
        self.Min_label.setObjectName("Min_label")

        self.Max_label1 = QtGui.QLabel(self.MotorLabels)
        self.Max_label1.setGeometry(QtCore.QRect(20,100,22,16))
        self.Max_label1.setObjectName("Max_label1")

        self.Steps_label = QtGui.QLabel(self.MotorLabels)
        self.Steps_label.setGeometry(QtCore.QRect(20,130,33,16))
        self.Steps_label.setObjectName("Steps_label")

        self.Position_label = QtGui.QLabel(self.MotorLabels)
        self.Position_label.setGeometry(QtCore.QRect(10,290,45,16))
        self.Position_label.setObjectName("Position_label")

        self.ScanBox = QtGui.QComboBox(self.MotorBox)
        self.ScanBox.setGeometry(QtCore.QRect(140,70,91,22))
        self.ScanBox.setObjectName("ScanBox")
        XpMaster.setCentralWidget(self.XpCentral)

        self.Bar = QtGui.QMenuBar(XpMaster)
        self.Bar.setGeometry(QtCore.QRect(0,0,1272,28))
        self.Bar.setObjectName("Bar")
        XpMaster.setMenuBar(self.Bar)

        self.retranslateUi(XpMaster)
        self.ImageFrame.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(XpMaster)

    def retranslateUi(self, XpMaster):
        XpMaster.setWindowTitle(QtGui.QApplication.translate("XpMaster", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.Message.setText(QtGui.QApplication.translate("XpMaster", "       Thank you for Using SpectroMicroscoPy\n"
        "    Please Begin a Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.Element_Label.setText(QtGui.QApplication.translate("XpMaster", "Element and Band to Watch", None, QtGui.QApplication.UnicodeUTF8))
        self.AutoRanger.setText(QtGui.QApplication.translate("XpMaster", "Auto Range", None, QtGui.QApplication.UnicodeUTF8))
        self.Min_Label.setText(QtGui.QApplication.translate("XpMaster", "Min Value", None, QtGui.QApplication.UnicodeUTF8))
        self.Max_label.setText(QtGui.QApplication.translate("XpMaster", "Max Value", None, QtGui.QApplication.UnicodeUTF8))
        self.Count_Label.setText(QtGui.QApplication.translate("XpMaster", "Min Count", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveImage.setText(QtGui.QApplication.translate("XpMaster", "Save Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("XpMaster", "Scale", None, QtGui.QApplication.UnicodeUTF8))
        self.ScaleBox.addItem(QtGui.QApplication.translate("XpMaster", "linear", None, QtGui.QApplication.UnicodeUTF8))
        self.ScaleBox.addItem(QtGui.QApplication.translate("XpMaster", "log", None, QtGui.QApplication.UnicodeUTF8))
        self.ImageFrame.setTabText(self.ImageFrame.indexOf(self.ElementTab), QtGui.QApplication.translate("XpMaster", "Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.ImageFrame.setTabText(self.ImageFrame.indexOf(self.Cartoon), QtGui.QApplication.translate("XpMaster", "Cartoon", None, QtGui.QApplication.UnicodeUTF8))
        self.ImageFrame.setTabText(self.ImageFrame.indexOf(self.Video), QtGui.QApplication.translate("XpMaster", "Video", None, QtGui.QApplication.UnicodeUTF8))
        self.Contol_Label.setText(QtGui.QApplication.translate("XpMaster", "Motor Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.Estop.setText(QtGui.QApplication.translate("XpMaster", "Emergancy Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.Run.setText(QtGui.QApplication.translate("XpMaster", "Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.Scan_label.setText(QtGui.QApplication.translate("XpMaster", "Scan Type", None, QtGui.QApplication.UnicodeUTF8))
        self.Count_label.setText(QtGui.QApplication.translate("XpMaster", "Count", None, QtGui.QApplication.UnicodeUTF8))
        self.Mover.setText(QtGui.QApplication.translate("XpMaster", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.Axis_label.setText(QtGui.QApplication.translate("XpMaster", "Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.Name_label.setText(QtGui.QApplication.translate("XpMaster", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.Min_label.setText(QtGui.QApplication.translate("XpMaster", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.Max_label1.setText(QtGui.QApplication.translate("XpMaster", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.Steps_label.setText(QtGui.QApplication.translate("XpMaster", "Steps", None, QtGui.QApplication.UnicodeUTF8))
        self.Position_label.setText(QtGui.QApplication.translate("XpMaster", "Position", None, QtGui.QApplication.UnicodeUTF8))

