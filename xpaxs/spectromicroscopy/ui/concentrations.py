#/*##########################################################################
# Copyright (C) 2004-2008 European Synchrotron Radiation Facility
#
# This file is part of the PyMCA X-ray Fluorescence Toolkit developed at
# the ESRF by the Beamline Instrumentation Software Support (BLISS) group.
#
# This toolkit is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# PyMCA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PyMCA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# PyMCA follows the dual licensing model of Trolltech's Qt and Riverbank's PyQt
# and cannot be used as a free plugin for a non-free program.
#
# Please contact the ESRF industrial unit (industry@esrf.fr) if this license
# is a problem for you.
#############################################################################*/
__revision__ = "$Revision: 1.20 $"
import sys
if 'qt' not in sys.modules:
    try:
        import PyQt4.Qt as qt
    except:
        import qt
else:
    import qt

QTVERSION = qt.qVersion()

if QTVERSION < '3.0.0':
    import Myqttable as qttable
elif QTVERSION < '4.0.0':
    import qttable

if QTVERSION < '4.0.0':
    class QTable(qttable.QTable):
        def __init__(self, parent=None, name=""):
            qttable.QTable.__init__(self, parent, name)
            self.rowCount    = self.numRows
            self.columnCount = self.numCols
            self.setRowCount = self.setNumRows
            self.setColumnCount = self.setNumCols
            self.resizeColumnToContents = self.adjustColumn

else:
    QTable = qt.QTableWidget

from PyMca import ConcentrationsTool
from PyMca import Elements
import time
DEBUG=0
if DEBUG:
    print "ConcentrationsWidget is in debug mode"

class Concentrations(qt.QWidget):
    def __init__(self, parent=None, name="Concentrations", fl = 0):
        if QTVERSION < '4.0.0':
            qt.QWidget.__init__(self, parent, name, fl)
            self. setCaption(name)
        else:
            qt.QWidget.__init__(self, parent)
        self.build()
        self.setParameters    = self.concentrationsWidget.setParameters
        self.getParameters    = self.concentrationsWidget.getParameters
        self.__lastVar = None
        self.__lastKw = None


    def build(self):
        layout = qt.QVBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)
        self.concentrationsTool   = ConcentrationsTool.ConcentrationsTool()
        self.concentrationsWidget = ConcentrationsWidget(self)
        self.concentrationsTable  = ConcentrationsTable(self)
        layout.addWidget(self.concentrationsWidget)
        layout.addWidget(self.concentrationsTable)
        if QTVERSION < '4.0.0':
            self.connect(self.concentrationsWidget,
                        qt.PYSIGNAL('ConcentrationsWidgetSignal'),self.mySlot)
        else:
            layout.setStretchFactor(self.concentrationsWidget, 0)
            layout.setStretchFactor(self.concentrationsTable, 1)
            self.connect(self.concentrationsWidget,
                        qt.SIGNAL('ConcentrationsWidgetSignal'),self.mySlot)
        self.concentrationsTool.configure(self.concentrationsWidget.getParameters())

    def mySlot(self, ddict={}):
        if QTVERSION < '4.0.0':
            self.disconnect(self.concentrationsWidget,
                        qt.PYSIGNAL('ConcentrationsWidgetSignal'),self.mySlot)
            self.concentrationsTable.setFocus()
            qt.qApp.processEvents()
            self.connect(self.concentrationsWidget,
                        qt.PYSIGNAL('ConcentrationsWidgetSignal'),self.mySlot)
        else:
            self.disconnect(self.concentrationsWidget,
                        qt.SIGNAL('ConcentrationsWidgetSignal'),self.mySlot)
            self.concentrationsTable.setFocus()
            qt.qApp.processEvents()
            self.connect(self.concentrationsWidget,
                        qt.SIGNAL('ConcentrationsWidgetSignal'),self.mySlot)
        if ddict['event'] == 'updated':
            self.concentrationsTool.configure(ddict)
            if self.__lastKw is not None:
                try:
                    ddict['concentrations'] = self.processFitResult(*self.__lastVar, **self.__lastKw)
                except:
                    self.__lastKw = None
                    raise
            self.mySignal(ddict)

    def mySignal(self, ddict={}):
        if QTVERSION < '4.0.0':
            self.emit(qt.PYSIGNAL('ConcentrationsSignal'),(ddict,))
        else:
            self.emit(qt.SIGNAL('ConcentrationsSignal'), ddict)

    def processFitResult(self, *var, **kw):
        self.__lastVar= var
        self.__lastKw = kw
        if DEBUG:
            ddict = self.concentrationsTool.processFitResult(*var, **kw)
            self.concentrationsTable.fillFromResult(ddict)
            return ddict
        try:
            threadResult = self._submitThread(*var, **kw)
            if type(threadResult) == type((1,)):
                if len(threadResult):
                    if threadResult[0] == "Exception":
                        raise threadResult[1],threadResult[2]
            ddict = threadResult
            self.concentrationsTable.fillFromResult(ddict)
            return ddict
        except:
            self.__lastKw = None
            self.concentrationsTable.setRowCount(0)
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("%s" % sys.exc_info()[1])
            if QTVERSION < '4.0.0':
                msg.exec_loop()
            else:
                msg.exec_()


    def closeEvent(self, event):
        qt.QWidget.closeEvent(self, event)
        ddict={}
        ddict['event']= 'closed'
        if QTVERSION < '4.0.0':
            self.emit(qt.PYSIGNAL('closed'), (ddict,))
        else:
            self.emit(qt.SIGNAL('closed'), ddict)

    def _submitThread(self, *var, **kw):
        message = "Calculating concentrations"
        sthread = SimpleThread(self.concentrationsTool.processFitResult,
                                *var, **kw)

        sthread.start()
        if QTVERSION < '3.0.0':
            msg = qt.QDialog(self, "Please Wait", False,qt.Qt.WStyle_NoBorder)
        elif QTVERSION < '4.0.0':
            msg = qt.QDialog(self, "Please Wait", 1,qt.Qt.WStyle_NoBorder)
        else:
            msg = qt.QDialog(self, qt.Qt.FramelessWindowHint)
            msg.setModal(0)
            msg.setWindowTitle("Please Wait")
        layout = qt.QHBoxLayout(msg)
        layout.setMargin(0)
        layout.setSpacing(0)
        l1 = qt.QLabel(msg)
        l1.setFixedWidth(l1.fontMetrics().width('##'))
        l2 = qt.QLabel(msg)
        l2.setText("%s" % message)
        l3 = qt.QLabel(msg)
        l3.setFixedWidth(l3.fontMetrics().width('##'))
        layout.addWidget(l1)
        layout.addWidget(l2)
        layout.addWidget(l3)
        msg.show()
        qt.qApp.processEvents()
        t0 = time.time()
        i = 0
        ticks = ['-','\\', "|", "/","-","\\",'|','/']
        if QTVERSION < '4.0.0':
            while (sthread.running()):
                i = (i+1) % 8
                l1.setText(ticks[i])
                l3.setText(" "+ticks[i])
                qt.qApp.processEvents()
                time.sleep(1)
            msg.close(True)
        else:
            while (sthread.isRunning()):
                i = (i+1) % 8
                l1.setText(ticks[i])
                l3.setText(" "+ticks[i])
                qt.qApp.processEvents()
                time.sleep(1)
            msg.close()
        result = sthread._result
        del sthread
        if QTVERSION < '4.0.0':
            self.raiseW()
        else:
            self.raise_()
        return result

