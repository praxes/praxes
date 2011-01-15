"""
"""
from __future__ import absolute_import

from PyQt4 import QtCore, QtGui

from .ui import ui_skipmode


class SkipModeWidget(ui_skipmode.Ui_SkipModeWidget, QtGui.QWidget):

    """Dialog for setting spec scan options"""

    def __init__(self, specRunner, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = specRunner

        settings = QtCore.QSettings()
        settings.beginGroup("SkipModeOptions")

        val = settings.value('threshold', QtCore.QVariant(0)).toInt()[0]
        self.thresholdSpinBox.setValue(val)

        val = settings.value('precount', QtCore.QVariant(0)).toDouble()[0]
        self.precountSpinBox.setValue(val)

        counters = [''] + self.specRunner.getCountersMne()
        self.counterComboBox.addItems(counters)
        try:
            i = counters.index(settings.value('counter').toString())
            self.counterComboBox.setCurrentIndex(i)
        except ValueError:
            pass

        self.connect(
            self.specRunner,
            QtCore.SIGNAL("specBusy"),
            self.setBusy
        )

    @QtCore.pyqtSignature("QString")
    def on_counterComboBox_currentIndexChanged(self, val):
        isEnabled = bool(val)
        self.thresholdSpinBox.setEnabled(isEnabled)
        self.thresholdLabel.setEnabled(isEnabled)
        self.precountSpinBox.setEnabled(isEnabled)
        self.precountLabel.setEnabled(isEnabled)

        self.configure(channel=val)

    @QtCore.pyqtSignature("")
    def on_precountSpinBox_editingFinished(self):
        self.configure(precount=self.precountSpinBox.value())

    @QtCore.pyqtSignature("")
    def on_thresholdSpinBox_editingFinished(self):
        self.configure(threshold=self.thresholdSpinBox.value())

    def closeEvent(self, event):
        settings = QtCore.QSettings()
        settings.beginGroup("SkipModeOptions")
        settings.setValue(
            'counter',
            QtCore.QVariant(self.counterComboBox.currentText())
        )
        settings.setValue(
            'threshold',
            QtCore.QVariant(self.thresholdSpinBox.value())
        )
        settings.setValue(
            'precount',
            QtCore.QVariant(self.precountSpinBox.value())
        )

        event.accept()

    def configure(self, channel=None, precount=None, threshold=None):
        if channel is None:
            channel = str(self.counterComboBox.currentText())

        if threshold is None:
            threshold = self.thresholdSpinBox.value()

        if precount is None:
            precount = self.precountSpinBox.value()

        if bool(precount) and bool(channel):
            self.specRunner(
                str("skipmode %s %s %s"%(precount, channel, threshold))
            )

        else:
            self.specRunner('skipmode 0')

    def setBusy(self, busy):
        self.setDisabled(busy)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
