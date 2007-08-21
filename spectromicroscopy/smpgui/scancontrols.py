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
from spectromicroscopy.smpcore import specutils, specrunner

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

        self.axes = []
        self.axesTab.removeTab(0)

        scans = specutils.SCAN_NUM_AXES.keys()
        scans.sort()
        self.scanTypeComboBox.addItems(scans)
        self.setScanType(scans[0])
        
        # QStackedLayout is not included in designer, do it manually
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Fixed)
        self.scanButton = QtGui.QPushButton(self.scanControlsGroupBox)
        self.scanButton.setText('Scan')
        self.scanButton.setSizePolicy(sizePolicy)
        self.scanButton.setMaximumHeight(26)
        self.pauseButton = QtGui.QPushButton(self.scanControlsGroupBox)
        self.pauseButton.setText('Pause')
        self.pauseButton.setSizePolicy(sizePolicy)
        self.pauseButton.setMaximumHeight(26)
        self.resumeButton = QtGui.QPushButton(self.scanControlsGroupBox)
        self.resumeButton.setText('Resume')
        self.resumeButton.setSizePolicy(sizePolicy)
        self.resumeButton.setMaximumHeight(26)
        
        self.scanStackedLayout = QtGui.QStackedLayout(self.scanFrame)
        self.scanStackedLayout.setGeometry(self.scanButton.geometry())
        self.scanStackedLayout.setContentsMargins(0, 0, 0, 0)
        self.scanStackedLayout.addWidget(self.scanButton)
        self.scanStackedLayout.addWidget(self.pauseButton)
        self.scanStackedLayout.addWidget(self.resumeButton)
        
        self.abortButton = QtGui.QPushButton(self.scanControlsGroupBox)
        self.abortButton.setSizePolicy(sizePolicy)
        self.abortButton.setEnabled(False)
        self.abortButton.setText('Abort')
        self.vboxlayout.addWidget(self.abortButton)

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
        enabled = [m for m in self.axes if m.isEnabled()]
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
        self.scanFinished()
        self.activityFinished()

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
        self.disconnectAxesSignals()
        self.scanStackedLayout.setCurrentWidget(self.pauseButton)

    def scanFinished(self):
        self.scanTypeComboBox.setEnabled(True)
        self.connectAxesSignals()
        self.scanStackedLayout.setCurrentWidget(self.scanButton)

    def scanPaused(self):
        self.specRunner.abort()
        self.scanStackedLayout.setCurrentWidget(self.resumeButton)

    def scanResumed(self):
        self.specRunner.scan.resumeScan()
        self.scanStackedLayout.setCurrentWidget(self.pauseButton)

    def setScanType(self, scanType):
        scanType = str(scanType)
        self.setAxes(scanType)
        flag = scanType in ('mesh','ascan','a2scan','a3scan')
        self.emit(QtCore.SIGNAL("scanType(string)"), scanType)
        self.setIndependentStepsEnabled(flag)

    def setIndependentStepsEnabled(self, val=False):
        for m in self.axes:
            m.scanStepsSpinBox.setEnabled(val)
        self.scanStepsSpinBox.setEnabled(not val)

    def setAxes(self, scanType):
        self.disconnectAxesSignals()
    
        numAxes = specutils.SCAN_NUM_AXES[scanType]
        self.setUpdatesEnabled(False)
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
        self.setUpdatesEnabled(True)
        self.connectAxesSignals()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