class SimpleThread(qt.QThread):
    def __init__(self, function, *var, **kw):
        if kw is None:kw={}
        qt.QThread.__init__(self)
        self._function = function
        self._var      = var
        self._kw       = kw
        self._result   = None

    def run(self):
        if DEBUG:
            self._result = self._function(*self._var, **self._kw )
        else:
            try:
                self._result = self._function(*self._var, **self._kw )
            except:
                self._result = ("Exception",) + sys.exc_info()

class ConcentrationsWidget(qt.QWidget):
    def __init__(self, parent=None, name="Concentrations", fl = 0):
        if QTVERSION < '4.0.0':
            qt.QWidget.__init__(self, parent, name, fl)
            self. setCaption(name)
        else:
            qt.QWidget.__init__(self, parent)

        self.build()
        ddict={}
        ddict['usematrix'] = 0
        ddict['useattenuators'] = 1
        ddict['flux'] = 1.0E10
        ddict['time'] = 1.0
        ddict['area'] = 30.0
        ddict['distance'] = 10.0
        ddict['reference'] = "Auto"
        ddict['mmolarflag'] = 0
        self.setParameters(ddict)

    def build(self):
        layout = qt.QVBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)
        if QTVERSION < '4.0.0':
            buttonGroup = qt.QVButtonGroup("Estimate concentrations", self)
            buttonGroup.setExclusive(True)
        else:
            buttonGroup = qt.QGroupBox(self)
            buttonGroup.layout = qt.QVBoxLayout(buttonGroup)
            buttonGroup.layout.setMargin(0)
            buttonGroup.layout.setSpacing(0)
        layout.addWidget(buttonGroup)
        self.fluxCheckBox = qt.QCheckBox(buttonGroup)
        self.fluxCheckBox.setText("From fundamental parameters")
        wf = qt.QWidget(buttonGroup)
        wf.layout = qt.QHBoxLayout(wf)
        wf.layout.setMargin(0)
        wf.layout.setSpacing(0)
        wf.layout.addWidget(HorizontalSpacer(wf))
        self.fundamentalWidget = FundamentalWidget(wf)
        wf.layout.addWidget(self.fundamentalWidget)
        wf.layout.addWidget(HorizontalSpacer(wf))
        self.matrixCheckBox = qt.QCheckBox(buttonGroup)
        self.matrixCheckBox.setText("From matrix composition")
        self.fluxCheckBox.setChecked(True)

        wm = qt.QWidget(buttonGroup)
        wm.layout = qt.QHBoxLayout(wm)
        wm.layout.setMargin(0)
        wm.layout.setSpacing(0)
        wm.layout.addWidget(HorizontalSpacer(wm))
        referenceLabel = qt.QLabel(wm)
        wm.layout.addWidget(referenceLabel)
        referenceLabel.setText("Matrix Reference Element:")
        #self.referenceCombo=MyQComboBox(wm)
        #self.referenceCombo=qt.QComboBox(wm)
        #self.referenceCombo.setEditable(True)
        #self.referenceCombo.insertItem('Auto')
        self.referenceLine = MyQLineEdit(wm)
        wm.layout.addWidget(self.referenceLine)
        self.referenceLine.setFixedWidth(self.referenceLine.fontMetrics().width('#######'))

        wm.layout.addWidget(HorizontalSpacer(wm))
        if QTVERSION < '4.0.0':
            self.connect(self.referenceLine,
                         qt.PYSIGNAL("MyQLineEditSignal"),
                         self._referenceLineSlot)

            self.connect(self.referenceLine,
                         qt.PYSIGNAL("MyQLineEditSignal"),
                         self._referenceLineSlot)
        else:
            self.connect(self.referenceLine,
                         qt.SIGNAL("MyQLineEditSignal"),
                         self._referenceLineSlot)

            self.connect(self.referenceLine,
                         qt.SIGNAL("MyQLineEditSignal"),
                         self._referenceLineSlot)
            buttonGroup.layout.addWidget(self.fluxCheckBox)
            buttonGroup.layout.addWidget(wf)
            buttonGroup.layout.addWidget(self.matrixCheckBox)
            buttonGroup.layout.addWidget(wm)



        #self.fundamentalWidget.setEnabled(False)
        self.attenuatorsCheckBox = qt.QCheckBox(self)
        self.attenuatorsCheckBox.setText("Consider attenuators in calculations")
        self.attenuatorsCheckBox.setDisabled(True)
        #Multilayer secondary excitation
        self.secondaryCheckBox = qt.QCheckBox(self)
        self.secondaryCheckBox.setText("Consider secondary excitation from deeper matrix layers (non intralayer nor above layers)")
        layout.addWidget(self.attenuatorsCheckBox)
        layout.addWidget( self.secondaryCheckBox)
        #mM checkbox
        self.mMolarCheckBox = qt.QCheckBox(self)
        self.mMolarCheckBox.setText("Elemental mM concentrations (assuming 1 l of solution is 1000 * matrix_density grams)")
        layout.addWidget( self.mMolarCheckBox)

        layout.addWidget(VerticalSpacer(self))
        buttonGroup.show()
        if QTVERSION < '4.0.0':
            self.connect(self.fluxCheckBox, qt.SIGNAL("clicked()"),self.checkBoxSlot)
            self.connect(self.matrixCheckBox, qt.SIGNAL("clicked()"),self.checkBoxSlot)
        else:
            self.connect(self.fluxCheckBox, qt.SIGNAL("clicked()"),self._fluxCheckBoxSlot)
            self.connect(self.matrixCheckBox, qt.SIGNAL("clicked()"),self.checkBoxSlot)
        self.connect(self.attenuatorsCheckBox, qt.SIGNAL("clicked()"),self.checkBoxSlot)
        self.connect(self.secondaryCheckBox, qt.SIGNAL("clicked()"),self.checkBoxSlot)
        self.connect(self.mMolarCheckBox, qt.SIGNAL("clicked()"),self.checkBoxSlot)

        if QTVERSION < '4.0.0':
            self.connect(self.fundamentalWidget.flux,
                         qt.PYSIGNAL('MyQLineEditSignal'), self._mySignal)
            self.connect(self.fundamentalWidget.area,
                         qt.PYSIGNAL('MyQLineEditSignal'), self._mySignal)
            self.connect(self.fundamentalWidget.time,
                         qt.PYSIGNAL('MyQLineEditSignal'), self._mySignal)
            self.connect(self.fundamentalWidget.distance,
                         qt.PYSIGNAL('MyQLineEditSignal'), self._mySignal)
        else:
            self.connect(self.fundamentalWidget.flux,
                         qt.SIGNAL('MyQLineEditSignal'), self._mySignal)
            self.connect(self.fundamentalWidget.area,
                         qt.SIGNAL('MyQLineEditSignal'), self._mySignal)
            self.connect(self.fundamentalWidget.time,
                         qt.SIGNAL('MyQLineEditSignal'), self._mySignal)
            self.connect(self.fundamentalWidget.distance,
                         qt.SIGNAL('MyQLineEditSignal'), self._mySignal)

    def _fluxCheckBoxSlot(self):
        if self.fluxCheckBox.isChecked():
            self.matrixCheckBox.setChecked(False)
        else:
            self.matrixCheckBox.setChecked(True)
        self.checkBoxSlot()

    def checkBoxSlot(self):
        if self.matrixCheckBox.isChecked():
            self.fundamentalWidget.setInputDisabled(True)
            self.referenceLine.setEnabled(True)
            if QTVERSION > '4.0.0':
                self.fluxCheckBox.setChecked(False)
        else:
            self.fundamentalWidget.setInputDisabled(False)
            self.referenceLine.setEnabled(False)
            if QTVERSION > '4.0.0':
                self.fluxCheckBox.setChecked(True)
        self._mySignal()

    def _referenceLineSlot(self, ddict):
        if ddict['event'] == "returnPressed":
            current = str(self.referenceLine.text())
            current = current.replace(' ','')
            if (current == '') or (current.upper()=='AUTO'):
                pass
            elif len(current) == 2:
                current = current.upper()[0] + current.lower()[1]
            elif len(current) == 1:
                current = current.upper()[0]
            else:
                msg=qt.QMessageBox(self.referenceLine)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Invalid Element %s" % current)
                if QTVERSION < '4.0.0':
                    msg.exec_loop()
                else:
                    msg.exec_()
                self.referenceLine.setFocus()
                return
            if (current == '') or (current.upper()=='AUTO'):
                self._mySignal()
            elif not Elements.isValidFormula(current):
                msg=qt.QMessageBox(self.referenceLine)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Invalid Element %s" % current)
                if QTVERSION < '4.0.0':
                    msg.exec_loop()
                else:
                    msg.exec_()

                self.referenceLine.setText('Auto')
                self.referenceLine.setFocus()
            else:
                self.referenceLine.setText(current)
                self._mySignal()

    def _mySignal(self,dummy=None):
        ddict = self.getParameters()
        ddict['event']='updated'
        if QTVERSION < '4.0.0':
            self.emit(qt.PYSIGNAL('ConcentrationsWidgetSignal'),(ddict,))
        else:
            self.emit(qt.SIGNAL('ConcentrationsWidgetSignal'), ddict)

    def getParameters(self):
        ddict={}
        if self.matrixCheckBox.isChecked():
            ddict['usematrix']      = 1
        else:
            ddict['usematrix']      = 0

        if self.attenuatorsCheckBox.isChecked():
            ddict['useattenuators'] = 1
        else:
            ddict['useattenuators'] = 0
        if self.secondaryCheckBox.isChecked():
            ddict['usemultilayersecondary'] = 1
        else:
            ddict['usemultilayersecondary'] = 0
        if self.mMolarCheckBox.isChecked():
            ddict['mmolarflag'] = 1
        else:
            ddict['mmolarflag'] = 0
        ddict['flux'] = float(str(self.fundamentalWidget.flux.text()))
        ddict['time'] = float(str(self.fundamentalWidget.time.text()))
        ddict['area'] = float(str(self.fundamentalWidget.area.text()))
        ddict['distance'] = float(str(self.fundamentalWidget.distance.text()))
        #ddict['reference'] = str(self.referenceCombo.currentText())
        ddict['reference'] = str(self.referenceLine.text())
        return ddict

    def setParameters(self, ddict, signal = None):
        if signal is None:signal=True
        if ddict.has_key('usemultilayersecondary'):
            if ddict['usemultilayersecondary']:
                self.secondaryCheckBox.setChecked(True)
            else:
                self.secondaryCheckBox.setChecked(False)
        else:
            self.secondaryCheckBox.setChecked(False)

        if ddict.has_key('mmolarflag'):
            if ddict['mmolarflag']:
                self.mMolarCheckBox.setChecked(True)
            else:
                self.mMolarCheckBox.setChecked(False)
        else:
            self.mMolarCheckBox.setChecked(False)

        if ddict['usematrix']:
            self.fluxCheckBox.setChecked(False)
            self.matrixCheckBox.setChecked(True)
        else:
            self.fluxCheckBox.setChecked(True)
            self.matrixCheckBox.setChecked(False)
        ddict['useattenuators'] = 1
        if ddict['useattenuators']:
            self.attenuatorsCheckBox.setChecked(True)
        else:
            self.attenuatorsCheckBox.setChecked(False)
        if ddict.has_key('reference'):
            #self.referenceCombo.setCurrentText(qt.QString(ddict['reference']))
            self.referenceLine.setText(qt.QString(ddict['reference']))
        else:
            #self.referenceCombo.setCurrentText(qt.QString("Auto"))
            self.referenceLine.setText(qt.QString("Auto"))

        self.fundamentalWidget.flux.setText("%.6g" % ddict['flux'])
        self.fundamentalWidget.area.setText("%.6g" % ddict['area'])
        self.fundamentalWidget.distance.setText("%.6g" % ddict['distance'])
        self.fundamentalWidget.time.setText("%.6g" % ddict['time'])
        if self.matrixCheckBox.isChecked():
            self.fundamentalWidget.setInputDisabled(True)
            self.referenceLine.setEnabled(True)
        else:
            self.fundamentalWidget.setInputDisabled(False)
            self.referenceLine.setEnabled(False)
        if signal:self._mySignal()

    def setReferenceOptions(self, options=None):
        if options is None:options=['Auto']
        old = self.referenceCombo.currentText()
        if 'Auto' not in options:
            options = ['Auto'] + options
        self.referenceCombo.clear()
        self.referenceCombo.insertStrList(options)
        if old in options:
            self.referenceCombo.setCurrentText(old)
        else:
            self.referenceCombo.setCurrentText('Auto')

