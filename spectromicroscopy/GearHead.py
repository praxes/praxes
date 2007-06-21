# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jeff/workspace/spectromicroscopy/spectromicroscopy//GearHead.ui'
#
# Created: Thu Jun 21 16:56:41 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MotorHead(object):
    def setupUi(self, MotorHead):
        MotorHead.setObjectName("MotorHead")
        MotorHead.resize(QtCore.QSize(QtCore.QRect(0,0,730,683).size()).expandedTo(MotorHead.minimumSizeHint()))
        MotorHead.setWindowIcon(QtGui.QIcon("Cornell seal.jpg"))

        self.centralwidget = QtGui.QWidget(MotorHead)
        self.centralwidget.setObjectName("centralwidget")

        self.Tabby = QtGui.QTabWidget(self.centralwidget)
        self.Tabby.setGeometry(QtCore.QRect(0,0,731,661))
        self.Tabby.setAutoFillBackground(True)
        self.Tabby.setObjectName("Tabby")

        self.MotorTab = QtGui.QWidget()
        self.MotorTab.setObjectName("MotorTab")

        self.label_responses = QtGui.QLabel(self.MotorTab)
        self.label_responses.setGeometry(QtCore.QRect(20,40,431,16))
        self.label_responses.setAlignment(QtCore.Qt.AlignCenter)
        self.label_responses.setObjectName("label_responses")

        self.CommandLine = QtGui.QLineEdit(self.MotorTab)
        self.CommandLine.setGeometry(QtCore.QRect(20,440,631,20))
        self.CommandLine.setObjectName("CommandLine")

        self.pushButton = QtGui.QPushButton(self.MotorTab)
        self.pushButton.setGeometry(QtCore.QRect(20,480,75,23))
        self.pushButton.setObjectName("pushButton")

        self.label_motors = QtGui.QLabel(self.MotorTab)
        self.label_motors.setGeometry(QtCore.QRect(490,40,181,16))

        font = QtGui.QFont(self.label_motors.font())
        font.setFamily("Verdana")
        self.label_motors.setFont(font)
        self.label_motors.setTextFormat(QtCore.Qt.AutoText)
        self.label_motors.setAlignment(QtCore.Qt.AlignCenter)
        self.label_motors.setObjectName("label_motors")

        self.saveras = QtGui.QPushButton(self.MotorTab)
        self.saveras.setGeometry(QtCore.QRect(580,480,75,23))
        self.saveras.setObjectName("saveras")

        self.saver = QtGui.QPushButton(self.MotorTab)
        self.saver.setGeometry(QtCore.QRect(490,480,75,23))
        self.saver.setObjectName("saver")

        self.ChangeFile = QtGui.QPushButton(self.MotorTab)
        self.ChangeFile.setGeometry(QtCore.QRect(400,480,75,23))
        self.ChangeFile.setObjectName("ChangeFile")

        self.ReStart = QtGui.QPushButton(self.MotorTab)
        self.ReStart.setGeometry(QtCore.QRect(110,480,61,23))
        self.ReStart.setObjectName("ReStart")

        self.ClearLog = QtGui.QPushButton(self.MotorTab)
        self.ClearLog.setGeometry(QtCore.QRect(190,480,75,23))
        self.ClearLog.setObjectName("ClearLog")

        self.Mover = QtGui.QPushButton(self.MotorTab)
        self.Mover.setGeometry(QtCore.QRect(620,320,61,23))
        self.Mover.setObjectName("Mover")

        self.Responses = QtGui.QTextEdit(self.MotorTab)
        self.Responses.setGeometry(QtCore.QRect(20,60,431,251))
        self.Responses.setObjectName("Responses")

        self.EStop = QtGui.QPushButton(self.MotorTab)
        self.EStop.setGeometry(QtCore.QRect(20,520,191,41))

        font = QtGui.QFont(self.EStop.font())
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.EStop.setFont(font)
        self.EStop.setObjectName("EStop")

        self.MoveBar = QtGui.QSlider(self.MotorTab)
        self.MoveBar.setGeometry(QtCore.QRect(520,320,91,21))
        self.MoveBar.setOrientation(QtCore.Qt.Horizontal)
        self.MoveBar.setObjectName("MoveBar")

        self.Positioner = QtGui.QSpinBox(self.MotorTab)
        self.Positioner.setGeometry(QtCore.QRect(470,320,46,23))
        self.Positioner.setObjectName("Positioner")

        self.MotorsTree = QtGui.QTreeWidget(self.MotorTab)
        self.MotorsTree.setGeometry(QtCore.QRect(480,60,201,251))
        self.MotorsTree.setObjectName("MotorsTree")
        self.Tabby.addTab(self.MotorTab,"")

        self.Graphing = QtGui.QWidget()
        self.Graphing.setObjectName("Graphing")

        self.label = QtGui.QLabel(self.Graphing)
        self.label.setGeometry(QtCore.QRect(650,10,62,20))
        self.label.setObjectName("label")

        self.MaxVal = QtGui.QSlider(self.Graphing)
        self.MaxVal.setGeometry(QtCore.QRect(670,30,21,111))
        self.MaxVal.setOrientation(QtCore.Qt.Vertical)
        self.MaxVal.setObjectName("MaxVal")

        self.label_2 = QtGui.QLabel(self.Graphing)
        self.label_2.setGeometry(QtCore.QRect(580,10,59,20))
        self.label_2.setObjectName("label_2")

        self.MinVal = QtGui.QSlider(self.Graphing)
        self.MinVal.setGeometry(QtCore.QRect(610,30,21,111))
        self.MinVal.setOrientation(QtCore.Qt.Vertical)
        self.MinVal.setObjectName("MinVal")

        self.frame = QtGui.QFrame(self.Graphing)
        self.frame.setWindowModality(QtCore.Qt.NonModal)
        self.frame.setGeometry(QtCore.QRect(180,10,391,261))
        self.frame.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(2)))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setLineWidth(8)
        self.frame.setObjectName("frame")

        self.PictureTube = QtGui.QGraphicsView(self.frame)
        self.PictureTube.setGeometry(QtCore.QRect(0,0,391,261))
        self.PictureTube.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(2)))
        self.PictureTube.setObjectName("PictureTube")

        self.label_3 = QtGui.QLabel(self.Graphing)
        self.label_3.setGeometry(QtCore.QRect(580,170,41,16))
        self.label_3.setObjectName("label_3")

        self.SaveImage = QtGui.QPushButton(self.Graphing)
        self.SaveImage.setGeometry(QtCore.QRect(590,250,75,23))
        self.SaveImage.setObjectName("SaveImage")

        self.label_8 = QtGui.QLabel(self.Graphing)
        self.label_8.setGeometry(QtCore.QRect(190,500,41,17))
        self.label_8.setObjectName("label_8")

        self.Element = QtGui.QComboBox(self.Graphing)
        self.Element.setGeometry(QtCore.QRect(20,40,131,22))
        self.Element.setObjectName("Element")

        self.lcdNumber = QtGui.QLCDNumber(self.Graphing)
        self.lcdNumber.setGeometry(QtCore.QRect(680,190,41,20))
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.lcdNumber.setObjectName("lcdNumber")

        self.MaxValeDisplay = QtGui.QLCDNumber(self.Graphing)
        self.MaxValeDisplay.setGeometry(QtCore.QRect(660,150,51,16))
        self.MaxValeDisplay.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.MaxValeDisplay.setObjectName("MaxValeDisplay")

        self.MinValeDisplay = QtGui.QLCDNumber(self.Graphing)
        self.MinValeDisplay.setGeometry(QtCore.QRect(590,150,51,16))
        self.MinValeDisplay.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.MinValeDisplay.setObjectName("MinValeDisplay")

        self.label_4 = QtGui.QLabel(self.Graphing)
        self.label_4.setGeometry(QtCore.QRect(20,20,121,20))
        self.label_4.setObjectName("label_4")

        self.label_6 = QtGui.QLabel(self.Graphing)
        self.label_6.setGeometry(QtCore.QRect(500,300,16,17))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtGui.QLabel(self.Graphing)
        self.label_7.setGeometry(QtCore.QRect(560,300,16,17))
        self.label_7.setObjectName("label_7")

        self.label_9 = QtGui.QLabel(self.Graphing)
        self.label_9.setGeometry(QtCore.QRect(600,310,53,16))
        self.label_9.setObjectName("label_9")

        self.Namer = QtGui.QLineEdit(self.Graphing)
        self.Namer.setGeometry(QtCore.QRect(600,330,23,24))
        self.Namer.setObjectName("Namer")

        self.label_5 = QtGui.QLabel(self.Graphing)
        self.label_5.setGeometry(QtCore.QRect(440,300,16,17))
        self.label_5.setObjectName("label_5")

        self.TableMove = QtGui.QPushButton(self.Graphing)
        self.TableMove.setGeometry(QtCore.QRect(600,370,75,26))
        self.TableMove.setObjectName("TableMove")

        self.Zoomer = QtGui.QSlider(self.Graphing)
        self.Zoomer.setGeometry(QtCore.QRect(580,190,91,21))
        self.Zoomer.setOrientation(QtCore.Qt.Horizontal)
        self.Zoomer.setObjectName("Zoomer")

        self.spinBox = QtGui.QSpinBox(self.Graphing)
        self.spinBox.setGeometry(QtCore.QRect(240,500,46,23))
        self.spinBox.setObjectName("spinBox")

        self.VidZoom = QtGui.QSlider(self.Graphing)
        self.VidZoom.setGeometry(QtCore.QRect(290,500,111,16))
        self.VidZoom.setOrientation(QtCore.Qt.Horizontal)
        self.VidZoom.setObjectName("VidZoom")

        self.Video = QtGui.QGraphicsView(self.Graphing)
        self.Video.setGeometry(QtCore.QRect(180,300,241,191))
        self.Video.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(2)))
        self.Video.setObjectName("Video")

        self.Stepper = QtGui.QDoubleSpinBox(self.Graphing)
        self.Stepper.setGeometry(QtCore.QRect(630,330,62,23))
        self.Stepper.setObjectName("Stepper")

        self.SpinX = QtGui.QDoubleSpinBox(self.Graphing)
        self.SpinX.setGeometry(QtCore.QRect(430,490,62,23))
        self.SpinX.setSingleStep(0.01)
        self.SpinX.setObjectName("SpinX")

        self.SpinY = QtGui.QDoubleSpinBox(self.Graphing)
        self.SpinY.setGeometry(QtCore.QRect(490,490,62,23))
        self.SpinY.setSingleStep(0.01)
        self.SpinY.setObjectName("SpinY")

        self.SpinZ = QtGui.QDoubleSpinBox(self.Graphing)
        self.SpinZ.setGeometry(QtCore.QRect(550,490,62,23))
        self.SpinZ.setSingleStep(0.01)
        self.SpinZ.setObjectName("SpinZ")

        self.X = QtGui.QSlider(self.Graphing)
        self.X.setGeometry(QtCore.QRect(440,320,25,161))
        self.X.setSingleStep(1)
        self.X.setOrientation(QtCore.Qt.Vertical)
        self.X.setTickPosition(QtGui.QSlider.TicksBelow)
        self.X.setTickInterval(10)
        self.X.setObjectName("X")

        self.Y = QtGui.QSlider(self.Graphing)
        self.Y.setGeometry(QtCore.QRect(500,320,25,161))
        self.Y.setOrientation(QtCore.Qt.Vertical)
        self.Y.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Y.setTickInterval(10)
        self.Y.setObjectName("Y")

        self.Z = QtGui.QSlider(self.Graphing)
        self.Z.setGeometry(QtCore.QRect(560,320,25,161))
        self.Z.setOrientation(QtCore.Qt.Vertical)
        self.Z.setTickPosition(QtGui.QSlider.TicksBelow)
        self.Z.setTickInterval(10)
        self.Z.setObjectName("Z")
        self.Tabby.addTab(self.Graphing,"")

        self.Konsole = QtGui.QWidget()
        self.Konsole.setObjectName("Konsole")

        self.Runner = QtGui.QPushButton(self.Konsole)
        self.Runner.setGeometry(QtCore.QRect(20,400,75,23))
        self.Runner.setObjectName("Runner")

        self.pushButton_3 = QtGui.QPushButton(self.Konsole)
        self.pushButton_3.setGeometry(QtCore.QRect(680,20,21,181))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(13)))
        self.pushButton_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")

        self.MacroSave = QtGui.QPushButton(self.Konsole)
        self.MacroSave.setGeometry(QtCore.QRect(200,400,101,23))
        self.MacroSave.setObjectName("MacroSave")

        self.changer = QtGui.QPushButton(self.Konsole)
        self.changer.setGeometry(QtCore.QRect(310,400,75,23))
        self.changer.setObjectName("changer")

        self.pushButton_4 = QtGui.QPushButton(self.Konsole)
        self.pushButton_4.setGeometry(QtCore.QRect(600,400,75,23))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtGui.QPushButton(self.Konsole)
        self.pushButton_5.setGeometry(QtCore.QRect(680,220,16,171))
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_2 = QtGui.QPushButton(self.Konsole)
        self.pushButton_2.setGeometry(QtCore.QRect(110,400,75,23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.KonsoleEm = QtGui.QTextEdit(self.Konsole)
        self.KonsoleEm.setGeometry(QtCore.QRect(20,220,651,171))
        self.KonsoleEm.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(4)))
        self.KonsoleEm.setObjectName("KonsoleEm")

        self.Display = QtGui.QTextBrowser(self.Konsole)
        self.Display.setGeometry(QtCore.QRect(20,10,651,192))
        self.Display.setObjectName("Display")
        self.Tabby.addTab(self.Konsole,"")
        MotorHead.setCentralWidget(self.centralwidget)

        self.Bar = QtGui.QMenuBar(MotorHead)
        self.Bar.setGeometry(QtCore.QRect(0,0,730,28))
        self.Bar.setObjectName("Bar")
        MotorHead.setMenuBar(self.Bar)
        self.label_responses.setBuddy(self.Responses)
        self.label_motors.setBuddy(self.MotorsTree)
        self.label.setBuddy(self.MaxVal)
        self.label_2.setBuddy(self.MinVal)
        self.label_3.setBuddy(self.Zoomer)
        self.label_4.setBuddy(self.Element)

        self.retranslateUi(MotorHead)
        self.Tabby.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),MotorHead.close)
        QtCore.QObject.connect(self.MaxVal,QtCore.SIGNAL("sliderMoved(int)"),self.MaxValeDisplay.display)
        QtCore.QObject.connect(self.MinVal,QtCore.SIGNAL("sliderMoved(int)"),self.MinValeDisplay.display)
        QtCore.QObject.connect(self.Zoomer,QtCore.SIGNAL("valueChanged(int)"),self.lcdNumber.display)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),self.KonsoleEm.clear)
        QtCore.QObject.connect(self.pushButton_4,QtCore.SIGNAL("clicked()"),MotorHead.close)
        QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL("clicked()"),self.Display.clear)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),self.Display.clear)
        QtCore.QObject.connect(self.pushButton_5,QtCore.SIGNAL("clicked()"),self.KonsoleEm.clear)
        QtCore.QObject.connect(self.Positioner,QtCore.SIGNAL("valueChanged(int)"),self.MoveBar.setValue)
        QtCore.QObject.connect(self.MoveBar,QtCore.SIGNAL("valueChanged(int)"),self.Positioner.setValue)
        QtCore.QObject.connect(self.spinBox,QtCore.SIGNAL("valueChanged(int)"),self.VidZoom.setValue)
        QtCore.QObject.connect(self.VidZoom,QtCore.SIGNAL("valueChanged(int)"),self.spinBox.setValue)
        QtCore.QMetaObject.connectSlotsByName(MotorHead)
        MotorHead.setTabOrder(self.saveras,self.ChangeFile)
        MotorHead.setTabOrder(self.ChangeFile,self.CommandLine)
        MotorHead.setTabOrder(self.CommandLine,self.saver)
        MotorHead.setTabOrder(self.saver,self.MotorsTree)
        MotorHead.setTabOrder(self.MotorsTree,self.Tabby)
        MotorHead.setTabOrder(self.Tabby,self.pushButton)
        MotorHead.setTabOrder(self.pushButton,self.ClearLog)
        MotorHead.setTabOrder(self.ClearLog,self.MaxVal)
        MotorHead.setTabOrder(self.MaxVal,self.Responses)
        MotorHead.setTabOrder(self.Responses,self.SaveImage)
        MotorHead.setTabOrder(self.SaveImage,self.MinVal)
        MotorHead.setTabOrder(self.MinVal,self.Zoomer)
        MotorHead.setTabOrder(self.Zoomer,self.Element)
        MotorHead.setTabOrder(self.Element,self.EStop)
        MotorHead.setTabOrder(self.EStop,self.KonsoleEm)
        MotorHead.setTabOrder(self.KonsoleEm,self.Runner)

    def retranslateUi(self, MotorHead):
        MotorHead.setWindowTitle(QtGui.QApplication.translate("MotorHead", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_responses.setText(QtGui.QApplication.translate("MotorHead", "Program Responses", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MotorHead", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label_motors.setText(QtGui.QApplication.translate("MotorHead", "Motors avalible", None, QtGui.QApplication.UnicodeUTF8))
        self.saveras.setText(QtGui.QApplication.translate("MotorHead", "Save Log As", None, QtGui.QApplication.UnicodeUTF8))
        self.saver.setText(QtGui.QApplication.translate("MotorHead", "Save Log", None, QtGui.QApplication.UnicodeUTF8))
        self.ChangeFile.setText(QtGui.QApplication.translate("MotorHead", "Change Log", None, QtGui.QApplication.UnicodeUTF8))
        self.ReStart.setText(QtGui.QApplication.translate("MotorHead", "Restart", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearLog.setText(QtGui.QApplication.translate("MotorHead", "Clear Log", None, QtGui.QApplication.UnicodeUTF8))
        self.Mover.setText(QtGui.QApplication.translate("MotorHead", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.EStop.setText(QtGui.QApplication.translate("MotorHead", "Emergency STOP", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabby.setTabText(self.Tabby.indexOf(self.MotorTab), QtGui.QApplication.translate("MotorHead", "Motor Testing", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MotorHead", "Max Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MotorHead", "Min Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MotorHead", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveImage.setText(QtGui.QApplication.translate("MotorHead", "Save Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MotorHead", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MotorHead", "Element Selection ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MotorHead", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MotorHead", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MotorHead", "Step Size", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MotorHead", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.TableMove.setText(QtGui.QApplication.translate("MotorHead", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabby.setTabText(self.Tabby.indexOf(self.Graphing), QtGui.QApplication.translate("MotorHead", "Graphing", None, QtGui.QApplication.UnicodeUTF8))
        self.Runner.setText(QtGui.QApplication.translate("MotorHead", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MotorHead", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.MacroSave.setText(QtGui.QApplication.translate("MotorHead", "Save As Macro", None, QtGui.QApplication.UnicodeUTF8))
        self.changer.setText(QtGui.QApplication.translate("MotorHead", "Change Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MotorHead", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MotorHead", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MotorHead", "Clear All", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabby.setTabText(self.Tabby.indexOf(self.Konsole), QtGui.QApplication.translate("MotorHead", "Konsole", None, QtGui.QApplication.UnicodeUTF8))

