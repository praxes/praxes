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
        for ax, m in zip(('axis: X', 'Y', 'Z'),
                         ('samx', 'samy', 'samz')):
            self.motors.append(scanmotor.ScanMotor(self, m))
            self.motorTab.addTab(self.motors[-1], ax)
        self.motorTab.removeTab(0)

        scans = specutils.SCAN_NUM_MOTORS.keys()
        scans.sort()
        self.scanTypeComboBox.addItems(scans)
        self.scanEnabled(scans[0])

        self.connect(self.scanTypeComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.scanEnabled)
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
                     self.scanEnabled)

    def abort(self):
        self.specRunner.abort()
        self.scanEnabled()
        self.pauseButton.setEnabled(False)

    def startScan(self):
        enabled = [m for m in self.motors if m.isEnabled()]
        scantype = str(self.scanTypeComboBox.currentText())
        motors = [str(m.motorComboBox.currentText()) for m in enabled]
        scanFrom = [m.scanFromSpinBox.value() for m in enabled]
        scanTo = [m.scanToSpinBox.value() for m in enabled]
        scanSteps = [m.scanStepsSpinBox.value() for m in self.motors \
                     if m.scanStepsSpinBox.isEnabled()]
        if scanSteps:
            scanZip = zip(motors, scanFrom, scanTo, scanSteps)
        else:
            scanZip = zip(motors, scanFrom, scanTo)
            scanZip.append(self.scanStepsSpinBox.value())
        scanArgs = []
        for i in scanZip:
            try:
                scanArgs.extend(i)
            except TypeError:
                scanArgs.append(i)
        scanArgs.append( float(self.scanCountSpinBox.value()) )
        scan = getattr(self.specRunner.scan, scantype)
        scan(*scanArgs)

    def activityStarted(self):
        self.setMotorsEnabled(0)
        self.abortButton.setEnabled(True)
        self.scanButton.setEnabled(False)

    def scanPauseResume(self):
        event = str(self.pauseButton.text())
        if event == 'Pause':
            self.specRunner.abort()
            self.pauseButton.setText('Resume')
        else:
            self.pauseButton.setText('Pause')
            self.specRunner.scan.resumeScan()

    def scanStarted(self):
        self.scanTypeComboBox.setEnabled(False)
        self.pauseButton.setEnabled(True)

    def scanEnabled(self, scanType=None):
        if scanType:
            # scan type changed
            scanType = str(scanType)
            flag = scanType in ('mesh')
            self.setIndependentStepsEnabled(flag)
        else:
            # scan ending, enabling widgets
            scanType = str(self.scanTypeComboBox.currentText())
            self.scanTypeComboBox.setEnabled(True)
            self.abortButton.setEnabled(False)
            self.pauseButton.setEnabled(False)
            self.scanButton.setEnabled(True)
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