class FundamentalWidget(qt.QWidget):
    def __init__(self, parent = None, name = ""):
        qt.QWidget.__init__(self,parent)
        self.build()

    def build(self):
        layout = qt.QHBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)

        #column 0
        c0 = qt.QWidget(self)
        c0.layout = qt.QVBoxLayout(c0)
        c0.layout.setMargin(0)
        c0.layout.setSpacing(0)

#        c0l1 = qt.QLabel(c0)
        #c0l1.setText("Integrated Flux")

        c0l2 = qt.QLabel(c0)
        c0l2.setText("Flux (photons/s)")

#        c0l3 = qt.QLabel(c0)
        #c0l3.setText("Detector Solid Angle")

        c0l4 = qt.QLabel(c0)
        c0l4.setText("Active Area (mm2)")

#        c0l5 = qt.QLabel(c0)
#        c0l5.setText(" ")
#        c0.layout.addWidget(c0l1)
        c0.layout.addWidget(c0l2)
#        c0.layout.addWidget(c0l3)
        c0.layout.addWidget(c0l4)
#        c0.layout.addWidget(c0l5)


        #column 1
        c1 = qt.QWidget(self)
        c1.layout = qt.QVBoxLayout(c1)
        c1.layout.setMargin(6)
        c1.layout.setSpacing(0)

