# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GearTester.ui'
#
# Created: Wed Jul 11 17:11:32 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MotorHead(object):
    def setupUi(self, MotorHead):
        MotorHead.setObjectName("MotorHead")
        MotorHead.resize(QtCore.QSize(QtCore.QRect(0,0,680,591).size()).expandedTo(MotorHead.minimumSizeHint()))

        self.Main = QtGui.QWidget(MotorHead)
        self.Main.setObjectName("Main")

        self.go = QtGui.QPushButton(self.Main)
        self.go.setGeometry(QtCore.QRect(650,330,21,21))
        self.go.setObjectName("go")

        self.ClearLog = QtGui.QPushButton(self.Main)
        self.ClearLog.setGeometry(QtCore.QRect(180,480,75,23))
        self.ClearLog.setObjectName("ClearLog")

        self.saveras = QtGui.QPushButton(self.Main)
        self.saveras.setGeometry(QtCore.QRect(570,480,75,23))
        self.saveras.setObjectName("saveras")

        self.label_motors = QtGui.QLabel(self.Main)
        self.label_motors.setGeometry(QtCore.QRect(480,20,181,16))

        font = QtGui.QFont(self.label_motors.font())
        font.setFamily("Verdana")
        self.label_motors.setFont(font)
        self.label_motors.setTextFormat(QtCore.Qt.AutoText)
        self.label_motors.setAlignment(QtCore.Qt.AlignCenter)
        self.label_motors.setObjectName("label_motors")

        self.count = QtGui.QSpinBox(self.Main)
        self.count.setGeometry(QtCore.QRect(600,330,46,23))
        self.count.setObjectName("count")

        self.Positioner = QtGui.QSpinBox(self.Main)
        self.Positioner.setGeometry(QtCore.QRect(460,300,46,23))
        self.Positioner.setObjectName("Positioner")

        self.Mover = QtGui.QPushButton(self.Main)
        self.Mover.setGeometry(QtCore.QRect(610,300,61,23))
        self.Mover.setObjectName("Mover")

        self.ReStart = QtGui.QPushButton(self.Main)
        self.ReStart.setGeometry(QtCore.QRect(100,480,61,23))
        self.ReStart.setObjectName("ReStart")

        self.ChangeFile = QtGui.QPushButton(self.Main)
        self.ChangeFile.setGeometry(QtCore.QRect(480,480,75,23))
        self.ChangeFile.setObjectName("ChangeFile")

        self.MoveBar = QtGui.QSlider(self.Main)
        self.MoveBar.setGeometry(QtCore.QRect(510,300,91,21))
        self.MoveBar.setOrientation(QtCore.Qt.Horizontal)
        self.MoveBar.setObjectName("MoveBar")

        self.plus = QtGui.QPushButton(self.Main)
        self.plus.setGeometry(QtCore.QRect(570,330,21,21))
        self.plus.setObjectName("plus")

        self.dis = QtGui.QDoubleSpinBox(self.Main)
        self.dis.setGeometry(QtCore.QRect(500,330,62,23))
        self.dis.setDecimals(3)
        self.dis.setObjectName("dis")

        self.EStop = QtGui.QPushButton(self.Main)
        self.EStop.setGeometry(QtCore.QRect(10,520,191,41))

        font = QtGui.QFont(self.EStop.font())
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.EStop.setFont(font)
        self.EStop.setObjectName("EStop")

        self.MotorsTree = QtGui.QTreeWidget(self.Main)
        self.MotorsTree.setGeometry(QtCore.QRect(470,40,201,251))
        self.MotorsTree.setObjectName("MotorsTree")

        self.pushButton = QtGui.QPushButton(self.Main)
        self.pushButton.setGeometry(QtCore.QRect(440,40,20,251))
        self.pushButton.setObjectName("pushButton")

        self.Closer = QtGui.QPushButton(self.Main)
        self.Closer.setGeometry(QtCore.QRect(10,480,75,23))
        self.Closer.setObjectName("Closer")

        self.label_responses = QtGui.QLabel(self.Main)
        self.label_responses.setGeometry(QtCore.QRect(10,20,431,16))
        self.label_responses.setAlignment(QtCore.Qt.AlignCenter)
        self.label_responses.setObjectName("label_responses")

        self.Responses = QtGui.QTextEdit(self.Main)
        self.Responses.setGeometry(QtCore.QRect(10,40,431,251))
        self.Responses.setObjectName("Responses")

        self.CommandLine = QtGui.QLineEdit(self.Main)
        self.CommandLine.setGeometry(QtCore.QRect(10,450,561,24))
        self.CommandLine.setObjectName("CommandLine")

        self.minus = QtGui.QPushButton(self.Main)
        self.minus.setGeometry(QtCore.QRect(470,330,21,21))
        self.minus.setObjectName("minus")

        self.widget = QtGui.QWidget(self.Main)
        self.widget.setGeometry(QtCore.QRect(10,300,441,141))
        self.widget.setObjectName("widget")

        self.SpecCMD = QtGui.QPushButton(self.Main)
        self.SpecCMD.setGeometry(QtCore.QRect(570,450,75,26))
        self.SpecCMD.setObjectName("SpecCMD")
        MotorHead.setCentralWidget(self.Main)

        self.Bar = QtGui.QMenuBar(MotorHead)
        self.Bar.setGeometry(QtCore.QRect(0,0,680,28))
        self.Bar.setObjectName("Bar")
        MotorHead.setMenuBar(self.Bar)
        self.label_motors.setBuddy(self.MotorsTree)
        self.label_responses.setBuddy(self.Responses)

        self.retranslateUi(MotorHead)
        QtCore.QObject.connect(self.Positioner,QtCore.SIGNAL("valueChanged(int)"),self.MoveBar.setValue)
        QtCore.QObject.connect(self.MoveBar,QtCore.SIGNAL("valueChanged(int)"),self.Positioner.setValue)
        QtCore.QObject.connect(self.Closer,QtCore.SIGNAL("clicked()"),MotorHead.close)
        QtCore.QObject.connect(self.ClearLog,QtCore.SIGNAL("clicked()"),self.Responses.clear)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.Responses.clear)
        QtCore.QMetaObject.connectSlotsByName(MotorHead)

    def retranslateUi(self, MotorHead):
        MotorHead.setWindowTitle(QtGui.QApplication.translate("MotorHead", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.go.setText(QtGui.QApplication.translate("MotorHead", "go", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearLog.setText(QtGui.QApplication.translate("MotorHead", "Clear Log", None, QtGui.QApplication.UnicodeUTF8))
        self.saveras.setText(QtGui.QApplication.translate("MotorHead", "Save Log As", None, QtGui.QApplication.UnicodeUTF8))
        self.label_motors.setText(QtGui.QApplication.translate("MotorHead", "Motors avalible", None, QtGui.QApplication.UnicodeUTF8))
        self.Mover.setText(QtGui.QApplication.translate("MotorHead", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.ReStart.setText(QtGui.QApplication.translate("MotorHead", "Restart", None, QtGui.QApplication.UnicodeUTF8))
        self.ChangeFile.setText(QtGui.QApplication.translate("MotorHead", "Set Log", None, QtGui.QApplication.UnicodeUTF8))
        self.plus.setText(QtGui.QApplication.translate("MotorHead", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.EStop.setText(QtGui.QApplication.translate("MotorHead", "Emergency STOP", None, QtGui.QApplication.UnicodeUTF8))
        self.MotorsTree.headerItem().setText(0,QtGui.QApplication.translate("MotorHead", "motors", None, QtGui.QApplication.UnicodeUTF8))
        self.MotorsTree.headerItem().setText(1,QtGui.QApplication.translate("MotorHead", "State", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MotorHead", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.Closer.setText(QtGui.QApplication.translate("MotorHead", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label_responses.setText(QtGui.QApplication.translate("MotorHead", "Program Responses", None, QtGui.QApplication.UnicodeUTF8))
        self.minus.setText(QtGui.QApplication.translate("MotorHead", "--", None, QtGui.QApplication.UnicodeUTF8))
        self.SpecCMD.setText(QtGui.QApplication.translate("MotorHead", "Spec CMD", None, QtGui.QApplication.UnicodeUTF8))

