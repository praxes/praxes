#!/usr/bin/env python
import sys, os, codecs
from os.path import isfile
os.system("pyuic4 Xp.ui>Xp.py")
DEBUG=2
GRAPH=1

#GUI
from PyQt4 import QtCore, QtGui
from Xp import Ui_XPrun
from SpecRunner import SpecRunner
#Number Crunching
import numpy
import numpy.oldnumeric as Numeric
from matplotlib.numerix import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pylab import *
from tempfile import TemporaryFile, NamedTemporaryFile
from PyMca import ClassMcaTheory , ConcentrationsTool #,McaAdvancedFitBatch


class MyXP(Ui_XPrun,QtGui.QMainWindow):
    """Establishes a Experimenbt controls"""
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.ScanBox.addItem("tseries")
        self.ScanBox.addItem("mesh")
        self.xprun=SpecRunner(self,DEBUG,"f3.chess.cornell.edu","xrf")
        self.buffer=TemporaryFile( 'w+b')
        self.Motor_Connect()
        if DEBUG!=1:
            QtCore.QObject.connect(self.Mv,
                                   QtCore.SIGNAL("clicked()"),self.Move)
            QtCore.QObject.connect(self.Xname, 
                                    QtCore.SIGNAL("editingFinished()"), self.Motor_Connect)
            QtCore.QObject.connect(self.Yname, 
                                    QtCore.SIGNAL("editingFinished()"), self.Motor_Connect)
            QtCore.QObject.connect(self.Zname, 
                                    QtCore.SIGNAL("editingFinished()"), self.Motor_Connect)
            QtCore.QObject.connect(self.Run,QtCore.SIGNAL("clicked()"),self.run_scan)
        
    def Motor_Connect(self):
        names =["%s"%self.Xname.text(),"%s"%self.Yname.text(),"%s"%self.Zname.text()]
        self.xprun.readmotors(names,"Async")
        MotorX=self.xprun.get_motor("%s"%self.Xname.text())
        MotorY=self.xprun.get_motor("%s"%self.Yname.text())
        MotorZ=self.xprun.get_motor("%s"%self.Zname.text())
        self.X=Spinner_Slide_Motor(self.Xslide,self.SpinX,MotorX,self.Xmin,self.Xmax,self.Xstep)
        self.Y=Spinner_Slide_Motor(self.Yslide,self.SpinY,MotorY,self.Ymin,self.Ymax,self.Ystep)
        self.Z=Spinner_Slide_Motor(self.Zslide,self.SpinZ,MotorZ,self.Zmin,self.Zmax,self.Zstep)


    def Move(self):
        self.X.Move()
        self.Y.Move()
        self.Z.Move()
    
    def run_scan(self):
        self.processed=[]
        max_index_x=self.X.get_settings()[2]
        max_index_y=self.Y.get_settings()[2]
        max_index =max_index_x*max_index_y
        count_time=self.Counter.value()
        file =os.path.join("/home/jeff/src/smp/spectromicroscopy","17KeV.cfg")
        self.theory=ClassMcaTheory.McaTheory(file)
        self.theory.enableOptimizedLinearFit()
        self.concentrate=ConcentrationsTool.ConcentrationsTool(file)
        self.data=numpy.memmap(self.buffer.name,dtype=float,mode='w+',shape=(max_index,2048))
        self.xprun.set_var('MCA_DATA',"Sync")
        if "%s"%self.ScanBox.currentText()=="tseries":
            self.xprun.set_cmd("tseries %s %s"%(max_index,count_time))
        else:
            x = self.X.get_motor_name()
            y = self.Y.get_motor_name()
            (xmin, xmax, xstep)=self.X.get_settings()
            (ymin, ymax, ystep)=self.Y.get_settings()
            self.xprun.set_cmd("mesh motor%s %s %s %s %s %s %s"\
                        %(x,xmin,xmax,xstep,y,ymin,ymax,ystep,count_time))
        self.xprun.run_cmd()
        setup=0
        self.Qimages={}
        while not self.xprun.get_cmd_reply():
            self.xprun.update()
            (value,index,actual)=self.xprun.get_values()
            if actual:
                typed=type(value[0])
                print "<<%s>> %s"%(index,typed)
                for i in range(len(value[0])):
                    if len(value[0])>1:
                        self.data[index-1,i]=value[0][i][1]
                    else:
                        self.data[index-1,i]=value[0][i]
                self.theory.setdata(range(2048),self.data[index-1],None)
                self.theory.estimate()
                fitresult, result = self.theory.startfit(digest=1)
                self.processed.append((fitresult,result))
                ##IMAGE PROCESSING##
                self.__peaks  = []
                self.__images = {}
                self.__sigmas = {}
                self.__nrows   = len(range(0,max_index))
                for group in result['groups']:
                    self.__peaks.append(group)
                    self.__images[group]=Numeric.zeros((self.__nrows,1),Numeric.Float)
                    self.__sigmas[group]=Numeric.zeros((self.__nrows,1),Numeric.Float)
                self.__images['chisq']  = Numeric.zeros((self.__nrows,1),Numeric.Float) - 1.
                self.__images['chisq'][index-1, 0] = result['chisq']
                for peak in self.__peaks:
                    self.__images[peak][index-1, 0] = result[peak]['fitarea']
                    self.__sigmas[peak][index-1,0] = result[peak]['sigmaarea']
                    if setup<len(self.__peaks):
                        self.Qimages[peak]=QImageTab(self.ElementTaber,peak,
                                                                    self.__images[peak],max_index_x,max_index_y)
                        setup+=1
                ## QImaging##
                for peak in self.__peaks:
                    self.Qimages[peak].update(self.__images[peak])
        self.ElementTaber.removeTab(0)
        print "data collected and processed"
        matshow(self.__images["Mn K"])
        show()