#        c1l1 = qt.QLabel(c1)
#        c1l1.setText("")

        self.flux = MyQLineEdit(c1)
        self.flux.setValidator(qt.QDoubleValidator(self.flux))

#        c1l2 = qt.QLabel(c1)
#        c1l2.setText("")

        self.area = MyQLineEdit(c1)
        self.area.setValidator(qt.QDoubleValidator(self.area))
#        c1l5 = qt.QLabel(c1)
#        c1l5.setText(" ")

#        c1.layout.addWidget(c1l1)
        c1.layout.addWidget(self.flux)
#        c1.layout.addWidget(c1l2)
        c1.layout.addWidget(self.area)
#        c1.layout.addWidget(c1l5)


        #column 2
        c2 = qt.QWidget(self)
        c2.layout = qt.QVBoxLayout(c2)
        c2.layout.setMargin(6)
        c2.layout.setSpacing(0)

#        c2l1 = qt.QLabel(c2)
#        c2l1.setText("")

        c2l2 = qt.QLabel(c2)
        c2l2.setText("x time(seconds)")

#        c2l3 = qt.QLabel(c2)
#        c2l3.setText("")

        c2l4 = qt.QLabel(c2)
        c2l4.setText("distance (mm)")
#        c2l5 = qt.QLabel(c2)
#        c2l5.setText(" ")

