# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SpecSetter.ui'
#
# Created: Thu Jul 05 20:10:01 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SpecSetter(object):
    def setupUi(self, SpecSetter):
        SpecSetter.setObjectName("SpecSetter")
        SpecSetter.resize(QtCore.QSize(QtCore.QRect(0,0,426,135).size()).expandedTo(SpecSetter.minimumSizeHint()))

        self.label_2 = QtGui.QLabel(SpecSetter)
        self.label_2.setGeometry(QtCore.QRect(90,40,65,16))
        self.label_2.setObjectName("label_2")

        self.Speed = QtGui.QLabel(SpecSetter)
        self.Speed.setGeometry(QtCore.QRect(370,40,54,16))
        self.Speed.setObjectName("Speed")

        self.pushButton = QtGui.QPushButton(SpecSetter)
        self.pushButton.setGeometry(QtCore.QRect(340,110,80,23))
        self.pushButton.setObjectName("pushButton")

        self.lineEdit_2 = QtGui.QLineEdit(SpecSetter)
        self.lineEdit_2.setGeometry(QtCore.QRect(120,10,156,23))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.Changer = QtGui.QPushButton(SpecSetter)
        self.Changer.setGeometry(QtCore.QRect(290,10,133,23))
        self.Changer.setObjectName("Changer")

        self.label = QtGui.QLabel(SpecSetter)
        self.label.setGeometry(QtCore.QRect(0,40,85,16))
        self.label.setObjectName("label")

        self.label_3 = QtGui.QLabel(SpecSetter)
        self.label_3.setGeometry(QtCore.QRect(90,90,65,20))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtGui.QLabel(SpecSetter)
        self.label_4.setGeometry(QtCore.QRect(160,90,68,20))
        self.label_4.setObjectName("label_4")

        self.Setter = QtGui.QPushButton(SpecSetter)
        self.Setter.setGeometry(QtCore.QRect(240,110,100,23))
        self.Setter.setObjectName("Setter")

        self.label_9 = QtGui.QLabel(SpecSetter)
        self.label_9.setGeometry(QtCore.QRect(0,10,121,16))
        self.label_9.setObjectName("label_9")

        self.LL = QtGui.QDoubleSpinBox(SpecSetter)
        self.LL.setGeometry(QtCore.QRect(90,110,65,23))
        self.LL.setMaximum(360.0)
        self.LL.setMinimum(-360.0)
        self.LL.setObjectName("LL")

        self.UL = QtGui.QDoubleSpinBox(SpecSetter)
        self.UL.setGeometry(QtCore.QRect(160,110,68,23))
        self.UL.setMaximum(360.0)
        self.UL.setMinimum(-360.0)
        self.UL.setObjectName("UL")

        self.Blash = QtGui.QDoubleSpinBox(SpecSetter)
        self.Blash.setGeometry(QtCore.QRect(0,110,85,23))
        self.Blash.setDecimals(0)
        self.Blash.setMaximum(1000000.0)
        self.Blash.setMinimum(-1000000.0)
        self.Blash.setObjectName("Blash")

        self.Name = QtGui.QLineEdit(SpecSetter)
        self.Name.setGeometry(QtCore.QRect(0,60,61,24))
        self.Name.setMaxLength(2)
        self.Name.setObjectName("Name")

        self.StepSize = QtGui.QDoubleSpinBox(SpecSetter)
        self.StepSize.setGeometry(QtCore.QRect(70,60,71,23))
        self.StepSize.setObjectName("StepSize")

        self.label_5 = QtGui.QLabel(SpecSetter)
        self.label_5.setGeometry(QtCore.QRect(0,90,85,20))
        self.label_5.setObjectName("label_5")

        self.Sign = QtGui.QSpinBox(SpecSetter)
        self.Sign.setGeometry(QtCore.QRect(150,60,46,23))
        self.Sign.setMaximum(1)
        self.Sign.setMinimum(-1)
        self.Sign.setSingleStep(2)
        self.Sign.setProperty("value",QtCore.QVariant(1))
        self.Sign.setObjectName("Sign")

        self.label_6 = QtGui.QLabel(SpecSetter)
        self.label_6.setGeometry(QtCore.QRect(160,40,46,16))
        self.label_6.setObjectName("label_6")

        self.Accel = QtGui.QDoubleSpinBox(SpecSetter)
        self.Accel.setGeometry(QtCore.QRect(200,60,69,23))
        self.Accel.setObjectName("Accel")

        self.label_7 = QtGui.QLabel(SpecSetter)
        self.label_7.setGeometry(QtCore.QRect(200,40,69,16))
        self.label_7.setObjectName("label_7")

        self.BR = QtGui.QDoubleSpinBox(SpecSetter)
        self.BR.setGeometry(QtCore.QRect(280,60,61,23))
        self.BR.setDecimals(0)
        self.BR.setMaximum(1000000.0)
        self.BR.setObjectName("BR")

        self.label_8 = QtGui.QLabel(SpecSetter)
        self.label_8.setGeometry(QtCore.QRect(280,40,73,16))
        self.label_8.setObjectName("label_8")

        self.Speed1 = QtGui.QDoubleSpinBox(SpecSetter)
        self.Speed1.setGeometry(QtCore.QRect(353,60,71,23))
        self.Speed1.setDecimals(0)
        self.Speed1.setMaximum(1000000.0)
        self.Speed1.setObjectName("Speed1")
        self.label_2.setBuddy(self.StepSize)
        self.Speed.setBuddy(self.Speed)
        self.label.setBuddy(self.Name)
        self.label_3.setBuddy(self.LL)
        self.label_4.setBuddy(self.UL)
        self.label_9.setBuddy(self.lineEdit_2)
        self.label_5.setBuddy(self.Blash)
        self.label_6.setBuddy(self.Sign)
        self.label_7.setBuddy(self.Accel)
        self.label_8.setBuddy(self.BR)

        self.retranslateUi(SpecSetter)
        QtCore.QMetaObject.connectSlotsByName(SpecSetter)
        SpecSetter.setTabOrder(self.lineEdit_2,self.Changer)
        SpecSetter.setTabOrder(self.Changer,self.Name)
        SpecSetter.setTabOrder(self.Name,self.StepSize)
        SpecSetter.setTabOrder(self.StepSize,self.Sign)
        SpecSetter.setTabOrder(self.Sign,self.Accel)
        SpecSetter.setTabOrder(self.Accel,self.BR)
        SpecSetter.setTabOrder(self.BR,self.Speed)
        SpecSetter.setTabOrder(self.Speed,self.Blash)
        SpecSetter.setTabOrder(self.Blash,self.LL)
        SpecSetter.setTabOrder(self.LL,self.UL)
        SpecSetter.setTabOrder(self.UL,self.Setter)
        SpecSetter.setTabOrder(self.Setter,self.pushButton)

    def retranslateUi(self, SpecSetter):
        SpecSetter.setWindowTitle(QtGui.QApplication.translate("SpecSetter", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SpecSetter", "Stepsize", None, QtGui.QApplication.UnicodeUTF8))
        self.Speed.setText(QtGui.QApplication.translate("SpecSetter", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("SpecSetter", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.Changer.setText(QtGui.QApplication.translate("SpecSetter", "Change File", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SpecSetter", "MotorName", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SpecSetter", "Lower Limit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SpecSetter", "Upper Limit", None, QtGui.QApplication.UnicodeUTF8))
        self.Setter.setText(QtGui.QApplication.translate("SpecSetter", "Set Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("SpecSetter", "Config File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("SpecSetter", "Backlash", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("SpecSetter", "Sign", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("SpecSetter", "Acceleration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("SpecSetter", "Base Rate", None, QtGui.QApplication.UnicodeUTF8))

