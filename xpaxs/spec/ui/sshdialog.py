#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import codecs
import os
import sys

import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from pexpect import pxssh


#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from xpaxs.spec.ui import ui_sshdialog

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

class SshDialog(ui_sshdialog.Ui_Dialog, QtGui.QDialog):
    """Establishes a SSH to start spec"""

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.log = parent.logRead
        self.SSH = None

    def exec_(self):
        if QtGui.QDialog.exec_(self):
            self.sshconnect()
            if self.SSH is None: self.exec_()
            return self.SSH

    def sshconnect(self):
        settings = QtCore.QSettings()
        server = settings.value('Server').toString()
        spec = settings.value("Port").toString()
        cmd = spec+" -S"
        user = "%s"%self.userEdit.text()
        pwd = "%s"%self.pwdEdit.text()
        self.SSH = pxssh.pxssh()

        try:
            if self.SSH.login(server, user, pwd, login_timeout=10000):
                self.SSH.sendline(cmd)
                self.SSH.prompt()
                print self.SSH.before
                self.log.append(self.SSH.before)
                time.sleep(1)
                if not len(self.SSH.before) > 250:
                    warning = QtGui.QMessageBox.warning(self, "Spec Error",
                                self.SSH.before+"\n Kill %s on %s?"%(spec, server),
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | \
                                    QtGui.QMessageBox.Cancel)
                    if warning == QtGui.QMessageBox.Yes:
                        self.SSH.sendline('killall %s'%spec)
                        self.log.append('killall %s'%spec)
                        self.SSH = None
                        self.sshconnect()

            else:
                error = QtGui.QMessageBox.warning(self, "Connection Error",
                                                str(self.SSH))
                self.log.append(self.SSH)
                self.SSH = None
        except pxssh.TIMEOUT:
            self.SSH = None


if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = SshDialog()
    myapp.show()
    sys.exit(app.exec_())
