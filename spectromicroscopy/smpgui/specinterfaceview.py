"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import sys
import time
import weakref

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy import configutils
from spectromicroscopy.smpgui import ui_smpspecinterface
from spectromicroscopy.smpgui import pymcafitparams, scancontrols
from spectromicroscopy.smpcore import specrunner
from SpecClient import SpecClientError

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SmpSpecScanOptionsDialog(QtGui.QDialog):

    """
    """

    def __init__(self, parent):
        super(SmpSpecScanOptionsDialog, self).__init__(parent)

        pymcaConfigFile = configutils.getDefaultPymcaConfigFile()
        self.pymcaConfig = configutils.getPymcaConfig(pymcaConfigFile)
#        self.pymcaConfigWidget = pymcafitparams.PyMcaFitParams(self)
#        self.pymcaConfigWidget.setParameters(self.pymcaConfig)
#        self.tabWidget.insertTab(1, self.pymcaConfigWidget,
#                                 'PyMca Configuration')

        self.getDefaults()

    def closeEvent(self):
        dtc_enabled = self.deadtimeCorrCheckBox.isChecked()
        sm_enabled = self.skipmodeCheckBox.isChecked()
        sm_counter = self.skipmodeCounterComboBox.currentText()
        sm_threshold = self.skipmodeThreshSpinBox.value()
        sm_precount = self.skipmodePrecountSpinBox.value()

        # TODO: this needs to be fixed:
        self.specRunner.skipmode(sm_enabled, sm_precount, str(sm_counter),
                                 sm_threshold)

        settings = QtGui.QSettings()
        settings.beginGroup("SpecScanOptionsDialog")
        settings.setValue('DeadTimeCorrection/enabled',
                          QtCore.QVariant(dtc_enabled))
        settings.setValue('SkipMode/enabled', QtCore.QVariant(sm_enabled))
        settings.setValue('SkipMode/counter', QtCore.QVariant(sm_counter))
        settings.setValue('SkipMode/threshold', QtCore.QVariant(sm_threshold))
        settings.setValue('SkipMode/precount', QtCore.QVariant(sm_precount))
        return event.accept()

    def getDefaults(self):
        settings = QtGui.QSettings()
        settings.beginGroup("SpecScanOptionsDialog")

        val = settings.value('DeadTimeCorrection/enabled', False).toBool()
        self.deadtimeCorrCheckBox.setChecked(val)

        val = settings.value('SkipMode/enabled', False).toBool()
        self.skipmodeCheckBox.setChecked(val)

        val = settings.value('SkipMode/threshold', 0).toDouble()
        self.skipmodeThreshSpinBox.setValue(val)

        val = settings.value('SkipMode/precount', 1).toDouble()
        self.skipmodePrecountSpinBox.setValue(val)

        # TODO: This needs updating:
        counters = self.specRunner.getCountersMne()
        self.skipmodeCounterComboBox.addItems(counters)
        val = settings.value('SkipMode/counter').toString()
        if val:
            try:
                ind = counters.index(val)
                self.skipmodeCounterComboBox.setCurrentIndex(ind)
            except ValueError:
                pass


class SmpSpecInterface(QtGui.QWidget):

    """Establishes a Experiment controls
    Generates Control and Feedback instances
    Adds Scan atributes to specRunner instance
    """

    def __init__(self, parent=None, statusBar=None):
        QtGui.QWidget.__init__(self, parent)

        self.parent = parent
        self.statusBar = statusBar
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.connectToSpec()

        self.scanControls = scancontrols.ScanControls(self)
        self.gridlayout.addWidget(self.scanControls, 0,0)

    def closeEvent(self, event):
        self.specRunner.skipmode(0)
        self.specRunner.close()
        event.accept()

    def connectToSpec(self):
        specVersion = self.getSpecVersion()
        try:
            self.statusBar.showMessage('Connecting')
            QtGui.qApp.processEvents()
            self.specRunner.runMacro('smp_mca.mac')
            self.statusBar.clearMessage()
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError(specVersion)
            raise SpecClientError.SpecClientTimeoutError

    def connectionError(self, specVersion):
        error = QtGui.QErrorMessage()
        server, port = specVersion.split(':')
        error.showMessage('''\
        SMP was unabel to connect to the "%s" spec instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%(port, server))
        error.exec_()

    def getSpecVersion(self):
        settings = QtCore.QSettings()
        server = "%s"% settings.value('Server').toString()
        port = "%s"% settings.value('Port').toString()
        return ':'.join([server, port])


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = SmpSpecInterface()
    myapp.show()
    sys.exit(app.exec_())
