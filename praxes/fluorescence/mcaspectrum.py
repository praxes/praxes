"""
"""

from __future__ import absolute_import

import copy
#import logging

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg\
    as MplToolbar
import numpy as np
from PyMca5.PyMcaPhysics.xrf.ClassMcaTheory import McaTheory
from PyQt4 import QtCore, QtGui

from .plotwidgets import QtMplCanvas
from .ui import ui_mcaspectrum


#logger = logging.getLogger(__file__)


class SpectrumAnalysisThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(SpectrumAnalysisThread, self).__init__(parent)

        self.mcafit = McaTheory()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

    def run(self):
        self.exec_()


class McaSpectrumFigure(QtMplCanvas):

    def __init__(self, parent=None):
        super(McaSpectrumFigure, self).__init__(parent)

        self.useLogScale = False

        self.spectrumAxes = self.figure.add_axes([.1, .4, .7, .55])
        self.spectrumAxes.xaxis.set_visible(False)
        self.spectrumAxes.set_ylabel('Counts')

        self.residualsAxes = self.figure.add_axes([.1, .125, .7, .225],
                                                  sharex=self.spectrumAxes)
        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')

    def updateFigure(self, results):
        xdata = results['energy'][:]

        self.spectrumAxes.clear()
        self.residualsAxes.clear()

        self.spectrumAxes.plot(xdata, results['ydata'], label='data')
        self.spectrumAxes.plot(xdata, results['yfit'], linewidth=1.5,
                               label='fit')
        self.spectrumAxes.plot(xdata, results['continuum'], linewidth=1.5,
                               label='continuum')

        try:
            continuum = results['pileup']+results['continuum']
            self.spectrumAxes.plot(xdata, continuum, linewidth=1.5,
                                   label='pileup')
        except KeyError:
            pass
        if results.has_key('ymatrix'):
            self.spectrumAxes.plot(xdata, results['ymatrix'], linewidth=1.5,
                                   label='matrix')

        for group in results['groups']:
            label = 'y'+group
            if results.has_key(label):
                self.spectrumAxes.plot(xdata, results[label], linewidth=1.5,
                                       label=group)

        self.spectrumAxes.xaxis.set_visible(False)
        self.spectrumAxes.set_ylabel('Counts')
        l = self.spectrumAxes.legend(loc=[1.05, -.7], numpoints=4)
        l.draw_frame(False)

        if self.useLogScale:
            res = np.log10(results['ydata']) - np.log10(results['yfit'])
            res[np.isinf(res)] = np.nan
            self.residualsAxes.plot(xdata, res, linewidth=1.5)
        else:
            res = results['ydata'] - results['yfit']
            self.residualsAxes.plot(xdata, res, linewidth=1.5)

        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')

        if self.useLogScale:
            self.spectrumAxes.set_yscale('log')
            ylim = list(self.spectrumAxes.get_ylim())
            if ylim[0] < 0.001:
                ylim[0] = 0.001
                self.spectrumAxes.set_ylim(ylim)

        self.draw()


class McaSpectrum(ui_mcaspectrum.Ui_McaSpectrum, QtGui.QWidget):

    """
    """

    def __init__(self, concentrationsWidget=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.concentrationsWidget = concentrationsWidget

        self.mcafit = McaTheory()
#        self.mcafit.enableOptimizedLinearFit()
        self.fitData = None

        self.figure = McaSpectrumFigure(self)
        self.toolbar = MplToolbar(self.figure, self)
        self.gridlayout1.addWidget(self.toolbar, 0, 0, 1, 1)
        self.gridlayout1.addWidget(self.figure, 1, 0, 1, 1)

        self.mcaLogscaleButton.clicked.connect(self.enableLogscale)

    def __getattr__(self, attr):
        return getattr(self.figure, attr)

    def configure(self, configDict):
        newDict = self.mcafit.configure(configDict)
        try:
            self.concentrationsWidget.setParameters(newDict['concentrations'],
                                                    signal=False)
        except KeyError:
            pass
        return newDict

    def enableInteraction(self):
        self.mcaAutoscaleButton.setEnabled(True)
        self.mcaLogscaleButton.setEnabled(True)

    def enableLogscale(self, val):
        self.figure.useLogScale = val
        self.updateFigure()

    def fit(self):
        if self.mcafit.config['peaks'] == {}:
            msg = QtGui.QMessageBox(self)
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("No peaks defined.\nPlease configure peaks")
            msg.exec_()
            return

        self.mcafit.estimate()
        fitresult, fitData = self.mcafit.startfit(digest=1)
        self.fitData = copy.deepcopy(fitData)
        self.peaksSpectrum()
        self.updateFigure()

        config = self.mcafit.config
        if 'concentrations' in self.mcafit.config:
            fitresult = {'fitresult': fitresult,
                         'result': self.fitData}
            tool = self.concentrationsWidget
            toolconfig = tool.getParameters()
            concDict = config['concentrations']
            tool.setParameters(concDict, signal=False)
            try:
                dict = tool.processFitResult(config=concDict,
                                             fitresult=fitresult,
                                             elementsfrommatrix=False,
                                             fluorates=self.mcafit._fluoRates)
            except:
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Error processing fit result: %s" % (sys.exc_info()[1]))
                msg.exec_()

        return copy.deepcopy(fitresult)

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

    def setData(self, *args, **kwargs):
        self.mcafit.setData(*args, **kwargs)

    def updateFigure(self):
        self.figure.updateFigure(self.fitData)
