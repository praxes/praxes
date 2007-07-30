# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Konsole.ui'
#
# Created: Mon Jul 30 17:16:19 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_Kontrol(object):
    def setupUi(self, Kontrol):
        Kontrol.setObjectName("Kontrol")
        Kontrol.resize(QtCore.QSize(QtCore.QRect(0,0,1252,684).size()).expandedTo(Kontrol.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(Kontrol)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120,600,75,23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.changer = QtGui.QPushButton(self.centralwidget)
        self.changer.setGeometry(QtCore.QRect(320,600,75,23))
        self.changer.setObjectName("changer")

        self.MacroSave = QtGui.QPushButton(self.centralwidget)
        self.MacroSave.setGeometry(QtCore.QRect(210,600,101,23))
        self.MacroSave.setObjectName("MacroSave")

        self.Runner = QtGui.QPushButton(self.centralwidget)
        self.Runner.setGeometry(QtCore.QRect(30,600,75,23))
        self.Runner.setObjectName("Runner")

        self.Closer = QtGui.QPushButton(self.centralwidget)
        self.Closer.setGeometry(QtCore.QRect(610,600,75,23))
        self.Closer.setObjectName("Closer")

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(490,600,75,26))
        self.pushButton.setObjectName("pushButton")

        self.Display = QtGui.QTextBrowser(self.centralwidget)
        self.Display.setGeometry(QtCore.QRect(20,10,791,301))
        self.Display.setObjectName("Display")

        self.KonsoleEm = QtGui.QTextEdit(self.centralwidget)
        self.KonsoleEm.setGeometry(QtCore.QRect(20,340,791,251))
        self.KonsoleEm.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(4)))
        self.KonsoleEm.setObjectName("KonsoleEm")

        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(820,10,21,301))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape(13)))
        self.pushButton_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(820,340,21,241))
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")

        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(860,10,371,581))
        self.treeWidget.setObjectName("treeWidget")
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
        self.Closer.setText(QtGui.QApplication.translate("Kontrol", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Kontrol", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Kontrol", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("Kontrol", "X", None, QtGui.QApplication.UnicodeUTF8))