#        c2.layout.addWidget(c2l1)
        c2.layout.addWidget(c2l2)
#        c2.layout.addWidget(c2l3)
        c2.layout.addWidget(c2l4)
#        c2.layout.addWidget(c2l5)

        #column 3
        c3 = qt.QWidget(self)
        c3.layout = qt.QVBoxLayout(c3)
        c3.layout.setMargin(6)
        c3.layout.setSpacing(0)

#        c3l1 = qt.QLabel(c3)
#        c3l1.setText("")

        self.time = MyQLineEdit(c3)
        self.time.setValidator(qt.QDoubleValidator(self.time))

#        c3l2 = qt.QLabel(c3)
#        c3l2.setText("")

        self.distance = MyQLineEdit(c3)
        self.distance.setValidator(qt.QDoubleValidator(self.distance))
#        c3l5 = qt.QLabel(c3)
#        c3l5.setText(" ")

#        c3.layout.addWidget(c3l1)
        c3.layout.addWidget(self.time)
#        c3.layout.addWidget(c3l2)
        c3.layout.addWidget(self.distance)
#        c3.layout.addWidget(c3l5)


        #column 4
        """
        c4 = qt.QWidget(self)
        c4.layout = qt.QVBoxLayout(c4)

        c4l1 = qt.QLabel(c4)
        c4l1.setText("")

        c4l2 = qt.QLabel(c4)
        c4l2.setText("seconds")

        c4l3 = qt.QLabel(c4)
        c4l3.setText("")

        c4l4 = qt.QLabel(c4)
        c4l4.setText("distance")
        """
        layout.addWidget(c0)
        layout.addWidget(c1)
        layout.addWidget(c2)
        layout.addWidget(c3)

    def setInputDisabled(self,a=None):
        if a is None:a=True
        if a:
            self.flux.setEnabled(False)
            self.time.setEnabled(False)
            self.area.setEnabled(False)
            self.distance.setEnabled(False)
        else:
            self.flux.setEnabled(True)
            self.time.setEnabled(True)
            self.area.setEnabled(True)
            self.distance.setEnabled(True)

