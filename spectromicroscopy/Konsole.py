# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Konsole.ui'
#
# Created: Tue Jul  3 14:15:29 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_Kontrol(object):
    def setupUi(self, Kontrol):
        Kontrol.setObjectName("Kontrol")
        Kontrol.resize(QtCore.QSize(QtCore.QRect(0,0,712,452).size()).expandedTo(Kontrol.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(Kontrol)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(110,400,75,23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.changer = QtGui.QPushButton(self.centralwidget)
        self.changer.setGeometry(QtCore.QRect(310,400,75,23))
        self.changer.setObjectName("changer")

        self.MacroSave = QtGui.QPushButton(self.centralwidget)
        self.MacroSave.setGeometry(QtCore.QRect(200,400,101,23))
        self.MacroSave.setObjectName("MacroSave")

        self.Runner = QtGui.QPushButton(self.centralwidget)
        self.Runner.setGeometry(QtCore.QRect(20,400,75,23))
        self.Runner.setObjectName("Runner")

        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(680,20,21,181))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(13)))
        self.pushButton_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(680,220,16,171))
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")

        self.Display = QtGui.QTextBrowser(self.centralwidget)
        self.Display.setGeometry(QtCore.QRect(20,10,651,192))
        self.Display.setObjectName("Display")

        self.Closer = QtGui.QPushButton(self.centralwidget)
        self.Closer.setGeometry(QtCore.QRect(600,400,75,23))
        self.Closer.setObjectName("Closer")

        self.KonsoleEm = QtGui.QTextEdit(self.centralwidget)
        self.KonsoleEm.setGeometry(QtCore.QRect(20,220,651,171))
        self.KonsoleEm.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(4)))
        self.KonsoleEm.setObjectName("KonsoleEm")
        Kontrol.setCentralWidget(self.centralwidget)

        self.retranslateUi(Kontrol)
        QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL("clicked()"),self.Display.clear)
        QtCore.QObject.connect(self.pushButton_5,QtCore.SIGNAL("clicked()"),self.KonsoleEm.clear)
        QtCore.QObject.connect(self.Closer,QtCore.SIGNAL("clicked()"),Kontrol.close)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),self.KonsoleEm.clear)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),self.Display.clear)
        QtCore.QMetaObject.connectSlotsByName(Kontrol)

    def retranslateUi(self, Kontrol):
        Kontrol.setWindowTitle(QtGui.QApplication.translate("Kontrol", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Kontrol", "Clear All", None, QtGui.QApplication.UnicodeUTF8))
        self.changer.setText(QtGui.QApplication.translate("Kontrol", "Change Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.MacroSave.setText(QtGui.QApplication.translate("Kontrol", "Save As Macro", None, QtGui.QApplication.UnicodeUTF8))
        self.Runner.setText(QtGui.QApplication.translate("Kontrol", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Kontrol", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("Kontrol", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.Closer.setText(QtGui.QApplication.translate("Kontrol", "Close", None, QtGui.QApplication.UnicodeUTF8))

