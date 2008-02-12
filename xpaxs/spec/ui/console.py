"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import codecs
import os
import pexpect
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.spec.ui import ui_console

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

class MyKon(ui_console.Ui_Kontrol, QtGui.QMainWindow):

    """Establishes a custom Console for interacting with the Computer"""

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.runButton,
                     QtCore.SIGNAL("clicked()"),
                     self.konsole)
        self.connect(self.macroSaveButton,
                     QtCore.SIGNAL("clicked()"),
                     self.macroSave)
        self.connect(self.changeDirButton,
                     QtCore.SIGNAL("clicked()"),
                     self.change)

    def macroSave(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        s = codecs.open(self.filename,'w','utf-8')
        s.write(unicode(self.textEditKonsole.toPlainText()))
        s.close()

    def change(self):
        try:
            fd = QtGui.QFileDialog(self)
            self.path = "%s"%fd.getExistingDirectory()
            os.chdir(self.path)
            self.dirLineEdit.setText(self.path)
        except: 
            os.system("dir")

    def konsole(self):
        self.textDisplay.append(">>>"+self.textEditKonsole.toPlainText())
        commands = self.textEditKonsole.toPlainText().split(";")
        for command in commands:
            doingit = pexpect.run("%s"%command)
            self.textDisplay.append(doingit)

            
if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MyKon()
    myapp.show()
    sys.exit(app.exec_())
