# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Xp.ui'
#
# Created: Fri Jul 13 17:01:45 2007
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

        self.spinBox = QtGui.QSpinBox(self.main)
        self.spinBox.setGeometry(QtCore.QRect(60,500,46,23))
        self.spinBox.setObjectName("spinBox")

        self.label_8 = QtGui.QLabel(self.main)
        self.label_8.setGeometry(QtCore.QRect(10,500,41,17))
        self.label_8.setObjectName("label_8")

        self.label_2 = QtGui.QLabel(self.main)
        self.label_2.setGeometry(QtCore.QRect(10,20,59,20))
        self.label_2.setObjectName("label_2")

        self.label = QtGui.QLabel(self.main)
        self.label.setGeometry(QtCore.QRect(80,20,62,20))
        self.label.setObjectName("label")

        self.label_7 = QtGui.QLabel(self.main)
        self.label_7.setGeometry(QtCore.QRect(340,310,16,16))
        self.label_7.setObjectName("label_7")

        self.Zslide = QtGui.QSlider(self.main)
        self.Zslide.setGeometry(QtCore.QRect(340,330,25,161))
        self.Zslide.setOrientation(QtCore.Qt.Vertical)
        self.Zslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Zslide.setTickInterval(10)
        self.Zslide.setObjectName("Zslide")

        self.SpinZ = QtGui.QDoubleSpinBox(self.main)
        self.SpinZ.setGeometry(QtCore.QRect(330,500,62,23))
        self.SpinZ.setSingleStep(0.01)
        self.SpinZ.setObjectName("SpinZ")

        self.SpinX = QtGui.QDoubleSpinBox(self.main)
        self.SpinX.setGeometry(QtCore.QRect(210,500,62,23))
        self.SpinX.setSingleStep(0.01)
        self.SpinX.setObjectName("SpinX")

        self.label_5 = QtGui.QLabel(self.main)
        self.label_5.setGeometry(QtCore.QRect(220,310,16,16))
        self.label_5.setObjectName("label_5")

        self.VidZoom = QtGui.QSlider(self.main)
        self.VidZoom.setGeometry(QtCore.QRect(110,500,91,16))
        self.VidZoom.setOrientation(QtCore.Qt.Horizontal)
        self.VidZoom.setObjectName("VidZoom")

        self.SpinY = QtGui.QDoubleSpinBox(self.main)
        self.SpinY.setGeometry(QtCore.QRect(270,500,62,23))
        self.SpinY.setSingleStep(0.01)
        self.SpinY.setObjectName("SpinY")

        self.Yslide = QtGui.QSlider(self.main)
        self.Yslide.setGeometry(QtCore.QRect(280,330,25,161))
        self.Yslide.setOrientation(QtCore.Qt.Vertical)
        self.Yslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Yslide.setTickInterval(10)
        self.Yslide.setObjectName("Yslide")

        self.label_6 = QtGui.QLabel(self.main)
        self.label_6.setGeometry(QtCore.QRect(280,310,16,16))
        self.label_6.setObjectName("label_6")

        self.MaxVal = QtGui.QSlider(self.main)
        self.MaxVal.setGeometry(QtCore.QRect(100,40,21,111))
        self.MaxVal.setOrientation(QtCore.Qt.Vertical)
        self.MaxVal.setObjectName("MaxVal")

        self.tabWidget = QtGui.QTabWidget(self.main)
        self.tabWidget.setGeometry(QtCore.QRect(160,10,291,281))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2,"")

        self.Ymin = QtGui.QDoubleSpinBox(self.main)
        self.Ymin.setGeometry(QtCore.QRect(480,100,62,23))
        self.Ymin.setObjectName("Ymin")

        self.Xmin = QtGui.QDoubleSpinBox(self.main)
        self.Xmin.setGeometry(QtCore.QRect(480,60,62,23))
        self.Xmin.setObjectName("Xmin")

        self.label_10 = QtGui.QLabel(self.main)
        self.label_10.setGeometry(QtCore.QRect(460,60,20,20))
        self.label_10.setObjectName("label_10")

        self.label_11 = QtGui.QLabel(self.main)
        self.label_11.setGeometry(QtCore.QRect(460,100,16,16))
        self.label_11.setObjectName("label_11")

        self.label_4 = QtGui.QLabel(self.main)
        self.label_4.setGeometry(QtCore.QRect(480,40,52,16))
        self.label_4.setObjectName("label_4")

        self.Xmax = QtGui.QDoubleSpinBox(self.main)
        self.Xmax.setGeometry(QtCore.QRect(550,60,62,23))
        self.Xmax.setObjectName("Xmax")

        self.label_9 = QtGui.QLabel(self.main)
        self.label_9.setGeometry(QtCore.QRect(550,40,52,16))
        self.label_9.setObjectName("label_9")

        self.frame_2 = QtGui.QFrame(self.main)
        self.frame_2.setGeometry(QtCore.QRect(10,310,181,181))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.MinVal = QtGui.QSlider(self.main)
        self.MinVal.setGeometry(QtCore.QRect(30,40,21,111))
        self.MinVal.setOrientation(QtCore.Qt.Vertical)
        self.MinVal.setObjectName("MinVal")

        self.spinBox_3 = QtGui.QSpinBox(self.main)
        self.spinBox_3.setGeometry(QtCore.QRect(20,160,46,23))
        self.spinBox_3.setObjectName("spinBox_3")

        self.spinBox_4 = QtGui.QSpinBox(self.main)
        self.spinBox_4.setGeometry(QtCore.QRect(100,160,46,23))
        self.spinBox_4.setObjectName("spinBox_4")

        self.label_3 = QtGui.QLabel(self.main)
        self.label_3.setGeometry(QtCore.QRect(20,190,41,16))
        self.label_3.setObjectName("label_3")

        self.spinBox_2 = QtGui.QSpinBox(self.main)
        self.spinBox_2.setGeometry(QtCore.QRect(110,210,46,23))
        self.spinBox_2.setObjectName("spinBox_2")

        self.Xslide = QtGui.QSlider(self.main)
        self.Xslide.setGeometry(QtCore.QRect(220,330,25,161))
        self.Xslide.setSingleStep(1)
        self.Xslide.setOrientation(QtCore.Qt.Vertical)
        self.Xslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Xslide.setTickInterval(10)
        self.Xslide.setObjectName("Xslide")

        self.label_12 = QtGui.QLabel(self.main)
        self.label_12.setGeometry(QtCore.QRect(410,500,41,17))
        self.label_12.setObjectName("label_12")

        self.VidZoom_2 = QtGui.QSlider(self.main)
        self.VidZoom_2.setGeometry(QtCore.QRect(510,500,91,16))
        self.VidZoom_2.setOrientation(QtCore.Qt.Horizontal)
        self.VidZoom_2.setObjectName("VidZoom_2")

        self.spinBox_5 = QtGui.QSpinBox(self.main)
        self.spinBox_5.setGeometry(QtCore.QRect(460,500,46,23))
        self.spinBox_5.setObjectName("spinBox_5")

        self.Zoomer = QtGui.QSlider(self.main)
        self.Zoomer.setGeometry(QtCore.QRect(10,210,91,21))
        self.Zoomer.setOrientation(QtCore.Qt.Horizontal)
        self.Zoomer.setObjectName("Zoomer")

        self.Ymax = QtGui.QDoubleSpinBox(self.main)
        self.Ymax.setGeometry(QtCore.QRect(550,100,62,23))
        self.Ymax.setObjectName("Ymax")

        self.Stepper = QtGui.QDoubleSpinBox(self.main)
        self.Stepper.setGeometry(QtCore.QRect(620,310,62,23))
        self.Stepper.setObjectName("Stepper")

        self.Mv = QtGui.QPushButton(self.main)
        self.Mv.setGeometry(QtCore.QRect(590,340,91,26))
        self.Mv.setObjectName("Mv")

        self.Namer = QtGui.QLineEdit(self.main)
        self.Namer.setGeometry(QtCore.QRect(590,310,23,24))
        self.Namer.setMaxLength(1)
        self.Namer.setObjectName("Namer")

        self.frame = QtGui.QFrame(self.main)
        self.frame.setGeometry(QtCore.QRect(400,310,181,181))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        XPrun.setCentralWidget(self.main)
        self.label_2.setBuddy(self.MinVal)
        self.label.setBuddy(self.MaxVal)
        self.label_3.setBuddy(self.Zoomer)

        self.retranslateUi(XPrun)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.MinVal,QtCore.SIGNAL("valueChanged(int)"),self.spinBox_3.setValue)
        QtCore.QObject.connect(self.MaxVal,QtCore.SIGNAL("valueChanged(int)"),self.spinBox_4.setValue)
        QtCore.QObject.connect(self.spinBox,QtCore.SIGNAL("valueChanged(int)"),self.VidZoom.setValue)
        QtCore.QObject.connect(self.VidZoom,QtCore.SIGNAL("valueChanged(int)"),self.spinBox.setValue)
        QtCore.QObject.connect(self.VidZoom_2,QtCore.SIGNAL("valueChanged(int)"),self.spinBox_5.setValue)
        QtCore.QObject.connect(self.spinBox_5,QtCore.SIGNAL("valueChanged(int)"),self.VidZoom_2.setValue)
        QtCore.QObject.connect(self.Zoomer,QtCore.SIGNAL("valueChanged(int)"),self.spinBox_2.setValue)
        QtCore.QMetaObject.connectSlotsByName(XPrun)

    def retranslateUi(self, XPrun):
        XPrun.setWindowTitle(QtGui.QApplication.translate("XPrun", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("XPrun", "Min Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("XPrun", "Max Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("XPrun", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("XPrun", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("XPrun", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("XPrun", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("XPrun", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("XPrun", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("XPrun", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("XPrun", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("XPrun", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.Mv.setText(QtGui.QApplication.translate("XPrun", "Move", None, QtGui.QApplication.UnicodeUTF8))