class ConcentrationsTable(QTable):
    def __init__(self, parent=None, **kw):
        QTable.__init__(self, parent)

        if kw.has_key('labels'):
            self.labels=[]
            for label in kw['labels']:
                self.labels.append(label)
        else:
            #self.labels=['Element','Group','Fit Area','Expected Area','Mass fraction']
            self.labels=['Element','Group','Fit Area','Mass fraction']
        if QTVERSION < '4.0.0':
            i=0
            self.setColumnCount(len(self.labels))
            self.setRowCount(1)
            for label in self.labels:
                qt.QHeader.setLabel(self.horizontalHeader(),i,label)
                self.adjustColumn(i)
                i=i+1
        else:
            self.setColumnCount(len(self.labels))
            self.setRowCount(1)
            for i in range(len(self.labels)):
                item = self.horizontalHeaderItem(i)
                if item is None:
                    item = qt.QTableWidgetItem(self.labels[i],qt.QTableWidgetItem.Type)
                self.setHorizontalHeaderItem(i,item)
                self.resizeColumnToContents(i)

    def fillFromResult(self,result):
        if result.has_key('mmolar'):
            mmolarflag = True
        else:
            mmolarflag = False
        groupsList = result['groups']
        nrows = len(groupsList)
        if nrows != self.rowCount():
            self.setRowCount(nrows)
        if mmolarflag:
            self.labels = ['Element','Group','Fit Area','Sigma Area', 'mM concentration']
        else:
            self.labels = ['Element','Group','Fit Area','Sigma Area', 'Mass fraction']
        if result.has_key('layerlist'):
            for label in result['layerlist']:
                self.labels += [label]
        self.setColumnCount(len(self.labels))
        if QTVERSION < '4.0.0':
            i=0
            for label in self.labels:
                qt.QHeader.setLabel(self.horizontalHeader(),i,label)
                #self.adjustColumn(i)
                i=i+1
        else:
            for i in range(len(self.labels)):
                item = self.horizontalHeaderItem(i)
                if item is None:
                    item = qt.QTableWidgetItem(self.labels[i],
                                               qt.QTableWidgetItem.Type)
                item.setText(self.labels[i])
                self.setHorizontalHeaderItem(i,item )

        line = 0
        for group in groupsList:
            element, group0 = group.split()
            transitions = group0 + " xrays"
            fitarea    = qt.QString("%.6e" % (result['fitarea'][group]))
            sigmaarea  = qt.QString("%.2e" % (result['sigmaarea'][group]))
            area       = qt.QString("%.6e" % (result['area'][group]))
            if result['mass fraction'][group] < 0.0:
                fraction   = qt.QString("Unknown")
            else:
                if mmolarflag:
                    fraction   = qt.QString("%.4g" % (result['mmolar'][group]))
                else:
                    fraction   = qt.QString("%.4g" % (result['mass fraction'][group]))
            if line % 2:
                color = qt.QColor(255,250,205)
            else:
                color = qt.QColor('white')
            if 'Expected Area' in self.labels:
                fields = [element,group0,fitarea,sigmaarea,area,fraction]
            else:
                fields = [element,group0,fitarea,sigmaarea,fraction]
            if result.has_key('layerlist'):
                for layer in result['layerlist']:
                    #fitarea    = qt.QString("%.6e" % (result[layer]['fitarea'][group]))
                    #area       = qt.QString("%.6e" % (result[layer]['area'][group]))
                    if result[layer]['mass fraction'][group] < 0.0:
                        fraction   = qt.QString("Unknown")
                    else:
                        if mmolarflag:
                            fraction   = qt.QString("%.4g" % (result[layer]['mmolar'][group]))
                        else:
                            fraction   = qt.QString("%.4g" % (result[layer]['mass fraction'][group]))
                    fields += [fraction]
            col = 0
            for field in fields:
                if QTVERSION < '4.0.0':
                    key=ColorQTableItem(self,qttable.QTableItem.Never,
                                        field,color=color)
                    self.setItem(line, col,key)
                else:
                    item = self.item(line, col)
                    if item is None:
                        item = qt.QTableWidgetItem(field,
                                                   qt.QTableWidgetItem.Type)
                    else:
                        item.setText(field)
                    item.setBackgroundColor(color)
                    item.setFlags(qt.Qt.ItemIsSelectable|
                                  qt.Qt.ItemIsEnabled)
                    self.setItem(line, col, item)
                col=col+1
            line +=1

        for i in range(self.columnCount()):
            if (i > 1) and (i < 5):
                self.resizeColumnToContents(i)


    def getHtmlText(self):
        lemon=("#%x%x%x" % (255,250,205)).upper()
        white = "#FFFFFF"
        if QTVERSION < '3.0.0':
            hcolor = ("#%x%x%x" % (230,240,249)).upper()
        elif QTVERSION < '4.0.0':
            hb = self.horizontalHeader().paletteBackgroundColor()
            hcolor = ("#%x%x%x" % (hb.red(),hb.green(),hb.blue())).upper()
        else:
            hcolor = ("#%x%x%x" % (230,240,249)).upper()
        text=""
        text+=("<nobr>")
        text+=( "<table>")
        text+=( "<tr>")
        for l in range(self.columnCount()):
            text+=('<td align="left" bgcolor="%s"><b>' % hcolor)
            if QTVERSION < '4.0.0':
                text+=(str(self.horizontalHeader().label(l)))
            else:
                item = self.horizontalHeaderItem(l)
                text+=str(item.text())
            text+=("</b></td>")
        text+=("</tr>")
        #text+=( str(qt.QString("</br>"))
        for r in range(self.rowCount()):
            text+=("<tr>")
            if r % 2:
                color = white
                b="<b>"
            else:
                b="<b>"
                color = lemon
            for c in range(self.columnCount()):
                if QTVERSION < '4.0.0':
                    moretext = str(self.text(r,c))
                else:
                    moretext = ""
                    item = self.item(r, c)
                    if item is not None:
                        moretext = str(item.text())
                if len(moretext):
                    finalcolor = color
                else:
                    finalcolor = white
                if c<2:
                    text+=('<td align="left" bgcolor="%s">%s' % (finalcolor,b))
                else:
                    text+=('<td align="right" bgcolor="%s">%s' % (finalcolor,b))
                text+= moretext
                if len(b):
                    text+=("</td>")
                else:
                    text+=("</b></td>")
            if QTVERSION < '4.0.0':
                moretext = str(self.text(r,0))
            else:
                moretext = ""
                item = self.item(r, 0)
                if item is not None:
                    moretext = str(item.text())
            if len(moretext):
                text+=("</b>")
            text+=("</tr>")
            #text+=( str(qt.QString("<br>"))
            text+=("\n")
        text+=("</table>")
        text+=("</nobr>")
        return text



