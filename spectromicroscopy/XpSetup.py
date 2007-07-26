# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XpSetup.ui'
#
# Created: Thu Jul 26 17:41:05 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_XpSetter(object):
    def setupUi(self, XpSetter):
        XpSetter.setObjectName("XpSetter")
        XpSetter.resize(QtCore.QSize(QtCore.QRect(0,0,735,666).size()).expandedTo(XpSetter.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(XpSetter)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(460,10,271,651))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.Ymin = QtGui.QDoubleSpinBox(self.frame)
        self.Ymin.setGeometry(QtCore.QRect(130,190,62,23))
        self.Ymin.setObjectName("Ymin")

        self.Xslide = QtGui.QSlider(self.frame)
        self.Xslide.setGeometry(QtCore.QRect(80,290,25,121))
        self.Xslide.setSingleStep(1)
        self.Xslide.setOrientation(QtCore.Qt.Vertical)
        self.Xslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Xslide.setTickInterval(10)
        self.Xslide.setObjectName("Xslide")

        self.Zstep = QtGui.QSpinBox(self.frame)
        self.Zstep.setGeometry(QtCore.QRect(210,250,51,23))
        self.Zstep.setObjectName("Zstep")

        self.Run = QtGui.QPushButton(self.frame)
        self.Run.setGeometry(QtCore.QRect(170,450,91,31))
        self.Run.setObjectName("Run")

        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(160,140,16,16))
        self.label_11.setObjectName("label_11")

        self.ScanBox = QtGui.QComboBox(self.frame)
        self.ScanBox.setGeometry(QtCore.QRect(140,10,91,22))
        self.ScanBox.setObjectName("ScanBox")

        self.Zmax = QtGui.QDoubleSpinBox(self.frame)
        self.Zmax.setGeometry(QtCore.QRect(200,220,62,23))
        self.Zmax.setObjectName("Zmax")

        self.SpinY = QtGui.QDoubleSpinBox(self.frame)
        self.SpinY.setGeometry(QtCore.QRect(130,420,62,23))
        self.SpinY.setDecimals(4)
        self.SpinY.setSingleStep(0.01)
        self.SpinY.setObjectName("SpinY")

        self.Counter = QtGui.QSpinBox(self.frame)
        self.Counter.setGeometry(QtCore.QRect(140,40,91,23))
        self.Counter.setMaximum(1000000)
        self.Counter.setMinimum(1)
        self.Counter.setProperty("value",QtCore.QVariant(1))
        self.Counter.setObjectName("Counter")

        self.Zname = QtGui.QLineEdit(self.frame)
        self.Zname.setGeometry(QtCore.QRect(210,160,51,24))
        self.Zname.setObjectName("Zname")

        self.Ystep = QtGui.QSpinBox(self.frame)
        self.Ystep.setGeometry(QtCore.QRect(140,250,51,23))
        self.Ystep.setObjectName("Ystep")

        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(30,190,21,16))
        self.label_4.setObjectName("label_4")

        self.Mv = QtGui.QPushButton(self.frame)
        self.Mv.setGeometry(QtCore.QRect(60,450,91,31))
        self.Mv.setObjectName("Mv")

        self.label_7 = QtGui.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(90,40,33,21))
        self.label_7.setObjectName("label_7")

        self.label_15 = QtGui.QLabel(self.frame)
        self.label_15.setGeometry(QtCore.QRect(220,140,16,16))
        self.label_15.setObjectName("label_15")

        self.Xmax = QtGui.QDoubleSpinBox(self.frame)
        self.Xmax.setGeometry(QtCore.QRect(60,220,62,23))
        self.Xmax.setObjectName("Xmax")

        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(70,10,57,21))
        self.label_5.setObjectName("label_5")

        self.Xname = QtGui.QLineEdit(self.frame)
        self.Xname.setGeometry(QtCore.QRect(70,160,51,24))
        self.Xname.setObjectName("Xname")

        self.label_14 = QtGui.QLabel(self.frame)
        self.label_14.setGeometry(QtCore.QRect(30,170,33,16))
        self.label_14.setObjectName("label_14")

        self.SpinZ = QtGui.QDoubleSpinBox(self.frame)
        self.SpinZ.setGeometry(QtCore.QRect(200,420,62,23))
        self.SpinZ.setDecimals(4)
        self.SpinZ.setSingleStep(0.01)
        self.SpinZ.setObjectName("SpinZ")

        self.SpinX = QtGui.QDoubleSpinBox(self.frame)
        self.SpinX.setGeometry(QtCore.QRect(60,420,62,23))
        self.SpinX.setDecimals(4)
        self.SpinX.setSingleStep(0.01)
        self.SpinX.setObjectName("SpinX")

        self.Zmin = QtGui.QDoubleSpinBox(self.frame)
        self.Zmin.setGeometry(QtCore.QRect(200,190,62,23))
        self.Zmin.setObjectName("Zmin")

        self.label_10 = QtGui.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(90,140,16,16))
        self.label_10.setObjectName("label_10")

        self.label_13 = QtGui.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(30,250,33,16))
        self.label_13.setObjectName("label_13")

        self.Xstep = QtGui.QSpinBox(self.frame)
        self.Xstep.setGeometry(QtCore.QRect(70,250,51,23))
        self.Xstep.setObjectName("Xstep")

        self.Yslide = QtGui.QSlider(self.frame)
        self.Yslide.setGeometry(QtCore.QRect(150,290,25,121))
        self.Yslide.setOrientation(QtCore.Qt.Vertical)
        self.Yslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Yslide.setTickInterval(10)
        self.Yslide.setObjectName("Yslide")

        self.Xmin = QtGui.QDoubleSpinBox(self.frame)
        self.Xmin.setGeometry(QtCore.QRect(60,190,62,23))
        self.Xmin.setObjectName("Xmin")

        self.Zslide = QtGui.QSlider(self.frame)
        self.Zslide.setGeometry(QtCore.QRect(220,290,25,121))
        self.Zslide.setOrientation(QtCore.Qt.Vertical)
        self.Zslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Zslide.setTickInterval(10)
        self.Zslide.setObjectName("Zslide")

        self.Ymax = QtGui.QDoubleSpinBox(self.frame)
        self.Ymax.setGeometry(QtCore.QRect(130,220,62,23))
        self.Ymax.setObjectName("Ymax")

        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(30,210,22,16))
        self.label_9.setObjectName("label_9")

        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10,420,45,16))
        self.label_6.setObjectName("label_6")

        self.Yname = QtGui.QLineEdit(self.frame)
        self.Yname.setGeometry(QtCore.QRect(140,160,51,24))
        self.Yname.setObjectName("Yname")

        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10,20,151,16))
        self.label_3.setObjectName("label_3")

        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10,40,441,211))
        self.listWidget.setObjectName("listWidget")
        XpSetter.setCentralWidget(self.centralwidget)

        self.retranslateUi(XpSetter)
        QtCore.QMetaObject.connectSlotsByName(XpSetter)

    def retranslateUi(self, XpSetter):
        XpSetter.setWindowTitle(QtGui.QApplication.translate("XpSetter", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.Zstep.setToolTip(QtGui.QApplication.translate("XpSetter", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Zstep</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Run.setText(QtGui.QApplication.translate("XpSetter", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("XpSetter", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.Zname.setText(QtGui.QApplication.translate("XpSetter", "samz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("XpSetter", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.Mv.setText(QtGui.QApplication.translate("XpSetter", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("XpSetter", "Count", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("XpSetter", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("XpSetter", "Scan Type", None, QtGui.QApplication.UnicodeUTF8))
        self.Xname.setText(QtGui.QApplication.translate("XpSetter", "samx", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("XpSetter", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("XpSetter", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("XpSetter", "Steps", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("XpSetter", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("XpSetter", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.Yname.setText(QtGui.QApplication.translate("XpSetter", "samy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("XpSetter", "Elements", None, QtGui.QApplication.UnicodeUTF8))

