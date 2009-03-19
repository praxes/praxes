"""
"""
from __future__ import absolute_import

import codecs
import logging
import os
import sys
import time

from PyQt4 import QtCore, QtGui
import pxssh

from .ui import ui_sshdialog


logger = logging.getLogger(__file__)


class SshDialog(ui_sshdialog.Ui_Dialog, QtGui.QDialog):
    """Establishes a SSH to start spec"""

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.userEdit.setFocus()
#        self.log = parent.logRead
        self.SSH = None
        self.settings = QtCore.QSettings()
        geometry = self.settings.value('SpecConnect/SSHGeometry').toByteArray()
        self.restoreGeometry(geometry)


    def exec_(self):
        if QtGui.QDialog.exec_(self):
            self.sshconnect()
            if self.SSH is None: self.exec_()
            self.settings.setValue('SpecConnect/SSHGeometry',
                          QtCore.QVariant(self.saveGeometry()))
            return self.SSH

    def sshconnect(self):
        server = self.settings.value('Server').toString()
        spec = self.settings.value("Port").toString()
        cmd = spec+" -S"
        user = "%s"%self.userEdit.text()
        pwd = "%s"%self.pwdEdit.text()
        self.SSH = pxssh.pxssh()

        if self.SSH.login(server, user, pwd):
            logger.info('connected to %s@%s',user,server)
            self.SSH.sendline(cmd)
            self.SSH.prompt()
            logger.debug(self.SSH.before)

            time.sleep(1)
            if not len(self.SSH.before) > 250:
                warning = QtGui.QMessageBox.warning(self, "Spec Error",
                            self.SSH.before+"\n Kill %s on %s?"%(spec, server),
                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | \
                                QtGui.QMessageBox.Cancel)
                if warning == QtGui.QMessageBox.Yes:
                    self.SSH.sendline('killall %s'%spec)
                    logger.info('killall %s'%spec)

                    self.SSH = None
                    self.sshconnect()
        else:
            logger.error('Connection Error')
            error = QtGui.QMessageBox.warning(self, "Connection Error",
                                              str(self.SSH))

            self.SSH = None
        self.parent().SSH=self.SSH


if __name__ == "__main__":
#    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = SshDialog()
    myapp.show()
    sys.exit(app.exec_())
