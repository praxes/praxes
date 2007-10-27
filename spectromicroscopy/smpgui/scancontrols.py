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

from spectromicroscopy import smpConfig
from spectromicroscopy.smpgui import scanmotor, ui_scancontrols
from spectromicroscopy.smpcore import specutils, specrunner

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanControls(ui_scancontrols.Ui_ScanControls, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.specInterface = parent
        self.setupUi(self)

        self.axes = []
        self.axesTab.removeTab(0)

        scans = specutils.SCAN_NUM_AXES.keys()
        scans.sort()
        self.scanTypeComboBox.addItems(scans)
        self.setScanType(scans[0])
        
        self.scanButton = QtGui.QPushButton(self.scanControlsGroupBox)
        self.scanButton.setText('Scan')
        self.pauseButton = QtGui.QPushButton(self.scanControlsGroupBox)
        self.pauseButton.setText('Pause')
        self.resumeButton = QtGui.QPushButton(self.scanControlsGroupBox)
        self.resumeButton.setText('Resume')
        
        self.scanStackedLayout = QtGui.QStackedLayout(self.stackedLayoutFrame)
        self.scanStackedLayout.setContentsMargins(0, 0, 0, 0)
        self.scanStackedLayout.addWidget(self.scanButton)
        self.scanStackedLayout.addWidget(self.pauseButton)
        self.scanStackedLayout.addWidget(self.resumeButton)
        self.stackedLayoutFrame.setGeometry(self.abortButton.geometry())

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
        self.connect(self.specInterface.specRunner.scan,
                     QtCore.SIGNAL("scanStarted()"),
                     self.scanStarted)
        self.connect(self.specInterface.specRunner.scan,
                     QtCore.SIGNAL("scanStarted()"),
                     self.activityStarted)
        self.connect(self.specInterface.specRunner.scan,
                     QtCore.SIGNAL("scanFinished()"),
                     self.scanFinished)
        self.connect(self.specInterface.specRunner.scan,
                     QtCore.SIGNAL("scanFinished()"),
                     self.activityFinished)

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

        scanArgs = []
        for m in self.axes:
            args = m.getScanInfo()
            if self.independentStepsEnabled or m is self.axes[-1]:
                scanArgs.extend(args)
            else:
                scanArgs.extend(args[:-1])
        scanArgs.append( self.scanCountSpinBox.value() )

        getattr(self.specInterface.specRunner.scan, scantype)(*scanArgs)

    def abort(self):
        self.specInterface.specRunner.abort()
        self.scanFinished()
        self.activityFinished()
        self.specInterface.specRunner.scan.scanAborted()

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

    def scanFinished(self):
        self.scanTypeComboBox.setEnabled(True)
        self.scanCountSpinBox.setEnabled(True)
        self.connectAxesSignals()
        self.scanStackedLayout.setCurrentWidget(self.scanButton)

    def scanPaused(self):
        self.specInterface.specRunner.abort()
        self.scanStackedLayout.setCurrentWidget(self.resumeButton)

    def scanResumed(self):
        self.specInterface.specRunner.scan.resumeScan()
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
    
        numAxes = specutils.SCAN_NUM_AXES[scanType]
        self.axesTab.setUpdatesEnabled(False)
        while self.axesTab.count() > 0:
            self.axesTab.removeTab(0)
        self.axes=[]
        
        if scanType in specutils.MOTOR_SCANS:
            for i, ax, m in zip(xrange(numAxes), 
                                ('axis: 1', '2', '3'),
                                ('samx', 'samz', 'samy')):
                if i < numAxes:
                    self.axes.append(scanmotor.ScanMotor(self, m))
                    self.axesTab.addTab(self.axes[-1], ax)
        self.axesTab.setUpdatesEnabled(True)
        self.connectAxesSignals()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
