"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyMca.ClassMcaTheory import McaTheory
from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import plotwidgets
from xpaxs.spectromicroscopy.ui import ui_mcaspectrum

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SpectrumAnalysisThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(SpectrumAnalysisThread, self).__init__(parent)

        self.mcafit = McaTheory()

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,
                     QtCore.SIGNAL("timeout()"),
                     self.update)
        self.timer.start(20)

    def run(self):
        self.exec_()




class McaSpectrumFigure(plotwidgets.QtMplCanvas):

    def __init__(self, parent=None):
        super(McaSpectrumFigure, self).__init__(parent)

        self.mcafit = McaTheory()
#        self.mcafit.enableOptimizedLinearFit()
        self.fitData = None

        self.useLogScale = False

        self.spectrumAxes = self.figure.add_axes([.1, .4, .7, .55])
        self.spectrumAxes.xaxis.set_visible(False)
        self.spectrumAxes.set_ylabel('Counts')

        self.residualsAxes = self.figure.add_axes([.1, .125, .7, .225],
                                                  sharex=self.spectrumAxes)
        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')

    def enableLogscale(self, val):
        self.useLogScale = val
        self.updateFigure()

    def analyzeSpectrum(self, channels, counts, config):
        self.fitconfig = fitconfig = self.mcafit.configure(config)
        self.mcafit.setdata(x=channels, y=counts)

        if fitconfig['peaks'] == {}:
            msg = QtGui.QMessageBox(self)
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("No peaks defined.\nPlease configure peaks")
            msg.exec_()
            return

        msg = QtGui.QDialog(self, QtCore.Qt.FramelessWindowHint)
        msg.setModal(0)
        msg.setWindowTitle("Please Wait")
        layout = QtGui.QHBoxLayout(msg)
        label = QtGui.QLabel(msg)
        layout.addWidget(label)
        label.setText("Please Wait")
        label.show()
        msg.show()
        QtGui.qApp.processEvents()

        self.mcafit.estimate()
        fitresult, self.fitData = self.mcafit.startfit(digest=1)

        self.peaksSpectrum()
        self.updateFigure()

        msg.close()

    def peaksSpectrum(self):
        fitresult = self.fitData
        config = self.mcafit.configure()
        groupsList = fitresult['groups']
        if not isinstance(groupsList, list): groupsList = [groupsList]

        nglobal = len(fitresult['parameters']) - len(groupsList)
        dict = self.fitData

        newparameters = fitresult['fittedpar'] * 1
        for i in range(nglobal, len(fitresult['parameters'])):
            newparameters[i] = 0.0
        for i in range(nglobal, len(fitresult['parameters'])):
            group = fitresult['parameters'][i]
            group = fitresult['parameters'][i]
            parameters = newparameters * 1
            parameters[i] = fitresult['fittedpar'][i]
            xmatrix = fitresult['xdata']
            ymatrix = self.mcafit.mcatheory(parameters, xmatrix)
            ymatrix.shape = [len(ymatrix), 1]
            label = 'y'+group
            if self.mcafit.STRIP:
                dict[label] = ymatrix + self.mcafit.zz
            else:
                dict[label] = ymatrix
            dict[label].shape = (len(dict[label]),)

            self.fitData[label] = dict[label] * 1.0

    def updateFigure(self):
        results = self.fitData

        xdata = results['energy'][:]

        self.spectrumAxes.clear()
        self.residualsAxes.clear()

        self.spectrumAxes.plot(xdata, results['ydata'], '.', label='data')
        self.spectrumAxes.plot(xdata, results['yfit'], linewidth=1.5, label='fit')
        self.spectrumAxes.plot(xdata, results['continuum'], linewidth=1.5, label='continuum')

        if self.fitconfig['fit']['sumflag']:
            continuum = results['pileup']+results['continuum']
            self.spectrumAxes.plot(xdata, continuum, linewidth=1.5, label='pileup')
        if results.has_key('ymatrix'):
            self.spectrumAxes.plot(xdata, results['ymatrix'], linewidth=1.5, label='matrix')

        for group in results['groups']:
            label = 'y'+group
            if results.has_key(label):
                self.spectrumAxes.plot(xdata, results[label], linewidth=1.5, label=group)

        self.spectrumAxes.xaxis.set_visible(False)
        self.spectrumAxes.set_ylabel('Counts')
        l = self.spectrumAxes.legend(loc=[1.05, -.85], numpoints=4)
        l.draw_frame(False)

        if self.useLogScale:
            res = numpy.log10(results['ydata']) - numpy.log10(results['yfit'])
            self.residualsAxes.plot(xdata, res, linewidth=1.5)
        else:
            res = results['ydata'] - results['yfit']
            self.residualsAxes.plot(xdata, res, linewidth=1.5)

        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')

        if self.useLogScale:
            self.spectrumAxes.set_yscale('log')

        self.draw()


class McaSpectrum(ui_mcaspectrum.Ui_McaSpectrum, QtGui.QWidget):

    """
    """

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.figure = McaSpectrumFigure(self)
        self.toolbar = plotwidgets.Toolbar(self.figure, self)
        self.gridlayout1.addWidget(self.toolbar, 0, 0, 1, 1)
        self.gridlayout1.addWidget(self.figure, 1, 0, 1, 1)

        self.connect(self.mcaLogscaleButton,
                     QtCore.SIGNAL("clicked(bool)"),
                     self.figure.enableLogscale)

    def __getattr__(self, attr):
        return getattr(self.figure, attr)

    def enableInteraction(self):
        self.mcaAutoscaleButton.setEnabled(True)
        self.mcaLogscaleButton.setEnabled(True)
