import sys, os, codecs
from os.path import isfile
    
DEBUG=1

#GUI
from PyQt4 import QtCore, QtGui
from Xp import Ui_XPrun

class MyXP(Ui_XPrun,QtGui.QMainWindow):
    """Establishes a Experimenbt controls"""
    def __init__(self,parent=None,MotorX=None,MotorY=None,MotorZ=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.Xslide,QtCore.SIGNAL("sliderReleased()"),
                               self.X)
        QtCore.QObject.connect(self.Yslide,QtCore.SIGNAL("sliderReleased()"),
                               self.Y)
        QtCore.QObject.connect(self.Zslide,QtCore.SIGNAL("sliderReleased()"),
                               self.Z)
        QtCore.QObject.connect(self.SpinX,
                               QtCore.SIGNAL("editingFinished()"),self.SpinnerX)
        QtCore.QObject.connect(self.SpinY,
                               QtCore.SIGNAL("editingFinished()"),self.SpinnerY)
        QtCore.QObject.connect(self.SpinZ,
                               QtCore.SIGNAL("editingFinished()"),self.SpinnerZ)
        QtCore.QObject.connect(self.Stepper,
                               QtCore.SIGNAL("editingFinished()"),self.Step)
        QtCore.QObject.connect(self.Stepper,
                               QtCore.SIGNAL("clicked()"),self.Move)
        self.Namer.setMaxLength(1)
        self.dict={}
        self.dict["X"]=(self.X,self.SpinX,MotorX)
        self.dict["Y"]=(self.Y,self.SpinY,MotorY)
        self.dict["Z"]=(self.Z,self.SpinZ,MotorZ)
        # TODO: rework all this XYZ code to work with motors
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
            pass
            #TODO: set up ticks = (Max-Min)stepsize
            """self.Xslide.setTickInterval()
            self.Yslide.setTickInterval()
            self.Zslide.setTickInterval()"""
        self.X()
        self.Y()
        self.Z()
        

    def X(self):
        if DEBUG!=1:
            Xsize=MotorX.getOFFset()
            (Xmin,Xmax)=MotorX.getlimits()
            self.SpinX.setRange(Xmin,Xmax)
            self.Xslide.setRange(Xmin,Xmax)
        self.SpinX.setValue(self.Xslide.value()/self.Xsize)
    def Y(self):
        if DEBUG!=1:
            self.Ysize=MotorY.getOFFset()
            (Ymin,Ymax)=MotorY.getlimits()
            self.SpinY.setRange(Ymin,Ymax)
            self.Yslide.setRange(Ymin,Ymax)
        self.SpinY.setValue(self.Yslide.value()/self.Ysize)
    def Z(self):
        if DEBUG!=1:
            Zsize=MotorZ.getOFFset()
            (Zmin,Zmax)=MotorZ.getlimits()
            self.SpinZ.setRange(Zmin,Zmax)
            self.Zslide.setRange(Zmin,Zmax)
        self.SpinZ.setValue(self.Zslide.value()/self.Zsize)
    def SpinnerX(self):
        self.Xslide.setValue(self.SpinX.value()*self.Xsize)
    def SpinnerY(self):
        self.Yslide.setValue(self.SpinY.value()*self.Ysize)
    def SpinnerZ(self):
        self.Zslide.setValue(self.SpinZ.value()*self.Zsize)
    
    def Step(self):
        Axis="%s"%self.Namer.text()
        Axis=Axis.capitalize()
        if Axis in self.dict.keys():
            (selectAxis,Spin,motor)=self.dict[Axis]
            if DEBUG==1:
                viable=True
                stepsize=100
            else:
                viable=self.Stepper.value()<motor.getOffset()
                stepsize=motor.setOffset(self.Stepper.value())
            if viable:
                selectAxis.setTickInterval(self.Stepper.value()*stepsize)
                selectAxis.setSingleStep(self.Stepper.value()*stepsize)
                Spin.setSingleStep(self.Stepper.value())
                
                
    def Move(self):
        if DEBUG==1:
            print "moved"
        else:
            MotorX.move(self.Xslide.getValue())
            MotorY.move(self.Yslide.getValue())
            MotorZ.move(self.Zslide.getValue())
        
        

if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MyXP()
    myapp.show()
    sys.exit(app.exec_())
