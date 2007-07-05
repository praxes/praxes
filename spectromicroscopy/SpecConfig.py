"""
motor_par(i, s [, v])
    Returns or sets configuration parameters for motor i.
     Recognized values for the string s include:


    "step_size"
        returns the current step-size parameter. 
        The units are generally in steps per degree or steps per millimeter. 
        If v is given, then the step size is set to that value. 
        Since the calculated motor positions will be affected by a change in the step size, 
        the function spec_par("modify_step_size", 1) must be entered first to enable step-size 
        modifications using motor_par().

    "acceleration"
        returns the value of the current acceleration parameter. 
        The units of acceleration are the time in milliseconds
        for the motor to accelerate to full speed.
        If v is given, then the acceleration is set to that value.

    "base_rate"
        returns the current base-rate parameter. The units are steps per second. 
        If v is given, then the base rate is set to that value.

    "velocity"
        returns the current steady- state velocity parameter. 
        The units are steps per second. If v is given, 
        then the steady-state velocity is set to that value.

    "backlash"
        returns the value of the backlash parameter. 
        Its sign and magnitude determine the direction and 
        extent of the motor's backlash correction. 
        If v is given, then the backlash is set to that value. 
        Setting the backlash to zero disables the backlash correction. 
set_lim(i, u, v)
    Sets the low and high dial limits of motor i. 
    It doesn't matter which order the limits, u and v, are given. 
    Returns -1 if not configured for motor i 
    or if the motor is protected, unusable or moving, else returns 0.


"""
from PyQt4 import QtGui, QtCore
from SpecSetter import Ui_SpecSetter 
class SpecConfig(QtGui.QWidget,Ui_SpecSetter):
    
    __pyqtSignals__ =("configChanged()")
    
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.Setter, QtCore.SIGNAL("clicked()"),
                               self.set)
    def set(self):
        Accel=self.Accel.getValue()
        BR=self.BR.getValue()
        BLash=self.Blash.getValue()
        LL=self.LL.getValue()
        Name=self.Name.getText()
        Sign=self.Sign.getValue()
        Speed=self.Speed.getValue()
        UL=self.UL.getValue()
        print "set_lim(%s,%s,%s)"%(Name,LL,UL)
        
    

"""
class SpecConfigPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent = None):
        QtDesigner.QPyDesignerCustomWidgetPlugin.__init__(self)
        self.initialized = False        
    def initialize(self, core):
        if self.initialized:
            return 
        self.initialized = True
    def isInitialized(self):
        return self.initialized
    def createWidget(self, parent):
        return SpecConfig(parent)
    def name(self):
        return "SpecConfig"
    def group(self):
        return "PyQt Examples"
    def icon(self):
        return QtGui.QIcon(_logo_pixmap)
    def toolTip(self):
        return ""
    def whatsThis(self):
        return ""
    def isContainer(self):
        return True
    def includeFile(self):
        return "SpecSetter"
    """
if __name__=="__main__":
    import sys,os
    path=path=os.path.join(os.path.expanduser("~"),
            "workspace/spectromicroscopy/spectromicroscopy/")
    os.system("pyuic4 %s/SpecSetter.ui>%s/SpecSetter.py"%(path,path))
    app = QtGui.QApplication(sys.argv)
    myapp = SpecConfig()
    myapp.show()
    sys.exit(app.exec_())
