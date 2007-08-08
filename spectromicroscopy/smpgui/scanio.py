"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import codecs
import os
import sys
import tempfile
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyMca import ClassMcaTheory , ConcentrationsTool 
from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from configuresmp import ConfigureSmp
from mplwidgets import MplCanvas
from ui_scanio import Ui_XpMaster
from spectromicroscopy.smpcore import SpecRunner, getPymcaConfig,\
    getPymcaConfigFile, getSmpConfig

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = 2 # ??

VisualTypes = ["imshow", "line plot"]

Scans = ["select", "tseries", "mesh"]


class MyXP(Ui_XpMaster, QtGui.QMainWindow):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        self.DEBUG=DEBUG
        QtGui.QWidget.__init__(self, parent)
        self.parent=parent
        self.setupUi(self)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)
        self.config()
        self.setup = 0
        if parent:
            Bar = parent.Bar
        else:
            Bar = self.Bar
        Bar.addAction("PyMca Config file", self.set_config_file)
        Bar.addAction("Configure SMP", self.config_smp)
        for item in Scans:
            self.ScanBox.addItem(item)
        self.xprun = SpecRunner(self, DEBUG, self.__server,self.__port)
        self.xprun.exc("NPTS=0")
        self.buffer = tempfile.TemporaryFile('w+b')
        self.ElementSelect.setLineEdit(self.ElementText)
        QtCore.QObject.connect(self.ScanBox,
                               QtCore.SIGNAL("currentIndexChanged(int)"),
                               self.ScanControls)
        QtCore.QObject.connect(self.Run,
                               QtCore.SIGNAL("clicked()"),
                               self.run_scan)
        QtCore.QObject.connect(self.ElementSelect,
                               QtCore.SIGNAL("currentIndexChanged(int)"),
                               self.set_element)
        QtCore.QObject.connect(self.ScaleBox,
                               QtCore.SIGNAL("currentIndexChanged(int)"),
                               self.change_limits)#self.set_scale)
        QtCore.QObject.connect(self.MinValSpin,
                               QtCore.SIGNAL("editingFinished()"),
                               self.change_limits)
        QtCore.QObject.connect(self.MaxValSpin,
                               QtCore.SIGNAL("editingFinished()"),
                               self.change_limits)
        QtCore.QObject.connect(self.Estop,
                               QtCore.SIGNAL("clicked()"),
                               self.emergancy_stop)
        QtCore.QObject.connect(self.Mover,
                               QtCore.SIGNAL("clicked()"),
                               self.Move)
        QtCore.QObject.connect(self.AutoRanger,
                               QtCore.SIGNAL("clicked()"),
                               self.auto_set)
        for peak in self.__peaks:
            self.ElementSelect.addItem(peak)
        self.Spin_Slide_Motor = []
        self.Image_Element = ''

    def ScanControls(self):
        """establishes the Motor controls for selected scan"""
        if self.Spin_Slide_Motor:
            for object in self.Spin_Slide_Motor:
                object.hide()
        self.Spin_Slide_Motor = []
        if self.ScanBox.currentText()==Scans[1]:
            self.X = Spinner_Slide_Motor(self.MotorBox,self.xprun,"X",0)
            self.X.show()
            self.Spin_Slide_Motor.append(self.X)
        elif self.ScanBox.currentText() == Scans[2]:
            self.X = Spinner_Slide_Motor(self.MotorBox,self.xprun,"X",0)
            self.Y = Spinner_Slide_Motor(self.MotorBox,self.xprun,"Z",1)
            self.X.show()
            self.Y.show()
            self.Spin_Slide_Motor.append(self.X)
            self.Spin_Slide_Motor.append(self.Y)
    
    def Move(self):
        for i in len(self.Spin_Slide_Motor):
            self.Spin_Slide_Motor[i].Move()
        
    def emergancy_stop(self):
        self.xprun.EmergencyStop()
    
    def config_smp(self):
