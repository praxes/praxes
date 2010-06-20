# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JohnnyG\Documents\CHESS\XRDproject_Python_11June2010Release\wavepeak_1d.ui'
#
# Created: Fri Jun 18 10:18:01 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_wavepeak1dDialog(object):
    def setupUi(self, wavepeak1dDialog):
        wavepeak1dDialog.setObjectName("wavepeak1dDialog")
        wavepeak1dDialog.resize(669, 133)
        self.buttonBox = QtGui.QDialogButtonBox(wavepeak1dDialog)
        self.buttonBox.setGeometry(QtCore.QRect(470, 80, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.typeComboBox = QtGui.QComboBox(wavepeak1dDialog)
        self.typeComboBox.setGeometry(QtCore.QRect(440, 46, 211, 26))
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeLabel = QtGui.QLabel(wavepeak1dDialog)
        self.typeLabel.setGeometry(QtCore.QRect(450, 30, 46, 14))
        self.typeLabel.setObjectName("typeLabel")
        self.maxqs_spinBox = QtGui.QDoubleSpinBox(wavepeak1dDialog)
        self.maxqs_spinBox.setGeometry(QtCore.QRect(230, 60, 81, 22))
        self.maxqs_spinBox.setSingleStep(0.1)
        self.maxqs_spinBox.setProperty("value", QtCore.QVariant(1.5))
        self.maxqs_spinBox.setObjectName("maxqs_spinBox")
        self.wavenoisecutoff_spinBox = QtGui.QDoubleSpinBox(wavepeak1dDialog)
        self.wavenoisecutoff_spinBox.setGeometry(QtCore.QRect(330, 60, 99, 20))
        self.wavenoisecutoff_spinBox.setMinimum(-99999.0)
        self.wavenoisecutoff_spinBox.setMaximum(99999.0)
        self.wavenoisecutoff_spinBox.setSingleStep(0.1)
        self.wavenoisecutoff_spinBox.setProperty("value", QtCore.QVariant(20.0))
        self.wavenoisecutoff_spinBox.setObjectName("wavenoisecutoff_spinBox")
        self.minridgelength_spinBox = QtGui.QSpinBox(wavepeak1dDialog)
        self.minridgelength_spinBox.setGeometry(QtCore.QRect(10, 40, 99, 20))
        self.minridgelength_spinBox.setMaximum(100000000)
        self.minridgelength_spinBox.setSingleStep(10000)
        self.minridgelength_spinBox.setProperty("value", QtCore.QVariant(2))
        self.minridgelength_spinBox.setObjectName("minridgelength_spinBox")
        self.minridgewtsum_spinBox = QtGui.QDoubleSpinBox(wavepeak1dDialog)
        self.minridgewtsum_spinBox.setGeometry(QtCore.QRect(110, 40, 91, 21))
        self.minridgewtsum_spinBox.setMinimum(0.0)
        self.minridgewtsum_spinBox.setMaximum(9999999.0)
        self.minridgewtsum_spinBox.setProperty("value", QtCore.QVariant(100.0))
        self.minridgewtsum_spinBox.setObjectName("minridgewtsum_spinBox")
        self.label_4 = QtGui.QLabel(wavepeak1dDialog)
        self.label_4.setGeometry(QtCore.QRect(110, 10, 111, 29))
        self.label_4.setObjectName("label_4")
        self.label = QtGui.QLabel(wavepeak1dDialog)
        self.label.setGeometry(QtCore.QRect(225, 30, 106, 29))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(wavepeak1dDialog)
        self.label_2.setGeometry(QtCore.QRect(15, 10, 86, 29))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(wavepeak1dDialog)
        self.label_3.setGeometry(QtCore.QRect(340, 30, 86, 29))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtGui.QLabel(wavepeak1dDialog)
        self.label_5.setGeometry(QtCore.QRect(110, 70, 91, 29))
        self.label_5.setObjectName("label_5")
        self.minchildwtsum_spinBox = QtGui.QDoubleSpinBox(wavepeak1dDialog)
        self.minchildwtsum_spinBox.setGeometry(QtCore.QRect(110, 100, 91, 21))
        self.minchildwtsum_spinBox.setMinimum(0.0)
        self.minchildwtsum_spinBox.setMaximum(9999999.0)
        self.minchildwtsum_spinBox.setProperty("value", QtCore.QVariant(0.0))
        self.minchildwtsum_spinBox.setObjectName("minchildwtsum_spinBox")
        self.minchildlength_spinBox = QtGui.QSpinBox(wavepeak1dDialog)
        self.minchildlength_spinBox.setGeometry(QtCore.QRect(10, 100, 99, 20))
        self.minchildlength_spinBox.setMaximum(100000000)
        self.minchildlength_spinBox.setSingleStep(10000)
        self.minchildlength_spinBox.setProperty("value", QtCore.QVariant(0))
        self.minchildlength_spinBox.setObjectName("minchildlength_spinBox")
        self.label_6 = QtGui.QLabel(wavepeak1dDialog)
        self.label_6.setGeometry(QtCore.QRect(20, 70, 86, 29))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(wavepeak1dDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), wavepeak1dDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), wavepeak1dDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(wavepeak1dDialog)

    def retranslateUi(self, wavepeak1dDialog):
        wavepeak1dDialog.setWindowTitle(QtGui.QApplication.translate("wavepeak1dDialog", "select values for 1d peak search", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setToolTip(QtGui.QApplication.translate("wavepeak1dDialog", "The dataset in which peaks will be identified.", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLabel.setText(QtGui.QApplication.translate("wavepeak1dDialog", "select", None, QtGui.QApplication.UnicodeUTF8))
        self.maxqs_spinBox.setToolTip(QtGui.QApplication.translate("wavepeak1dDialog", "If the global maximum of the wavelet transform intensity in a ridge occurs at a wavelet scale above this value, the ridge will not be counted as a peak. Ancestor ridges are not considered in the global maximum.", None, QtGui.QApplication.UnicodeUTF8))
        self.wavenoisecutoff_spinBox.setToolTip(QtGui.QApplication.translate("wavepeak1dDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This is the critical wavelet transform intensity for local maxima in the wavelet transform to be included in the set of ridges and should be set near the noise level inthe wavelet transform. </span> Use trial and error with the \"Visualization-&gt;plot 1D wavetrans\" in the main menu - if there are lots local maxima identified where peaks are not evident in the data, raise this value.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.minridgelength_spinBox.setToolTip(QtGui.QApplication.translate("wavepeak1dDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The minimum number of wavelet transform local maxima in a ridge for it to count as a peak. Ancestor ridges are included in this calculation.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.minridgewtsum_spinBox.setToolTip(QtGui.QApplication.translate("wavepeak1dDialog", "For a ridge to be counted as a peak, the sum of the wavelet transform intensity over the local maxima in the ridge must be bigger than this value. The \"wavelet noise cutoff\" should be set near the noise threshold in the wavelet transform, and this value should be set significantly higher than that. Use trial and error with the \"Visualization->plot 1D wavetrans\" in the main menu - if there are too many falsely identified peaks, raise this value.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("wavepeak1dDialog", "min. total wave\n"
"trans. for ridge", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("wavepeak1dDialog", "max wavelet\n"
"q scale of peak", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("wavepeak1dDialog", "minimum\n"
"ridge length", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("wavepeak1dDialog", "wavelet\n"
"noise cutoff", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("wavepeak1dDialog", "min. total WT\n"
"for child ridge", None, QtGui.QApplication.UnicodeUTF8))
        self.minchildwtsum_spinBox.setToolTip(QtGui.QApplication.translate("wavepeak1dDialog", "If this value is 0, the algorithm is maximally sensitive to overlapped peaks. If this value is equal to the above \"min. total ..ridge\", the algorithm will essentially identify overlapped peaks as a single peak. Use trial and error with the \"Visualization->plot 1D wavetrans\" in the main menu - if there are wide single peaks in the data that are being identified as multiple split peaks, raise this value.", None, QtGui.QApplication.UnicodeUTF8))
        self.minchildlength_spinBox.setToolTip(QtGui.QApplication.translate("wavepeak1dDialog", "The minimum number of wavelet transform local maxima in a child ridge for it to count as a peak.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("wavepeak1dDialog", "min. child\n"
"ridge length", None, QtGui.QApplication.UnicodeUTF8))

