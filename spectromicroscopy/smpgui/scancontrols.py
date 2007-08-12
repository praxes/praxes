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
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import scanmotor, ui_scancontrols
from spectromicroscopy.smpcore import specutils, specrunner, qtspecscan

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanControls(ui_scancontrols.Ui_ScanControls, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)

        try:
            self.specRunner = parent.specRunner
        except AttributeError:
            self.specRunner = specrunner.SpecRunner(timeout = 500)

        # TODO: where to create the scan?
        self.specRunner.scan = \
            qtspecscan.QtSpecScanA(self.specRunner.specVersion)

        self.motors = []
        for ax, m in zip(('axis: 1', '2', '3'),
                         ('samx', 'samz', 'samy')):
            self.motors.append(scanmotor.ScanMotor(self, m))
            self.motorTab.addTab(self.motors[-1], ax)
        self.motorTab.removeTab(0)

        scans = specutils.SCAN_NUM_MOTORS.keys()
        scans.sort()
        self.scanTypeComboBox.addItems(scans)
        self.setScanType(scans[0])

        self.connectMotorSignals()
        self.connect(self.scanTypeComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.setScanType)
        self.connect(self.abortButton,
                     QtCore.SIGNAL("clicked()"),
                     self.abort)
        self.connect(self.scanButton,
                     QtCore.SIGNAL("clicked()"),
                     self.startScan)
        self.connect(self.pauseButton,
                     QtCore.SIGNAL("clicked()"),
                     self.scanPauseResume)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("scanStarted()"),
                     self.scanStarted)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("scanStarted()"),
                     self.activityStarted)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("scanFinished()"),
                     self.scanFinished)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("scanFinished()"),
                     self.activityFinished)

    def connectMotorSignals(self):
        for motor in self.motors:
            self.connect(motor,
                         QtCore.SIGNAL("motorActive()"),
                         self.activityStarted)
            self.connect(motor,
                         QtCore.SIGNAL("motorReady()"),
                         self.activityFinished)

    def disconnectMotorSignals(self):
        for motor in self.motors:
            self.disconnect(motor,
                            QtCore.SIGNAL("motorActive()"),
                            self.activityStarted)
            self.disconnect(motor,
                            QtCore.SIGNAL("motorReady()"),
                            self.activityFinished)

    def startScan(self):
        enabled = [m for m in self.motors if m.isEnabled()]
        scantype = str(self.scanTypeComboBox.currentText())

        scanArgs = []
        for m in enabled:
            scanArgs.extend(m.getScanInfo())
        if self.scanStepsSpinBox.isEnabled():
            scanArgs.append(self.scanStepsSpinBox.value())
        scanArgs.append( self.scanCountSpinBox.value() )

        getattr(self.specRunner.scan, scantype)(*scanArgs)

    def abort(self):
        self.specRunner.abort()
        self.pauseButton.setText('Pause')
        self.scanFinished()
        self.activityFinished()

    def activityStarted(self):
        self.motorTab.setEnabled(False)
        self.abortButton.setEnabled(True)
        self.scanButton.setEnabled(False)

    def activityFinished(self):
        self.motorTab.setEnabled(True)
        self.abortButton.setEnabled(False)
        self.scanButton.setEnabled(True)

    def scanStarted(self):
        self.scanTypeComboBox.setEnabled(False)
        self.disconnectMotorSignals()
        self.pauseButton.setEnabled(True)

    def scanFinished(self):
        self.scanTypeComboBox.setEnabled(True)
        self.connectMotorSignals()
        self.pauseButton.setEnabled(False)

    def scanPauseResume(self):
        event = str(self.pauseButton.text())
        if event == 'Pause':
            self.specRunner.abort()
            self.pauseButton.setText('Resume')
        else:
            self.pauseButton.setText('Pause')
            self.specRunner.scan.resumeScan()

    def setScanType(self, scanType):
        scanType = str(scanType)
        flag = scanType in ('mesh')
        self.setIndependentStepsEnabled(flag)
        numMotors = specutils.SCAN_NUM_MOTORS[scanType]
        self.setMotorsEnabled(numMotors)

    def setIndependentStepsEnabled(self, val=False):
        for m in self.motors:
            m.scanStepsSpinBox.setEnabled(val)
        self.scanStepsSpinBox.setEnabled(not val)

    def setMotorsEnabled(self, numMotors):
        for m, i in zip(self.motors, xrange(len(self.motors))):
            m.setEnabled(numMotors > i)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