if QTVERSION < '4.0.0':
    class ColorQTableItem(qttable.QTableItem):
             def __init__(self, table, edittype, text,color=qt.Qt.white,bold=0):
                     qttable.QTableItem.__init__(self, table, edittype, text)
                     self.color = color
                     self.bold  = bold
             def paint(self, painter, colorgroup, rect, selected):
                painter.font().setBold(self.bold)
                cg = qt.QColorGroup(colorgroup)
                cg.setColor(qt.QColorGroup.Base, self.color)
                qttable.QTableItem.paint(self,painter, cg, rect, selected)
                painter.font().setBold(0)

class MyQLineEdit(qt.QLineEdit):
    def __init__(self,parent=None,name=None):
        qt.QLineEdit.__init__(self,parent)
        qt.QObject.connect(self,qt.SIGNAL("returnPressed()"),self._mySignal)

    def focusInEvent(self,event):
        self.setPaletteBackgroundColor(qt.QColor('yellow'))

    def focusOutEvent(self,event):
        self.setPaletteBackgroundColor(qt.QColor('white'))
        self.emit(qt.SIGNAL("returnPressed()"),())

    def setPaletteBackgroundColor(self, qcolor):
        if QTVERSION < '3.0.0':
            palette = self.palette()
            palette.setColor(qt.QColorGroup.Base,qcolor)
            self.setPalette(palette)
            text = self.text()
            self.setText(text)
        else:
            if QTVERSION < '4.0.0':
                qt.QLineEdit.setPaletteBackgroundColor(self,qcolor)

    def _mySignal(self):
        self.setPaletteBackgroundColor(qt.QColor('white'))
        ddict={}
        ddict['event'] = "returnPressed"
        if QTVERSION < '4.0.0':
            self.emit(qt.PYSIGNAL("MyQLineEditSignal"), (ddict,))
        else:
            self.emit(qt.SIGNAL("MyQLineEditSignal"), ddict)

