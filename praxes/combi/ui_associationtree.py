# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\associationtree.ui'
#
# Created: Mon Jun 14 16:20:35 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_associationtreeForm(object):
    def setupUi(self, associationtreeForm):
        associationtreeForm.setObjectName("associationtreeForm")
        associationtreeForm.resize(862, 330)
        self.treeAWidget = QtGui.QTreeWidget(associationtreeForm)
        self.treeAWidget.setGeometry(QtCore.QRect(10, 70, 271, 192))
        self.treeAWidget.setObjectName("treeAWidget")
        self.treeBWidget = QtGui.QTreeWidget(associationtreeForm)
        self.treeBWidget.setGeometry(QtCore.QRect(285, 70, 291, 192))
        self.treeBWidget.setObjectName("treeBWidget")
        self.treeCWidget = QtGui.QTreeWidget(associationtreeForm)
        self.treeCWidget.setGeometry(QtCore.QRect(580, 70, 271, 192))
        self.treeCWidget.setObjectName("treeCWidget")
        self.label = QtGui.QLabel(associationtreeForm)
        self.label.setGeometry(QtCore.QRect(10, 50, 271, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(associationtreeForm)
        self.label_2.setGeometry(QtCore.QRect(320, 50, 231, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(associationtreeForm)
        self.label_3.setGeometry(QtCore.QRect(590, 50, 251, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(associationtreeForm)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 551, 28))
        self.label_4.setObjectName("label_4")
        self.plot_treeA_pushButton = QtGui.QPushButton(associationtreeForm)
        self.plot_treeA_pushButton.setGeometry(QtCore.QRect(70, 280, 139, 41))
        self.plot_treeA_pushButton.setObjectName("plot_treeA_pushButton")
        self.plot_treeB_pushButton = QtGui.QPushButton(associationtreeForm)
        self.plot_treeB_pushButton.setGeometry(QtCore.QRect(360, 280, 139, 41))
        self.plot_treeB_pushButton.setObjectName("plot_treeB_pushButton")
        self.label_5 = QtGui.QLabel(associationtreeForm)
        self.label_5.setGeometry(QtCore.QRect(10, 260, 251, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(associationtreeForm)
        QtCore.QMetaObject.connectSlotsByName(associationtreeForm)

    def retranslateUi(self, associationtreeForm):
        associationtreeForm.setWindowTitle(QtGui.QApplication.translate("associationtreeForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.treeAWidget.headerItem().setText(0, QtGui.QApplication.translate("associationtreeForm", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeBWidget.headerItem().setText(0, QtGui.QApplication.translate("associationtreeForm", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeCWidget.headerItem().setText(0, QtGui.QApplication.translate("associationtreeForm", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("associationtreeForm", "1d spectrum->instanced qq peak->associated 1d peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("associationtreeForm", "1d spectrum->1d peak->associated qq peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("associationtreeForm", "qq peaks->1d spectrum containing peak->1d peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("associationtreeForm", "format for qq peaks:   qq#(?,?)            for 1d peaks:    k#(?)            # is the array index and ? are q-values in 1/nm\n"
"three digit numbers refer to substrate point index", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_treeA_pushButton.setText(QtGui.QApplication.translate("associationtreeForm", "plot selection\n"
"(select either type of peak)", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_treeB_pushButton.setText(QtGui.QApplication.translate("associationtreeForm", "plot selection\n"
"(select either type of peak)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("associationtreeForm", "1d peaks not associated with qq peaks at bottom", None, QtGui.QApplication.UnicodeUTF8))