##        print type(self.Qimages['Mn K'].graphics)
class QImageTab:
    def __init__(self,master,title,matrix,x,y):
        self.matrix=matrix
        self.x=x
        self.y=y
        self.graphics=MyMplCanvas(matrix,x,y)
        master.addTab(self.graphics,title)
    def update(self,matrix):
        self.matrix=matrix
        self.graphics=MyMplCanvas(matrix,self.x,self.y)
if GRAPH==0:
    class MyMplCanvas(FigureCanvas):
        def __init__(self,matrix, x,y,parent=None, width=5, height=4, dpi=100):
            self.matrix=matrix.reshape(x,y)
            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.image=self.fig.figimage(self.matrix)#.draw(?????)
            FigureCanvas.__init__(self, self.fig)
            self.setParent(parent)
            FigureCanvas.setSizePolicy(self,
                                       QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
            self.draw()
    
        def sizeHint(self):
            w, h = self.get_width_height()
            return QtCore.QSize(w, h)
    
        def minimumSizeHint(self):
            return QtCore.QSize(10, 10)
else :
    class MyMplCanvas(FigureCanvas):
        """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
        def __init__(self, matrix,x,y,parent=None, width=5, height=4, dpi=100):
            self.matrix=matrix.reshape(x,y)
            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = self.fig.add_subplot(111)
            # We want the axes cleared every time plot() is called
            self.axes.hold(False)
    
            self.compute_initial_figure()
    
            FigureCanvas.__init__(self, self.fig)
            self.setParent(parent)
    
            FigureCanvas.setSizePolicy(self,
                                       QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
    
        def sizeHint(self):
            w, h = self.get_width_height()
            return QtCore.QSize(w, h)
    
        def minimumSizeHint(self):
            return QtCore.QSize(10, 10)
    
        def compute_initial_figure(self):
            s = self.matrix.flatten()
            t = arange(0.0, 3+len(s), 1)
            print len(t) ,len(s)
            self.axes.plot(t,s)
##            self.axes.figimage(self.matrix)
##            self.draw()
   


class Spinner_Slide_Motor:
    def __init__(self,Slide,Spin, Motor,Min,Max,Step):
        self.Spin=Spin
        self.Slide=Slide
        self.Motor=Motor
        self.Min=Min
        self.Max=Max
        self.Step=Step
        QtCore.QObject.connect(self.Slide,QtCore.SIGNAL("sliderReleased()"),
                               self.slide)
        QtCore.QObject.connect(self.Spin,
                               QtCore.SIGNAL("editingFinished()"),self.spin)
        self.get_params()
        self.setup()
    def get_params(self):
        self.values=[]
        params=['position','offset','sign',"low_limit","high_limit","step_size"]
        for param in params:
            try: 
                self.values.append(self.Motor.getParameter(param))
            except:
                self.values.append("unable to get value")
            
    def setup(self):
        values=self.values
        min =values[2]*values[3]+values[1]
        max=values[2]*values[4]+values[1]
        motor_step_size=values[5]
        self.Step.setRange(-100000,100000)
        self.Step.setValue(1)
        self.Max.setRange(min,max)
        self.Min.setRange(min,max)
        self.Max.setValue(max)
        self.Min.setValue(min)
        self.Spin.setRange(min,max)
        self.Slide.setRange(min*motor_step_size,max*motor_step_size)
        self.Spin.setValue(self.values[0])
        self.Slide.setTickInterval(20*motor_step_size)
        self.spin()
    def slide(self):
        self.Spin.setValue(self.Slide.value()/self.value[5])
    def spin(self):
        self.Slide.setValue(self.Spin.value()*self.values[5])
    def Move(self):
        self.Motor.move(self.Spin.value())
    def get_settings(self):
        return (self.Min.value(),self.Max.value(),self.Step.value())
    def get_motor_name(self):
        return self.motor.specName
        





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyXP()
    myapp.show()
    sys.exit(app.exec_())