class HorizontalSpacer(qt.QWidget):
    def __init__(self, *args):
        qt.QWidget.__init__(self, *args)

        self.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed))


class VerticalSpacer(qt.QWidget):
    def __init__(self, *args):
        qt.QWidget.__init__(self, *args)
        self.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Fixed,qt.QSizePolicy.Expanding))

class MyQComboBox(qt.QComboBox):
    def __init__(self,parent = None,name = None,fl = 0):
        qt.QComboBox.__init__(self,parent)
        self.setEditable(True)
        self._lineEdit = MyQLineEdit()
        self.setLineEdit(self._lineEdit)
        if QTVERSION < '4.0.0':
            self.connect(self._lineEdit,
                         qt.PYSIGNAL("MyQLineEditSignal"),self._mySlot)
        else:
            self.connect(self._lineEdit,
                         qt.SIGNAL("MyQLineEditSignal"),self._mySlot)

    def _mySlot(self, ddict):
        if ddict['event'] == "returnPressed":
            current = str(self.currentText())
            current = current.replace(' ','')
            if (current == '') or (current.upper()=='AUTO'):
                pass
            elif len(current) == 2:
                current = current.upper()[0] + current.lower()[1]
            elif len(current) == 1:
                current = current.upper()[0]
            else:
                msg=qt.QMessageBox(self._lineEdit)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Invalid Element %s" % current)
                if QTVERSION < '4.0.0':
                    msg.exec_loop()
                else:
                    msg.exec_()
                self._lineEdit.setFocus()
            if not Elements.isValidFormula(current):
                msg=qt.QMessageBox(self._lineEdit)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Invalid Element %s" % current)
                if QTVERSION < '4.0.0':
                    msg.exec_loop()
                else:
                    msg.exec_()
                self._lineEdit.setFocus()
            else:
                self.setCurrentText(current)


if __name__ == "__main__":
    import sys
    import ConfigDict
    import getopt
    import ConcentrationsTool
    if len(sys.argv) > 1:
        options = ''
        longoptions = ['flux=','time=','area=','distance=','attenuators=','usematrix=']

        #tool = ConcentrationsTool.ConcentrationsTool()
        opts, args = getopt.getopt(
                        sys.argv[1:],
                        options,
                        longoptions)
        #config = tool.configure()
        #tool.configure(config)
        app = qt.QApplication([])
        qt.QObject.connect(app, qt.SIGNAL("lastWindowClosed()"),app,qt.SLOT("quit()"))
        demo= Concentrations()
        config = demo.getParameters()
        for opt,arg in opts:
            if opt in ('--flux'):
                config['flux'] = float(arg)
            elif opt in ('--area'):
                config['area'] = float(arg)
            elif opt in ('--time'):
                config['time'] = float(arg)
            elif opt in ('--distance'):
                config['distance'] = float(arg)
            elif opt in ('--attenuators'):
                config['useattenuators'] = int(float(arg))
            elif opt in ('--usematrix'):
                config['usematrix'] = int(float(arg))
        demo.setParameters(config)
        filelist = args
        for file in filelist:
            d = ConfigDict.ConfigDict()
            d.read(file)
            demo.processFitResult(fitresult=d,elementsfrommatrix=False)
        demo.show()
        if QTVERSION < '4.0.0':
            app.setMainWidget(demo)
            app.exec_loop()
        else:
            app.exec_()

    else:
        print "Usage:"
        print "ConcentrationsWidget.py [--flux=xxxx --area=xxxx] fitresultfile"

#python ConcentrationsWidget.py --flux=xxxx
