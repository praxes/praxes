#!/usr/bin/env python
################################################################################

import codecs
import pexpect
import os
import sys


#GUI
from PyQt4 import QtCore, QtGui
from Konsole import Ui_Kontrol

class MyKon(Ui_Kontrol,QtGui.QMainWindow):

    """Establishes a custom Console for interacting with the Computer"""

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.Runner, QtCore.SIGNAL("clicked()"),
                               self.konsole)
        QtCore.QObject.connect(self.MacroSave, QtCore.SIGNAL("clicked()"),
                               self.macrosave)
        QtCore.QObject.connect(self.changer, QtCore.SIGNAL("clicked()"),
                               self.change)

    def macrosave(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        s = codecs.open(self.filename,'w','utf-8')
        s.write(unicode(self.KonsoleEm.toPlainText()))
        s.close()

    def change(self):
        try:
            fd = QtGui.QFileDialog(self)
            self.path = "%s"%fd.getExistingDirectory()
            os.chdir(self.path)
        except: 
            os.system("dir")

    def konsole(self):
        self.Display.append(">>>"+self.KonsoleEm.toPlainText())
        Kommands=self.KonsoleEm.toPlainText().split(";")
        for i in range(len(Kommands)):
            Kommand="%s"%Kommands[i]
            doingit=pexpect.run(Kommand)
            self.Display.append(doingit)

            
if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MyKon()
    myapp.show()
    sys.exit(app.exec_())
