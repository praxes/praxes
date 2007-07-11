# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Xp.ui'
#
# Created: Wed Jul 11 17:11:32 2007
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

        self.Video = QtGui.QGraphicsView(self.main)
        self.Video.setGeometry(QtCore.QRect(170,310,241,191))
        self.Video.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(2)))
        self.Video.setObjectName("Video")

        self.Namer = QtGui.QLineEdit(self.main)
        self.Namer.setGeometry(QtCore.QRect(590,390,23,24))
        self.Namer.setObjectName("Namer")

        self.Zoomer = QtGui.QSlider(self.main)
        self.Zoomer.setGeometry(QtCore.QRect(550,190,91,21))
        self.Zoomer.setOrientation(QtCore.Qt.Horizontal)
        self.Zoomer.setObjectName("Zoomer")

        self.spinBox = QtGui.QSpinBox(self.main)
        self.spinBox.setGeometry(QtCore.QRect(230,510,46,23))
        self.spinBox.setObjectName("spinBox")

        self.label_8 = QtGui.QLabel(self.main)
        self.label_8.setGeometry(QtCore.QRect(180,510,41,17))
        self.label_8.setObjectName("label_8")

        self.MinValeDisplay = QtGui.QLCDNumber(self.main)
        self.MinValeDisplay.setGeometry(QtCore.QRect(560,150,51,16))
        self.MinValeDisplay.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.MinValeDisplay.setObjectName("MinValeDisplay")

        self.MaxVal = QtGui.QSlider(self.main)
        self.MaxVal.setGeometry(QtCore.QRect(640,30,21,111))
        self.MaxVal.setOrientation(QtCore.Qt.Vertical)
        self.MaxVal.setObjectName("MaxVal")

        self.Stepper = QtGui.QDoubleSpinBox(self.main)
        self.Stepper.setGeometry(QtCore.QRect(620,390,62,23))
        self.Stepper.setObjectName("Stepper")

        self.label_9 = QtGui.QLabel(self.main)
        self.label_9.setGeometry(QtCore.QRect(590,370,53,16))
        self.label_9.setObjectName("label_9")

        self.MaxValeDisplay = QtGui.QLCDNumber(self.main)
        self.MaxValeDisplay.setGeometry(QtCore.QRect(630,150,51,16))
        self.MaxValeDisplay.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.MaxValeDisplay.setObjectName("MaxValeDisplay")

        self.lcdNumber = QtGui.QLCDNumber(self.main)
        self.lcdNumber.setGeometry(QtCore.QRect(650,190,41,20))
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.lcdNumber.setObjectName("lcdNumber")

        self.TableMove = QtGui.QPushButton(self.main)
        self.TableMove.setGeometry(QtCore.QRect(590,430,75,26))
        self.TableMove.setObjectName("TableMove")

        self.label_2 = QtGui.QLabel(self.main)
        self.label_2.setGeometry(QtCore.QRect(550,10,59,20))
        self.label_2.setObjectName("label_2")

        self.MinVal = QtGui.QSlider(self.main)
        self.MinVal.setGeometry(QtCore.QRect(570,30,21,111))
        self.MinVal.setOrientation(QtCore.Qt.Vertical)
        self.MinVal.setObjectName("MinVal")

        self.label = QtGui.QLabel(self.main)
        self.label.setGeometry(QtCore.QRect(620,10,62,20))
        self.label.setObjectName("label")

        self.label_3 = QtGui.QLabel(self.main)
        self.label_3.setGeometry(QtCore.QRect(560,170,41,16))
        self.label_3.setObjectName("label_3")

        self.VidZoom = QtGui.QSlider(self.main)
        self.VidZoom.setGeometry(QtCore.QRect(280,510,111,16))
        self.VidZoom.setOrientation(QtCore.Qt.Horizontal)
        self.VidZoom.setObjectName("VidZoom")

        self.SaveImage = QtGui.QPushButton(self.main)
        self.SaveImage.setGeometry(QtCore.QRect(590,320,75,23))
        self.SaveImage.setObjectName("SaveImage")

        self.Element = QtGui.QComboBox(self.main)
        self.Element.setGeometry(QtCore.QRect(0,50,131,22))
        self.Element.setObjectName("Element")

        self.label_4 = QtGui.QLabel(self.main)
        self.label_4.setGeometry(QtCore.QRect(10,20,121,20))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtGui.QLabel(self.main)
        self.label_5.setGeometry(QtCore.QRect(430,310,16,16))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtGui.QLabel(self.main)
        self.label_6.setGeometry(QtCore.QRect(490,310,16,16))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtGui.QLabel(self.main)
        self.label_7.setGeometry(QtCore.QRect(550,310,16,16))
        self.label_7.setObjectName("label_7")

        self.PictureTube = QtGui.QGraphicsView(self.main)
        self.PictureTube.setGeometry(QtCore.QRect(140,10,391,261))
        self.PictureTube.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(2)))
        self.PictureTube.setObjectName("PictureTube")

        self.Xslide = QtGui.QSlider(self.main)
        self.Xslide.setGeometry(QtCore.QRect(430,330,25,161))
        self.Xslide.setSingleStep(1)
        self.Xslide.setOrientation(QtCore.Qt.Vertical)
        self.Xslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Xslide.setTickInterval(10)
        self.Xslide.setObjectName("Xslide")

        self.Yslide = QtGui.QSlider(self.main)
        self.Yslide.setGeometry(QtCore.QRect(490,330,25,161))
        self.Yslide.setOrientation(QtCore.Qt.Vertical)
        self.Yslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Yslide.setTickInterval(10)
        self.Yslide.setObjectName("Yslide")

        self.Zslide = QtGui.QSlider(self.main)
        self.Zslide.setGeometry(QtCore.QRect(550,330,25,161))
        self.Zslide.setOrientation(QtCore.Qt.Vertical)
        self.Zslide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Zslide.setTickInterval(10)
        self.Zslide.setObjectName("Zslide")

        self.SpinY = QtGui.QDoubleSpinBox(self.main)
        self.SpinY.setGeometry(QtCore.QRect(480,500,62,23))
        self.SpinY.setSingleStep(0.01)
        self.SpinY.setObjectName("SpinY")

        self.SpinZ = QtGui.QDoubleSpinBox(self.main)
        self.SpinZ.setGeometry(QtCore.QRect(540,500,62,23))
        self.SpinZ.setSingleStep(0.01)
        self.SpinZ.setObjectName("SpinZ")

        self.SpinX = QtGui.QDoubleSpinBox(self.main)
        self.SpinX.setGeometry(QtCore.QRect(420,500,62,23))
        self.SpinX.setSingleStep(0.01)
        self.SpinX.setObjectName("SpinX")
        XPrun.setCentralWidget(self.main)
        self.label_2.setBuddy(self.MinVal)
        self.label.setBuddy(self.MaxVal)
        self.label_3.setBuddy(self.Zoomer)
        self.label_4.setBuddy(self.Element)

        self.retranslateUi(XPrun)
        QtCore.QMetaObject.connectSlotsByName(XPrun)

    def retranslateUi(self, XPrun):
        XPrun.setWindowTitle(QtGui.QApplication.translate("XPrun", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("XPrun", "Step Size", None, QtGui.QApplication.UnicodeUTF8))
        self.TableMove.setText(QtGui.QApplication.translate("XPrun", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("XPrun", "Min Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("XPrun", "Max Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("XPrun", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveImage.setText(QtGui.QApplication.translate("XPrun", "Save Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("XPrun", "Element Selection ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("XPrun", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("XPrun", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("XPrun", "Z", None, QtGui.QApplication.UnicodeUTF8))

