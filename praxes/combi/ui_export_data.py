# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\XRDproject_Python_11June2010Release backup\export_data.ui'
#
# Created: Mon Jun 14 16:20:36 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_export_data(object):
    def setupUi(self, export_data):
        export_data.setObjectName("export_data")
        export_data.resize(365, 341)
        self.buttonBox = QtGui.QDialogButtonBox(export_data)
        self.buttonBox.setGeometry(QtCore.QRect(15, 295, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.png_2D_Browser = QtGui.QTextBrowser(export_data)
        self.png_2D_Browser.setGeometry(QtCore.QRect(0, 24, 111, 253))
        self.png_2D_Browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.png_2D_Browser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.png_2D_Browser.setObjectName("png_2D_Browser")
        self.textBrowser = QtGui.QTextBrowser(export_data)
        self.textBrowser.setGeometry(QtCore.QRect(111, 24, 97, 105))
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtGui.QLabel(export_data)
        self.label.setGeometry(QtCore.QRect(63, 4, 201, 16))
        self.label.setObjectName("label")
        self.col_checkBox = QtGui.QCheckBox(export_data)
        self.col_checkBox.setGeometry(QtCore.QRect(115, 132, 161, 19))
        self.col_checkBox.setChecked(True)
        self.col_checkBox.setObjectName("col_checkBox")
        self.col_auto_checkBox = QtGui.QCheckBox(export_data)
        self.col_auto_checkBox.setGeometry(QtCore.QRect(115, 180, 166, 19))
        self.col_auto_checkBox.setChecked(True)
        self.col_auto_checkBox.setObjectName("col_auto_checkBox")
        self.col_min_SpinBox = QtGui.QDoubleSpinBox(export_data)
        self.col_min_SpinBox.setGeometry(QtCore.QRect(115, 216, 89, 22))
        self.col_min_SpinBox.setMaximum(9999999.0)
        self.col_min_SpinBox.setObjectName("col_min_SpinBox")
        self.label_2 = QtGui.QLabel(export_data)
        self.label_2.setGeometry(QtCore.QRect(115, 200, 87, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(export_data)
        self.label_3.setGeometry(QtCore.QRect(115, 240, 91, 16))
        self.label_3.setObjectName("label_3")
        self.col_max_SpinBox = QtGui.QDoubleSpinBox(export_data)
        self.col_max_SpinBox.setGeometry(QtCore.QRect(115, 256, 89, 22))
        self.col_max_SpinBox.setMaximum(9999999.0)
        self.col_max_SpinBox.setObjectName("col_max_SpinBox")
        self.col_log_checkBox = QtGui.QCheckBox(export_data)
        self.col_log_checkBox.setGeometry(QtCore.QRect(115, 156, 171, 19))
        self.col_log_checkBox.setObjectName("col_log_checkBox")

        self.retranslateUi(export_data)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), export_data.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), export_data.reject)
        QtCore.QMetaObject.connectSlotsByName(export_data)

    def retranslateUi(self, export_data):
        export_data.setWindowTitle(QtGui.QApplication.translate("export_data", "Enter data to be exported", None, QtGui.QApplication.UnicodeUTF8))
        self.png_2D_Browser.setHtml(QtGui.QApplication.translate("export_data", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">raw data:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">  </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">p###</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  Bin.p###</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">background:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  bmin, bminbin</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  bave, bavebin</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  banom###</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  bimap</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  killmap</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">integration:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">imap</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">correlation:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  qq, qq###</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">phase map:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("export_data", "save 2d  images to .png", None, QtGui.QApplication.UnicodeUTF8))
        self.col_checkBox.setText(QtGui.QApplication.translate("export_data", "Include Colorbar", None, QtGui.QApplication.UnicodeUTF8))
        self.col_auto_checkBox.setText(QtGui.QApplication.translate("export_data", "Auto Color Scale", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("export_data", "min colorbar value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("export_data", "max colorbar value", None, QtGui.QApplication.UnicodeUTF8))
        self.col_log_checkBox.setText(QtGui.QApplication.translate("export_data", "Log10 colorscale", None, QtGui.QApplication.UnicodeUTF8))