#        print self.__server,self.__port
        editor = ConfigureSmp(self)
        editor.exec_()
        smpConfig = getSmpConfig()
        self.__server = smpConfig['session']['server']
        self.__port = smpConfig['session']['port']
        print "***",self.__server,self.__port
    
    def set_config_file(self):
        try:
            fd = QtGui.QFileDialog(self)
            self.pymcaConfigFile = "%s"%fd.getOpenFileName()
            config = getPymcaConfig(self.pymcaConfigFile)
            self.__peaks = config["peaks"]
            self.ElementSelect.clear()
            for peak in self.__peaks:
                self.ElementSelect.addItem(peak)
        except:
            print "come on now"

    def config(self):
        smpConfig = getSmpConfig()
        try:
            self.__server = smpConfig['session']['server']
            self.__port = smpConfig['session']['port']
        except KeyError:
            self.config_smp()
        
        # TODO: break this into a new method
        self.pymcaConfigFile = getPymcaConfigFile()
        reader = getPymcaConfig()
        self.__peaks = []
        try:
            elements = reader["peaks"]
            for key in elements.keys():
                self.__peaks.append("%s %s"%(key,elements[key]))
        except KeyError:
            pass

    def set_element(self):
        self.Image_Element = "%s"%self.ElementSelect.currentText()
        self.change_limits()

    def auto_set(self):
        self.MinValSpin.setValue(0)
        self.MaxValSpin.setValue(0)
        self.change_limits()

    def change_limits(self):
        if self.setup != 0:
            parent = self.ImageFrame.widget(0)
            self.Range_Max = self.MaxValSpin.value()
            self.Range_Min = self.MinValSpin.value()
            scale = "%s"%self.ScaleBox.currentText()
            self.image = MyCanvas(self.ScanBox.currentText(),
                                  self.__images[self.Image_Element],
                                  self.x_index,
                                  self.y_index,
                                  self.Range_Min,
                                  self.Range_Max,
                                  parent,
                                  self.energy,
                                  self.__totaled,
                                  scale)
            self.image.setGeometry( QtCore.QRect(169, -1, 771, 900) )
            self.image.setMinimumSize(100, 100)
            self.image.setObjectName("Graph")
            self.image.show()

    def run_scan(self):
        """
        sets up scans
        Pauses scan if running
        resumes scan if paused
        
        Inorder to run a scan it:
       1) establishes required values
       2)connects MCA_DATAas spec variable
       3)begins a timmer to gather data
        """
        if "%s"%self.Run.text() == "Scan":
            self.setup = 0
            self.processed = []
            indexs=[[1,1,1],[1,1,1],[1,1,1]]
            for i in range(len(self.Spin_Slide_Motor)):
                for j in range(3):
                    indexs[i][j] = self.Spin_Slide_Motor[i].get_settings()[j]
            count_time = self.Counter.value()
            self.Range_Max = self.MaxValSpin.value()
            self.Range_Min = self.MinValSpin.value()
            if "%s"%self.ScanBox.currentText() == "tseries":
                self.max = indexs[0][2]*indexs[1][2]
                self.xprun.set_cmd("tseries %s %s"%(self.max,count_time))
                self.x_index = indexs[0][2]
                self.y_index = 1
            else:
                self.x_index = indexs[0][2]+1
                self.y_index = indexs[1][2]+1
                self.max = self.x_index*self.y_index
                x = self.X.get_motor_name()
                y = self.Y.get_motor_name()
                (xmin, xmax, xstep) = indexs[0]
                (ymin, ymax, ystep) = indexs[1]
                part_one = " %s %s %s %s"%(x,xmin,xmax,xstep)
                part_two = " %s %s %s %s"%(y,ymin, ymax, ystep)
                self.xprun.set_cmd("mesh"+part_one+part_two+" %s"%(count_time))
            self.xprun.exc("NPTS=0")
            self.processed = []
            self.theory = ClassMcaTheory.McaTheory(self.pymcaConfigFile)
            self.theory.enableOptimizedLinearFit()
            self.data = numpy.memmap(self.buffer.name,
                                     dtype=float,
                                     mode='w+',
                                     shape=(self.max,2048))
