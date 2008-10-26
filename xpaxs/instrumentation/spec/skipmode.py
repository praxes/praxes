"""

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_scancontrols,  ui_scandialog

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SkipMode(ui_skipmode.Ui_SkipMode, QtGui.QWidget):

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
        self.precountSpin.setValue(val)

        counters = [''] + self.specRunner.getCountersMne()
        self.counterBox.addItems(counters)
        try:
            i = counters.index(settings.value('counter').toString())
            self.counterBox.setCurrentIndex(i)
        except ValueError:
            pass

    @QtCore.pyqtSignature("QString")
    def on_counterComboBox_currentIndexChanged(self, val):
        isEnabled = bool(val)
        self.thresholdSpinBox.setEnabled(isEnabled)
        self.thresholdLabel.setEnabled(isEnabled)
        self.precountSpinBox.setEnabled(isEnabled)
        self.precountLabel.setEnabled(isEnabled)

    def closeEvent(self, event):
        settings = QtCore.QSettings()
        settings.beginGroup("SkipModeOptions")
        settings.setValue(
            'counter',
            QtCore.QVariant( str(self.counterComboBox.currentText()) )
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

    def configure(self):
        sm_counter = str(self.counterComboBox.currentText())
        sm_threshold = self.thresholdSpinBox.value()
        sm_precount = self.precountSpinBox.value()

        if bool(sm_precount) and bool(sm_counter):
            self.specRunner(
                str("skipmode %s %s %s"%(sm_precount, sm_counter, sm_threshold))
            )

        else:
            self.specRunner('skipmode 0')


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
