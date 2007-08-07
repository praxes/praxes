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
# TODO: This is not the right module for analysis
from PyMca import ClassMcaTheory , ConcentrationsTool #,McaAdvancedFitBatch
from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from ui_testinterface import Ui_MotorHead
from spectromicroscopy.smpcore import SpecRunner
#from SpecConfig import SpecConfig

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG=0     #if set to 1 it deactivates spec commands
Rollcall=2    #if set to 1 it auto starts spec -s on f3.chess.cornell.edu
              #and connects if set to 2 it wont autostart but will autoconnect
              #if set to 3 it will autoconnect and start spec on roll

              
class MyUI(Ui_MotorHead,QtGui.QMainWindow):
    """Any and all things GUI"""
    def __init__(self, parent=None):
        self.startSesh() #to be removed when done
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
#        self.custom()
        if parent:
            Bar=parent.Bar
        else:
            Bar=self.Bar
        Bar.addAction("New Macro",self.macro)
        Bar.addAction("Old Macro",self.tester)
        self.filename=''
        self.command=''
        self.estop=''
        sys.stdout=self
        self.specrun=SpecRunner(self,DEBUG)
        time_ = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print "Rollcall=%s, DEBUG=%s"%(Rollcall,DEBUG)                                  # REMOVE WHEN DONE
        print "\n New Session started (%s)\n Enter spec server hostname: "%time_
        QtCore.QObject.connect(self.ChangeFile, QtCore.SIGNAL("clicked()"),
                               self.file_dialog)
        QtCore.QObject.connect(self.saveras,QtCore.SIGNAL("clicked()"),
                               self.file_saveas)
        QtCore.QObject.connect(self.ClearLog, QtCore.SIGNAL("clicked()"),
                               self.clearlog)
        QtCore.QObject.connect(self.EStop, QtCore.SIGNAL("clicked()"),
                               self.EmergencyStop)
        QtCore.QObject.connect(self.ReStart, QtCore.SIGNAL("clicked()"),
                               self.reStart)
        QtCore.QObject.connect(self.CommandLine, 
                               QtCore.SIGNAL("returnPressed()"), self.input)
        QtCore.QObject.connect(self.MotorsTree, QtCore.SIGNAL("itemSelectionChanged ()"), self.select_motor)
        QtCore.QObject.connect(self.Mover, QtCore.SIGNAL("clicked()"),
                               self.cmdMove)
        QtCore.QObject.connect(self.SpecCMD, QtCore.SIGNAL("clicked()"), self.spec_cmd)
        QtCore.QObject.connect(self.Closer,QtCore.SIGNAL("clicked()"),\
                                 self.endsesh)
        QtCore.QObject.connect(self.plus, QtCore.SIGNAL("clicked()"),
                               self.Plus)
        QtCore.QObject.connect(self.ReStart, QtCore.SIGNAL("clicked()"),
                               self.reStart)
        
        
        if Rollcall==1 or Rollcall==2:
            self.specrun.set_spec_host("f3.chess.cornell.edu")
            self.CommandLine.setText("xrf")
        elif Rollcall==3:
            self.specrun.set_spec_host("roll.chess.cornell.edu")
            self.CommandLine.setText("spec")

            
    def runspec(self):
        self.buffer=tempfile.TemporaryFile('w+b')
        if not self.specrun.get_spec_host():
            self.specrun.set_spec_host(self.command)
            print " Host set as %s \n Select a Port"%self.command
        elif not self.specrun.get_spec_port():
            self.specrun.set_spec_port(self.command)
            print " Port set as %s"%self.command
            try:
                self.connection=self.specrun.serverconnect()
            except:
                print "Invalid Host or Server"
            if self.connection:
                print " Connected to %s on %s"%(self.specrun.get_spec_port(),
                                                self.specrun.get_spec_host())
                self.specrun.readmotors()
                self.get_motors()
                self.get_params()
                print " Select a motor"
            else:
                print "Connection Failed"
                self.specrun.set_spec_host('')
                self.specrun.set_spec_port('')
        elif not self.specrun.get_motor_name():
            self.MotorsTree.setItemSelected(self.motor_widget_dict[self.command],True)
        elif not self.specrun.get_var():
            QtCore.QObject.connect(self.ResetVar, QtCore.SIGNAL("clicked()"), self.specrun.reset_var)
            vars=self.command.split(";")
            for var in vars:
                self.specrun.set_var(var)
                print " %s to be monitored" %var 
            print"Select a command to run asynchronously: "
        elif not self.specrun.get_cmd():
            self.specrun.set_cmd(self.command)
            self.specrun.run_cmd()
            self.processed=[]
            file =os.path.join("/home/jeff/src/smp/spectromicroscopy","17KeV.cfg")
            self.theory=ClassMcaTheory.McaTheory(file)
            self.theory.enableOptimizedLinearFit()
            self.data=numpy.memmap(self.buffer.name,dtype=float,mode='w+',shape=(self.max,2048))
            while self.update() and not self.estop:
                (value,index,actual)=self.specrun.get_values()
                if actual:
                    typed=type(value[0])
                    print "<<%s>> %s"%(index,typed)
                    if typed==type(1) or typed==type(1.0):
                        print "int or float:", value[0]
                    elif typed==type({}):
                        for key in value[0].keys():
                            self.data[index,int(key)]=float(value[0][key])
                            pass
                        print "DICT"
                    elif typed==type(""):
                        print "string: ",value[0]
                    else:
                        for i in range(len(value[0])):
                            if len(value[0])>1:
                                self.data[index-1,i]=value[0][i][1]
                            else:
                                self.data[index-1,i]=value[0][i]
            print "data collected"
            self.specrun.set_cmd('')
        else:
            print ":P"
        

    def input(self):
        """converts a string from the textbox into motors and variables"""
        self.command="%s"%self.CommandLine.text().toAscii()
        self.CommandLine.clear()
        self.specrun.exc('IndexVar=-1')
        print "\n>>>>%s"%self.command
        self.runspec()
        
    def write(self,string):
        """stdout for program, displays on the Responses screen"""
        if string!="\n":
            self.last_written=string
            sys.stdout=sys.__stdout__
            print self.last_written
            sys.stdout=self
            if os.path.isfile (self.filename):
                s = codecs.open(self.filename,'a','utf-8')
                s.write(unicode(string))
                s.close()
            self.Responses.append(string)

    def EmergencyStop(self):
        """Stops all spec commands"""
        self.estop=True
        self.specrun.EmergencyStop() 
    
    def clearlog(self):
        """Clears Log File"""
        self.Responses.clear()
        if os.path.isfile(self.filename):
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.Responses.toPlainText()))
            s.close()
        self.write(self.last_written)
    def file_dialog(self):
        """Changes Log File"""
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        if os.path.isfile(self.filename):
            s = codecs.open(self.filename,'r','utf-8').read()
            self.Responses.setPlainText(s)

    def file_saveas(self):
        """Saves Log File"""
        self.currentfile=self.filename
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        if os.path.isfile(self.filename):
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.Responses.toPlainText()))
            s.close()
            self.filename=self.currentfile   
                      
    def macro(self):
        """Opens Macro Editor"""
        if sys.platform=="win32":
            print "signal sent"
        else:
            os.system("gedit")

    def get_motors(self):
        """Generates Motors as widgets and names for MotorTree
        
        self.motordict--widget=key name=tag
        """
        self.motor_widget_dict={}
        self.motor_widget_list=[]
        motor_names=self.specrun.get_motor_names()
        for name in motor_names:
            item = QtGui.QTreeWidgetItem(self.MotorsTree)
            item.setText(0, name)
            item.setText(1, self.specrun.status(name))
            self.motor_widget_list.append(item)
            self.motor_widget_dict[name]=item
        
    def select_motor(self):
        """Selects the motors based on widgets selected in MotorTree"""
        if self.MotorsTree.selectedItems()[0].parent()==None:
            name="%s"%self.MotorsTree.selectedItems()[0].text(0)
            self.specrun.set_motor(name)
            print " **%s selected**\n Select a Variable"%name
            try:
                if DEBUG==1:            
                    min = 30
                    max = 100
                else:
                    (min,max)=self.specrun.get_motor_limits(name)
                self.MoveBar.setRange(min,max)
                self.Positioner.setRange(min,max)
            except:
                print "unable to get limits of motor"
            try:
                if DEBUG==1:
                    place=0
                else:
                    place=self.specrun.get_motor_position(name)
                self.MoveBar.setValue(place)
                self.Positioner.setValue(place)
            except:
                print "Unable to Get Position"
            

    def get_params(self):
        """gets variables from specrun
        
        self.vardict--widget=key name=tag
        """
        self.paramwidget=[]
        for motorname in self.specrun.get_motor_names():
            MotorsParam= self.specrun.get_params_names()
            MotorValues=self.specrun.readParam(motorname)
            j=0
            for Param in MotorsParam:
                widget=QtGui.QTreeWidgetItem(self.motor_widget_dict[motorname])
                widget.setText(0,"%s is %s"%(Param,MotorValues[j]))
                self.paramwidget.append(widget)
                j+=1

    def update(self):
        for widget in self.motor_widget_list:
            widget.setText(1, self.specrun.status("%s"%widget.text(0)))
        for widget in self.paramwidget:
            Param="%s"%widget.text(0)
            Param=Param.split(" ",1)[0]
            j=self.specrun.get_params_names().index(Param)
            MotorValues=self.specrun.readParam("%s"%widget.parent().text(0))
            widget.setText(0,"%s is %s"%(Param,MotorValues[j]))
        if not self.specrun.get_cmd_reply():
            self.specrun.update()
            return 1
        else:
            return 0
    
    def cmdMove(self):
        """Moves selected motor"""
        cmd="mv %s %s"%(self.specrun.get_motor_name(),self.Positioner.value())
        self.specrun.set_cmd(cmd)
        self.specrun.run_cmd()
    def spec_cmd(self):
        if self.connection:
            self.specrun.exc("%s"%self.CommandLine.text().toAscii())
            self.CommandLine.clear()
    
    def get_specrun(self):
        return self.specrun
    
    def reStart(self):
        """restarts the run"""
        self.specrun=SpecRunner(DEBUG, self)
        self.MotorsTree.clear()
        print "\n Enter spec server hostname: "
        self.clearlog()
    def startSesh(self):
        """to be removed when done"""
        if Rollcall==1:
            import pxssh
            self.sesh = pxssh.pxssh()
            if not self.sesh.login ('f3.chess.cornell.edu', 'specuser', 'CThrooMe'):
                print"SSH session failed on login."
                print str(self.sesh)
            else:
                print "SSH session login successful"
                self.sesh.sendline ('xrf -S')
                self.sesh.prompt()
                print self.sesh.before
        elif Rollcall==3:
            import pxssh
            self.sesh = pxssh.pxssh()
            if not self.sesh.login ('roll.chess.cornell.edu', 'specuser', 'CThrooMe'):
                print"SSH session failed on login."
                print str(self.sesh)
            else:
                print "SSH session login successful"
                self.sesh.sendline("killall spec")
                self.sesh.sendline ('spec -S')
                self.sesh.prompt()
                print self.sesh.before
              
        else:
            self.sesh=None
    def endsesh(self):
        """Tobe removed when done"""
        if self.sesh:
            self.sesh.sendline('^D')
            self.sesh.prompt
            print self.sesh.before
            self.sesh.sendline("logout")
            self.sesh.close()
        else:
            time_=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            print "BYE!!!!!!!@%s"%time_
#    def custom(self):
#        self.widget=SpecConfig(self)
#        self.widget.setGeometry(10,330,441,141)
        

    
    def tester(self):
        """used to see if a signal is received, only for testing stage"""
        print "signaled"
        
    def Plus(self):
        self.specrun.set_cmd("mvr %s %s"%(self.specrun.get_motor_name(),self.dis.value()))
        self.specrun.run_cmd()
        while self.update() and not self.estop:
            self.update()
    def Minus(self):
        self.specrun.set_cmd("mvr %s %s"%(self.specrun.get_motor_name(),-self.dis.value()))
        self.specrun.run_cmd()
        while self.update() and not self.estop:
            self.update()

                   
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyUI()
    myapp.show()
    sys.exit(app.exec_())
