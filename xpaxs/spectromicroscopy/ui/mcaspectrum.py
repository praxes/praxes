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

from xpaxs import plotwidgets
from xpaxs.spectromicroscopy.ui import ui_mcaspectrum

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class McaSpectrumFigure(plotwidgets.QtMplCanvas):

    def __init__(self, parent=None):
        super(McaSpectrumFigure, self).__init__(parent)
        
        self.fitData = {}

        self.spectrumAxes = self.figure.add_axes([.1, .4, .85, .55])
        self.spectrumAxes.xaxis.set_visible(False)
        self.spectrumAxes.set_ylabel('Counts')
        
        self.residualsAxes = self.figure.add_axes([.1, .125, .85, .225], 
                                                  sharex=self.spectrumAxes)
        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')

    def _createInitialFigure(self, fitData):
        self.dataLine, = self.spectrumAxes.plot(fitData['energy'],
                                                fitData['ydata'],
                                                'b', linewidth=1.5)
        self.fitLine, = self.spectrumAxes.plot(fitData['energy'],
                                               fitData['yfit'],
                                               'k', linewidth=1.5)
        self.spectrumAxes.set_ylabel('Counts')
        
        self.resLine, = self.residualsAxes.plot(fitData['energy'],
                                                fitData['residuals'],
                                                'k', linewidth=1.5)
        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')
        self.emit(QtCore.SIGNAL('enableInteraction()'))

    def enableAutoscale(self, val):
        self.spectrumAxes.set_autoscale_on(val)
        self.residualsAxes.set_autoscale_on(val)
        self.updateFigure()

    def enableLogscale(self, val):
        if val:
            isAutoscaled = self.spectrumAxes.get_autoscale_on()
            self.spectrumAxes.set_autoscale_on(True)
            self.spectrumAxes.set_yscale('log')
            self.updateFigure()
            self.spectrumAxes.set_autoscale_on(isAutoscaled)
        else:
            self.spectrumAxes.set_yscale('linear')
            self.updateFigure()

    def updateFigure(self, fitData=None):
        if self.fitData == {}:
            self._createInitialFigure(fitData)
            self.mcaCountsSummed = fitData['ydata']
            self.numSpectra = 1
        else:
            if fitData is None:
                fitData = self.fitData
            else:
                self.mcaCountsSummed += fitData['ydata']
                self.numSpectra += 1
        
            self.dataLine.set_ydata(fitData['ydata'])
            self.fitLine.set_ydata(fitData['yfit'])
            if self.spectrumAxes.get_yscale() == 'log':
                self.resLine.set_ydata(fitData['logresiduals'])
            else:
                self.resLine.set_ydata(fitData['residuals'])
        
            self.spectrumAxes.relim()
            self.spectrumAxes.autoscale_view()
        
            self.residualsAxes.relim()
            self.residualsAxes.autoscale_view()
        
        self.fitData = fitData
        self.draw()


class McaSpectrum(ui_mcaspectrum.Ui_McaSpectrum, QtGui.QWidget):

    """
    """

    def __init__(self, scan, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        self._scan = scan
        
        self.figure = McaSpectrumFigure(self)
        self.figure.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                           QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addWidget(self.figure, 0, 0, 1, 1)
        self.toolbar = plotwidgets.Toolbar(self.figure, self)
        self.gridlayout2.addWidget(self.toolbar, 1, 0, 1, 1)
        
        self.connect(self.mcaLogscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.figure.enableLogscale)
        self.connect(self.mcaAutoscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.figure.enableAutoscale)
        self.connect(self._scan,
                     QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"),
                     self.updateView)
        self.connect(self.figure,
                     QtCore.SIGNAL('enableInteraction()'),
                     self.enableInteraction)
        self.connect(self.configPyMcaButton,
                     QtCore.SIGNAL("clicked()"),
                     self.launchMcaAdvancedFit)

    def __getattr__(self, attr):
        return getattr(self.figure, attr)

    def launchMcaAdvancedFit(self):
        dialog = QtGui.QDialog()
        layout = QtGui.QVBoxLayout(dialog)
        from PyMca import McaAdvancedFit
        mcaFit = McaAdvancedFit.McaAdvancedFit(dialog)
        mcaFit.mcafit.configure(self.specInterface.pymcaConfig)
        x = self.figure.fitData['xdata'].flatten()
        y = self.figure.mcaCountsSummed.flatten()/self.figure.numSpectra
        mcaFit.setData(x=x, y=y)
        layout.addWidget(mcaFit)
        dialog.exec_()

    def enableInteraction(self):
        self.mcaAutoscaleButton.setEnabled(True)
        self.mcaLogscaleButton.setEnabled(True)

    def updateView(self, data):
        self.figure.updatePlot(data)
