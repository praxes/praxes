"""
This is a library that subclasses many of the generic qt spec classes to
provide support specific to the spectromicroscopy package.
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

from xpaxs.spec.client import utils
from xpaxs.spec.ui import scanmotor, ui_scancontrols

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanControls(ui_scancontrols.Ui_ScanControls, QtGui.QWidget):

    """Provides a GUI interface for positioning motors and running scans"""

    def __init__(self, specRunner, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.specRunner = specRunner
        self.setupUi(self)

        self.axes = []
        self.axesTab.removeTab(0)
        self.progressBar.setVisible(False)

        scans = list(utils.MOTOR_SCANS)
        self.scanTypeComboBox.addItems(scans)
        self.setScanType(scans[0])

        self.scanButton = QtGui.QPushButton(self)
        self.scanButton.setText('Scan')
        self.pauseButton = QtGui.QPushButton(self)
        self.pauseButton.setText('Pause')
        self.resumeButton = QtGui.QPushButton(self)
        self.resumeButton.setText('Resume')

        self.scanStackedLayout = QtGui.QStackedLayout(self.stackedLayoutFrame)
        self.scanStackedLayout.setContentsMargins(0, 0, 0, 0)
        self.scanStackedLayout.addWidget(self.scanButton)
        self.scanStackedLayout.addWidget(self.pauseButton)
        self.scanStackedLayout.addWidget(self.resumeButton)
        self.stackedLayoutFrame.setGeometry(self.abortButton.geometry())

        self.connectSignals()

    def connectSignals(self):
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
                     self.scanPaused)
        self.connect(self.resumeButton,
                     QtCore.SIGNAL("clicked()"),
                     self.scanResumed)
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
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newScanIndex(int)"),
                     self.updateProgressBar)

    def connectAxesSignals(self):
        for axis in self.axes:
            self.connect(axis,
                         QtCore.SIGNAL("motorActive()"),
                         self.activityStarted)
            self.connect(axis,
                         QtCore.SIGNAL("motorReady()"),
                         self.activityFinished)

    def disconnectAxesSignals(self):
        for axis in self.axes:
            self.disconnect(axis,
                            QtCore.SIGNAL("motorActive()"),
                            self.activityStarted)
            self.disconnect(axis,
                            QtCore.SIGNAL("motorReady()"),
                            self.activityFinished)

    def startScan(self):
        scantype = str(self.scanTypeComboBox.currentText())
        scanPoints = 1
        scanArgs = []
        for m in self.axes:
            args = m.getScanInfo()
            if self.independentStepsEnabled or m is self.axes[-1]:
                scanArgs.extend(args)
                scanPoints *= scanArgs[-1]+1
            else:
                scanArgs.extend(args[:-1])
        scanArgs.append( self.scanCountSpinBox.value() )
        self.progressBar.setMaximum(scanPoints)
        getattr(self.specRunner.scan, scantype)(*scanArgs)

    def abort(self):
        self.specRunner.abort()
        self.scanFinished()
        self.activityFinished()
        self.specRunner.scan.scanAborted()

    def activityStarted(self):
        self.axesTab.setEnabled(False)
        self.abortButton.setEnabled(True)
        self.scanButton.setEnabled(False)

    def activityFinished(self):
        self.axesTab.setEnabled(True)
        self.abortButton.setEnabled(False)
        self.scanButton.setEnabled(True)

    def scanStarted(self):
        self.scanTypeComboBox.setEnabled(False)
        self.scanCountSpinBox.setEnabled(False)
        self.disconnectAxesSignals()
        self.scanStackedLayout.setCurrentWidget(self.pauseButton)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)

    def scanFinished(self):
        self.scanTypeComboBox.setEnabled(True)
        self.scanCountSpinBox.setEnabled(True)
        self.connectAxesSignals()
        self.scanStackedLayout.setCurrentWidget(self.scanButton)
        self.progressBar.setVisible(False)

    def scanPaused(self):
        self.specRunner.abort()
        self.scanStackedLayout.setCurrentWidget(self.resumeButton)

    def scanResumed(self):
        self.specRunner.scan.resumeScan()
        self.scanStackedLayout.setCurrentWidget(self.pauseButton)

    def setScanType(self, scanType):
        scanType = str(scanType)
        self.setAxes(scanType)
        self.emit(QtCore.SIGNAL("scanType(string)"), scanType)
        self.setIndependentStepsEnabled(scanType in ('mesh', ))

    def setIndependentStepsEnabled(self, enabled=False):
        self.independentStepsEnabled = enabled
        if enabled:
            for m in self.axes:
                for n in self.axes:
                    if m is not n:
                        m.disconnect(m.scanStepsSpinBox,
                                     QtCore.SIGNAL("valueChanged(int)"),
                                     n.scanStepsSpinBox,
                                     QtCore.SLOT('setValue(int)'))
        else:
            for m in self.axes:
                for n in self.axes:
                    if m is not n:
                        m.connect(m.scanStepsSpinBox,
                                  QtCore.SIGNAL("valueChanged(int)"),
                                  n.scanStepsSpinBox,
                                  QtCore.SLOT('setValue(int)'))

    def setAxes(self, scanType):
        self.disconnectAxesSignals()

        numAxes = utils.SCAN_NUM_AXES[scanType]
        self.axesTab.setUpdatesEnabled(False)
        while self.axesTab.count() > 0:
            self.axesTab.removeTab(0)
        self.axes=[]

        if scanType in utils.MOTOR_SCANS:
            for i, ax, m in zip(xrange(numAxes),
                                ('axis: 1', '2', '3'),
                                ('samx', 'samz', 'samy')):
                if i < numAxes:
                    self.axes.append(scanmotor.ScanMotor(self, m))
                    self.axesTab.addTab(self.axes[-1], ax)
        self.axesTab.setUpdatesEnabled(True)
        self.connectAxesSignals()

    def updateProgressBar(self, val):
        self.progressBar.setValue(val+1)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
