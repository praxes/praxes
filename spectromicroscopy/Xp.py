# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Xp.ui'
#
# Created: Thu Jul 19 16:14:24 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_XPrun(object):
    def setupUi(self, XPrun):
        XPrun.setObjectName("XPrun")
        XPrun.resize(QtCore.QSize(QtCore.QRect(0,0,699,540).size()).expandedTo(XPrun.minimumSizeHint()))

        self.main = QtGui.QWidget(XPrun)
        self.main.setObjectName("main")

        self.Zoomer = QtGui.QSlider(self.main)
        self.Zoomer.setGeometry(QtCore.QRect(10,210,91,21))
        self.Zoomer.setOrientation(QtCore.Qt.Horizontal)
        self.Zoomer.setObjectName("Zoomer")

        self.label_2 = QtGui.QLabel(self.main)
        self.label_2.setGeometry(QtCore.QRect(10,20,59,20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtGui.QLabel(self.main)
        self.label_3.setGeometry(QtCore.QRect(20,190,41,16))
        self.label_3.setObjectName("label_3")

        self.spinBox_3 = QtGui.QSpinBox(self.main)
        self.spinBox_3.setGeometry(QtCore.QRect(20,160,46,23))
        self.spinBox_3.setObjectName("spinBox_3")

        self.MinVal = QtGui.QSlider(self.main)
        self.MinVal.setGeometry(QtCore.QRect(30,40,21,111))
        self.MinVal.setOrientation(QtCore.Qt.Vertical)
        self.MinVal.setObjectName("MinVal")

        self.label = QtGui.QLabel(self.main)
        self.label.setGeometry(QtCore.QRect(80,20,62,20))
        self.label.setObjectName("label")

        self.MaxVal = QtGui.QSlider(self.main)
        self.MaxVal.setGeometry(QtCore.QRect(100,40,21,111))
        self.MaxVal.setOrientation(QtCore.Qt.Vertical)
        self.MaxVal.setObjectName("MaxVal")

        self.spinBox_4 = QtGui.QSpinBox(self.main)
        self.spinBox_4.setGeometry(QtCore.QRect(100,160,46,23))
        self.spinBox_4.setObjectName("spinBox_4")

        self.spinBox_2 = QtGui.QSpinBox(self.main)
        self.spinBox_2.setGeometry(QtCore.QRect(110,210,46,23))
        self.spinBox_2.setObjectName("spinBox_2")

        self.label_13 = QtGui.QLabel(self.main)
        self.label_13.setGeometry(QtCore.QRect(460,270,33,16))
        self.label_13.setObjectName("label_13")

        self.label_4 = QtGui.QLabel(self.main)
        self.label_4.setGeometry(QtCore.QRect(460,210,21,16))
        self.label_4.setObjectName("label_4")

        self.label_14 = QtGui.QLabel(self.main)
        self.label_14.setGeometry(QtCore.QRect(460,190,33,16))
        self.label_14.setObjectName("label_14")

        self.label_9 = QtGui.QLabel(self.main)
        self.label_9.setGeometry(QtCore.QRect(460,230,22,16))
        self.label_9.setObjectName("label_9")

        self.label_10 = QtGui.QLabel(self.main)
        self.label_10.setGeometry(QtCore.QRect(520,160,16,16))
        self.label_10.setObjectName("label_10")

        self.Ymax = QtGui.QDoubleSpinBox(self.main)
        self.Ymax.setGeometry(QtCore.QRect(560,240,62,23))
        self.Ymax.setObjectName("Ymax")

        self.Ystep = QtGui.QSpinBox(self.main)
        self.Ystep.setGeometry(QtCore.QRect(570,270,51,23))
        self.Ystep.setObjectName("Ystep")

        self.label_11 = QtGui.QLabel(self.main)
        self.label_11.setGeometry(QtCore.QRect(590,160,16,16))
        self.label_11.setObjectName("label_11")

        self.Zmax = QtGui.QDoubleSpinBox(self.main)
        self.Zmax.setGeometry(QtCore.QRect(630,240,62,23))
        self.Zmax.setObjectName("Zmax")

        self.Zmin = QtGui.QDoubleSpinBox(self.main)
        self.Zmin.setGeometry(QtCore.QRect(630,210,62,23))
        self.Zmin.setObjectName("Zmin")

        self.spinBox_8 = QtGui.QSpinBox(self.main)
        self.spinBox_8.setGeometry(QtCore.QRect(640,270,51,23))
        self.spinBox_8.setObjectName("spinBox_8")

        self.label_15 = QtGui.QLabel(self.main)
        self.label_15.setGeometry(QtCore.QRect(650,160,16,16))
        self.label_15.setObjectName("label_15")

        self.Xname = QtGui.QLineEdit(self.main)
        self.Xname.setGeometry(QtCore.QRect(500,180,51,24))
        self.Xname.setObjectName("Xname")

        self.Yname = QtGui.QLineEdit(self.main)
        self.Yname.setGeometry(QtCore.QRect(570,180,51,24))
        self.Yname.setObjectName("Yname")

        self.Zname = QtGui.QLineEdit(self.main)
        self.Zname.setGeometry(QtCore.QRect(640,180,51,24))
        self.Zname.setObjectName("Zname")

        self.Ymin = QtGui.QDoubleSpinBox(self.main)
        self.Ymin.setGeometry(QtCore.QRect(560,210,62,23))
        self.Ymin.setObjectName("Ymin")

        self.tabWidget = QtGui.QTabWidget(self.main)
        self.tabWidget.setGeometry(QtCore.QRect(160,10,291,281))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2,"")

        self.label_6 = QtGui.QLabel(self.main)
        self.label_6.setGeometry(QtCore.QRect(440,440,52,16))
        self.label_6.setObjectName("label_6")

        self.label_16 = QtGui.QLabel(self.main)
        self.label_16.setGeometry(QtCore.QRect(10,500,41,17))
        self.label_16.setObjectName("label_16")

        self.spinBox_7 = QtGui.QSpinBox(self.main)
        self.spinBox_7.setGeometry(QtCore.QRect(50,500,46,23))
        self.spinBox_7.setObjectName("spinBox_7")

        self.label_17 = QtGui.QLabel(self.main)
        self.label_17.setGeometry(QtCore.QRect(210,500,41,17))
        self.label_17.setObjectName("label_17")

        self.spinBox_6 = QtGui.QSpinBox(self.main)
        self.spinBox_6.setGeometry(QtCore.QRect(250,500,46,23))
        self.spinBox_6.setObjectName("spinBox_6")

        self.Xmin = QtGui.QDoubleSpinBox(self.main)
        self.Xmin.setGeometry(QtCore.QRect(490,210,62,23))
        self.Xmin.setObjectName("Xmin")

        self.Xmax = QtGui.QDoubleSpinBox(self.main)
        self.Xmax.setGeometry(QtCore.QRect(490,240,62,23))
        self.Xmax.setObjectName("Xmax")

        self.Xstep = QtGui.QSpinBox(self.main)
        self.Xstep.setGeometry(QtCore.QRect(500,270,51,23))
        self.Xstep.setObjectName("Xstep")

        self.SpinZ = QtGui.QDoubleSpinBox(self.main)
        self.SpinZ.setGeometry(QtCore.QRect(630,440,62,23))
        self.SpinZ.setSingleStep(0.01)
        self.SpinZ.setObjectName("SpinZ")

        self.frame_5 = QtGui.QFrame(self.main)
        self.frame_5.setGeometry(QtCore.QRect(210,310,181,181))
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")

        self.frame_4 = QtGui.QFrame(self.main)
        self.frame_4.setGeometry(QtCore.QRect(10,310,181,181))
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.VidZoom_4 = QtGui.QSlider(self.main)
        self.VidZoom_4.setGeometry(QtCore.QRect(100,500,91,16))
        self.VidZoom_4.setOrientation(QtCore.Qt.Horizontal)
        self.VidZoom_4.setObjectName("VidZoom_4")

        self.VidZoom_3 = QtGui.QSlider(self.main)
        self.VidZoom_3.setGeometry(QtCore.QRect(300,500,91,16))
        self.VidZoom_3.setOrientation(QtCore.Qt.Horizontal)
        self.VidZoom_3.setObjectName("VidZoom_3")

        self.Xslide = QtGui.QSlider(self.main)
        self.Xslide.setGeometry(QtCore.QRect(510,310,25,121))
        self.Xslide.setSingleStep(1)
        self.Xslide.setOrientation(QtCore.Qt.Vertical)
        self.Xslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Xslide.setTickInterval(10)
        self.Xslide.setObjectName("Xslide")

        self.Yslide = QtGui.QSlider(self.main)
        self.Yslide.setGeometry(QtCore.QRect(580,310,25,121))
        self.Yslide.setOrientation(QtCore.Qt.Vertical)
        self.Yslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Yslide.setTickInterval(10)
        self.Yslide.setObjectName("Yslide")

        self.Zslide = QtGui.QSlider(self.main)
        self.Zslide.setGeometry(QtCore.QRect(650,310,25,121))
        self.Zslide.setOrientation(QtCore.Qt.Vertical)
        self.Zslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Zslide.setTickInterval(10)
        self.Zslide.setObjectName("Zslide")

        self.SpinY = QtGui.QDoubleSpinBox(self.main)
        self.SpinY.setGeometry(QtCore.QRect(560,440,62,23))
        self.SpinY.setSingleStep(0.01)
        self.SpinY.setObjectName("SpinY")

        self.SpinX = QtGui.QDoubleSpinBox(self.main)
        self.SpinX.setGeometry(QtCore.QRect(490,440,62,23))
        self.SpinX.setSingleStep(0.01)
        self.SpinX.setObjectName("SpinX")

        self.Mv = QtGui.QPushButton(self.main)
        self.Mv.setGeometry(QtCore.QRect(490,470,91,31))
        self.Mv.setObjectName("Mv")

        self.Run = QtGui.QPushButton(self.main)
        self.Run.setGeometry(QtCore.QRect(600,470,91,31))
        self.Run.setObjectName("Run")
        XPrun.setCentralWidget(self.main)
        self.label_2.setBuddy(self.MinVal)
        self.label_3.setBuddy(self.Zoomer)
        self.label.setBuddy(self.MaxVal)

        self.retranslateUi(XPrun)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.MinVal,QtCore.SIGNAL("valueChanged(int)"),self.spinBox_3.setValue)
        QtCore.QObject.connect(self.MaxVal,QtCore.SIGNAL("valueChanged(int)"),self.spinBox_4.setValue)
        QtCore.QObject.connect(self.Zoomer,QtCore.SIGNAL("valueChanged(int)"),self.spinBox_2.setValue)
        QtCore.QMetaObject.connectSlotsByName(XPrun)

    def retranslateUi(self, XPrun):
        XPrun.setWindowTitle(QtGui.QApplication.translate("XPrun", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("XPrun", "Min Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("XPrun", "Max Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("XPrun", "Steps", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("XPrun", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("XPrun", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("XPrun", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("XPrun", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("XPrun", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBox_8.setToolTip(QtGui.QApplication.translate("XPrun", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Zstep</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("XPrun", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.Xname.setText(QtGui.QApplication.translate("XPrun", "samx", None, QtGui.QApplication.UnicodeUTF8))
        self.Yname.setText(QtGui.QApplication.translate("XPrun", "samy", None, QtGui.QApplication.UnicodeUTF8))
        self.Zname.setText(QtGui.QApplication.translate("XPrun", "samz", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("XPrun", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("XPrun", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("XPrun", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.Mv.setText(QtGui.QApplication.translate("XPrun", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.Run.setText(QtGui.QApplication.translate("XPrun", "Run", None, QtGui.QApplication.UnicodeUTF8))