#            self.xprun.exc("MCA_DATA=0")
#            self.xprun.set_var('MCA_DATA',"Sync")
            self.__images = {}
            self.__sigmas = {}
            config = getPymcaConfig()
            gain = float(config["detector"]["gain"])
            offset = float(config["detector"]["zero"])
            self.__totaled = numpy.zeros(2048, numpy.float_)
            converstion = 0.01##TODO: read this value from config files
            self.energy = gain*numpy.arange(2048, dtype=numpy.float_)+offset
            self.timer = QtCore.QTimer(self)
            QtCore.QObject.connect(self.timer,
                                   QtCore.SIGNAL("timeout()"),
                                   self.data_collect)
            self.timer.start(20)
            self.xprun.run_cmd()
            self.Run.setText("Pause")
        elif "%s"%self.Run.text() == "Pause":
            print "Pause command"
            self.xprun.exc("")
            self.Run.setText("Resume")
        elif "%s"%self.Run.text() == "Resume":
            self.xprun.exc("scan_on")
            self.Run.setText("Pause")
    
    def data_collect(self):
        """gathers data from spec and processes it """
        max_index = self.max
        self.xprun.update()
        (value,index,actual) = self.xprun.get_values()
        if actual:
            typed = type(value[0])
#            print "<<%s>> %s"%(index,typed)
            if len(value[0])>1:
                self.data[index-1] = value[0][:,1]
            else:
                self.data[index-1] = value[0]
            self.theory.setdata(range(2048),self.data[index-1],None)
            self.theory.estimate()
            fitresult, result = self.theory.startfit(digest=1)
            self.processed.append((fitresult,result))
            self.__peaks = []
            self.__nrows = len(range(0,max_index))
            for group in result['groups']:
                self.__peaks.append(group)
                if not self.setup:
                    self.__images[group] = numpy.zeros((self.__nrows,1),
                                                       dtype=numpy.float_)
                    self.__sigmas[group] = numpy.zeros((self.__nrows,1),
                                                       dtype=numpy.float_)
            self.__images['chisq'] = numpy.zeros((self.__nrows,1),
                                                 dtype=numpy.float_) - 1.
            self.__images['chisq'][index-1, 0] = result['chisq']
            for peak in self.__peaks:
                if not self.setup:
                    self.__images[peak][index-1, 0] = result[peak]['fitarea']
                    self.__sigmas[peak][index-1,0] = result[peak]['sigmaarea']
                else:
                    self.__images[peak][index-1, 0] += result[peak]['fitarea']
                    self.__sigmas[peak][index-1,0] += result[peak]['sigmaarea']
            if self.Image_Element not in self.__peaks:
                self.Image_Element=self.__peaks[0]
#            print self.__images[self.Image_Element]
            scale = "%s"%self.ScaleBox.currentText()
            self.__totaled += self.data[index-1]
            parent = self.ImageFrame.widget(0)
            self.image = MyCanvas(self.ScanBox.currentText(),
                                  self.__images[self.Image_Element],
                                  self.x_index,
                                  self.y_index,
                                  self.Range_Min,
                                  self.Range_Max,
                                  parent,
                                  self.energy,
                                  self.__totaled,
                                  scale)
            self.image.setGeometry( QtCore.QRect(169, -1, 771, 800) )
            self.image.setMinimumSize(100,100)
            self.image.setObjectName("Graph")
            self.image.show()
            self.ToolBar = NavigationToolbar2QTAgg(self.image, parent)
            self.ToolBar.setGeometry( QtCore.QRect(169, 800, 771, 50) )
            self.ToolBar.show()
            self.ToolBar.draw()
            self.ToolBar.update()
            self.setup = 1
#            print self.Image_Element
        if index == self.max:
            self.timer.stop()
            self.setup = 2
#            self.xprun.exc("MCA_DATA=0")
            self.Run.setText("Scan")


