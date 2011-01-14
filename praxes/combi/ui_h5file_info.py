# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python_11June2010Release\h5file_info.ui'
#
# Created: Fri Jun 18 10:17:59 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_h5infoDialog(object):
    def setupUi(self, h5infoDialog):
        h5infoDialog.setObjectName("h5infoDialog")
        h5infoDialog.resize(962, 480)
        self.layoutWidget = QtGui.QWidget(h5infoDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 951, 461))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.logLabel = QtGui.QLabel(self.layoutWidget)
        self.logLabel.setObjectName("logLabel")
        self.gridLayout_2.addWidget(self.logLabel, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy)
        self.logBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logBrowser.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.logBrowser.setObjectName("logBrowser")
        self.gridLayout_2.addWidget(self.logBrowser, 1, 0, 1, 1)
        self.treeWidget = QtGui.QTreeWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeWidget.setObjectName("treeWidget")
        self.gridLayout_2.addWidget(self.treeWidget, 1, 1, 2, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(h5infoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), h5infoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), h5infoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(h5infoDialog)

    def retranslateUi(self, h5infoDialog):
        h5infoDialog.setWindowTitle(QtGui.QApplication.translate("h5infoDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.logLabel.setText(QtGui.QApplication.translate("h5infoDialog", "log of modifications on ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("h5infoDialog", "h5 file structure", None, QtGui.QApplication.UnicodeUTF8))
        self.logBrowser.setToolTip(QtGui.QApplication.translate("h5infoDialog", "This is a text log of activity for this spec group. For relevant commands, a descritptive line of text is added upon completion of the command.", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.setToolTip(QtGui.QApplication.translate("h5infoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This tree structure shows all the objects in the spec group. The basic format is &lt;name&gt; for groups and &lt;name&gt;(&lt;shape&gt;) for datasets and \'&lt;name&gt;\':&lt;value&gt; for attributes.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("h5infoDialog", "1", None, QtGui.QApplication.UnicodeUTF8))

