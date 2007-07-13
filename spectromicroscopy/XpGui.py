import sys, os, codecs
from os.path import isfile
    
DEBUG=1

#GUI
from PyQt4 import QtCore, QtGui
from Xp import Ui_XPrun
from XpRunner import XpRunner

class MyXP(Ui_XPrun,QtGui.QMainWindow):
    """Establishes a Experimenbt controls"""
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.Mv,
                               QtCore.SIGNAL("clicked()"),self.Move)
        if parent:
            self.xprun=XpRunner(parent.get_specrun())
            MotorX=self.xprun.get_motor('samx')
            MotorY=self.xprun.get_motor('samy')
            MotorZ=self.xprun.get_motor('samz')
        
        self.X=Spinner_Slide_Motor(self.Xslide,self.SpinX,MotorX)
        self.Y=Spinner_Slide_Motor(self.Yslide,self.SpinY,MotorY)
        self.Z=Spinner_Slide_Motor(self.Zslide,self.SpinZ,MotorZ)
        self.dict={}
        self.dict["X"]=(self.Xslide,self.SpinX,MotorX,self.X)
        self.dict["Y"]=(self.Yslide,self.SpinY,MotorY,self.Y)
        self.dict["Z"]=(self.Zslide,self.SpinZ,MotorZ,self.Z)

        if DEBUG==1:
            self.Xslide.setRange(0,10000)
            self.SpinX.setRange(0,100)
            self.Yslide.setRange(0,10000)
            self.SpinY.setRange(0,100) 
            self.Zslide.setRange(0,10000)
            self.SpinZ.setRange(0,100)
            self.Xsize=100.00
            self.Ysize=100.00
            self.Zsize=100.00
            self.Xslide.setTickInterval(1000.00)
            self.Yslide.setTickInterval(1000.00)
            self.Zslide.setTickInterval(1000.00)
        else:
            self.X.run()
            self.Y.run()
            self.Z.run()
            #TODO: set up ticks = (Max-Min)stepsize
            """self.Xslide.setTickInterval()
            self.Yslide.setTickInterval()
            self.Zslide.setTickInterval()"""
        

    def Step(self):
        Axis="%s"%self.Namer.text()
        Axis=Axis.capitalize()
        if Axis in self.dict.keys():
            (selectAxis,Spin,motor)=self.dict[Axis]
            if DEBUG==1:
                viable=True
                stepsize=100
            else:
                selectAxis.setTickInterval(self.Stepper.value()*stepsize)
                selectAxis.setSingleStep(self.Stepper.value()*stepsize)
                Spin.setSingleStep(self.Stepper.value())
                
                
    def Move(self):
        if DEBUG==1:
            print "moved"
        else:
            self.X.move()
            self.Y.move()
            self.Z.move()
        

class Spinner_Slide_Motor:
    def __init__(self,Spin,Slide,Motor):
        self.Spin=Spin
        self.Slide=Slide
        self.Motor=Motor
        QtCore.QObject.connect(self.Slide,QtCore.SIGNAL("sliderReleased()"),
                               self.run)
        QtCore.QObject.connect(self.Spin,
                               QtCore.SIGNAL("editingFinished()"),self.spin)
    def run(self):
        if DEBUG!=1:
            Size=Motor.getOFFset()
            (min,max)=Motor.getlimits()
            self.Spin.setRange(min,max)
            self.Slide.setRange(min,max)
        self.Spin.setValue(self.Slide.value()/self.Size)
    def spin(self):
        self.Slide.setValue(self.Spin.value()*self.Size)
    def Move(self):
        self.Motor.move(self.Spin.getValue())
        


if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MyXP()
    myapp.show()
    sys.exit(app.exec_())