class Spinner_Slide_Motor(QtGui.QFrame):

    def __init__(self, parent, xprun, axis, number):
        QtGui.QFrame.__init__(self, parent)
        self.xprun = xprun
        self.setGeometry( QtCore.QRect(60+91*number, 310, 91, 321) )
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        self.setObjectName("MotorWidget")

        self.Axis = QtGui.QLabel(self)
        self.Axis.setGeometry( QtCore.QRect(40, 10, 16, 16) )
        self.Axis.setObjectName("Axis")
        self.Axis.setText(axis)

        self.MotorName = QtGui.QLineEdit(self)
        self.MotorName.setGeometry( QtCore.QRect(20, 30, 51, 24) )
        self.MotorName.setObjectName("MotorName")
        if number == 0: self.MotorName.setText("samx")
        elif number == 1: self.MotorName.setText("samz")
        elif number == 2: self.MotorName.setText("samy")

        self.ScanMin = QtGui.QDoubleSpinBox(self)
        self.ScanMin.setGeometry( QtCore.QRect(10, 60, 62, 23) )
        self.ScanMin.setObjectName("ScanMin")

        self.ScanMax = QtGui.QDoubleSpinBox(self)
        self.ScanMax.setGeometry( QtCore.QRect(10, 90, 62, 23) )
        self.ScanMax.setObjectName("ScanMax")

        self.ScanSteps = QtGui.QSpinBox(self)
        self.ScanSteps.setGeometry( QtCore.QRect(20, 120, 51, 23) )
        self.ScanSteps.setObjectName("ScanSteps")

        self.MotorSlide = QtGui.QSlider(self)
        self.MotorSlide.setGeometry( QtCore.QRect(30, 160, 25, 121) )
        self.MotorSlide.setSingleStep(1)
        self.MotorSlide.setOrientation(QtCore.Qt.Vertical)
        self.MotorSlide.setTickPosition(QtGui.QSlider.TicksBelow)
        self.MotorSlide.setTickInterval(10)
        self.MotorSlide.setObjectName("MotorSlide")

        self.MotorSpin = QtGui.QDoubleSpinBox(self)
        self.MotorSpin.setGeometry( QtCore.QRect(10, 290, 62, 23) )
        self.MotorSpin.setDecimals(4)
        self.MotorSpin.setSingleStep(0.01)
        self.MotorSpin.setObjectName("MotorSpin")
        
        self.Spin = self.MotorSpin
        self.Slide = self.MotorSlide
        self.Min = self.ScanMin
        self.Max = self.ScanMax
        self.Step = self.ScanSteps
        self.motor_get()
        QtCore.QObject.connect(self.Slide,
                               QtCore.SIGNAL("sliderReleased()"),
                               self.slide)
        QtCore.QObject.connect(self.Spin,
                               QtCore.SIGNAL("editingFinished()"),
                               self.spin)
        QtCore.QObject.connect(self.MotorName,
                               QtCore.SIGNAL("editingFinished()"),
                               self.motor_get)
        self.get_params()
        self.setup()

    def motor_get(self):
        name = "%s"%self.MotorName.text()
        self.xprun.readmotors([name], "Async")
        self.Motor = self.xprun.get_motor(name)

    def get_params(self):
        # TODO: What is the point of this?
        self.values = []
        params = ['position', 'offset', 'sign', 'low_limit', 'high_limit', 'step_size']
        for param in params:
            try: 
                self.values.append(self.Motor.getParameter(param))
            except:
                self.values.append(0)

    def setup(self):
        values = self.values
        min = values[0]-1#values[2]*values[3]+values[1]
        max = values[0]#values[2]*values[4]+values[1]
        motor_step_size = values[5]
        self.Step.setRange(-100000,100000)
        self.Step.setValue(2)##1)
        self.Max.setRange(min, max)
        self.Min.setRange(min, max)
        self.Max.setValue(max)
        self.Min.setValue(min)
        self.Spin.setRange(min, max)
        self.Slide.setRange(min*motor_step_size, max*motor_step_size)
        self.Spin.setValue(self.values[0])
        self.Slide.setTickInterval(20*motor_step_size)
        self.spin()

    def slide(self):
        self.Spin.setValue(self.Slide.value()/self.values[5])

    def spin(self):
        self.Slide.setValue(self.Spin.value()*self.values[5])

    def Move(self):
        self.Motor.move(self.Spin.value())

    def get_settings(self):
        return (self.Min.value(), self.Max.value(), self.Step.value())

    def get_motor_name(self):
        return self.Motor.specName


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyXP()
    myapp.show()
    sys.exit(app.exec_())
