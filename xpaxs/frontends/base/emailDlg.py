#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from __future__ import absolute_import

import logging
import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .ui import ui_emailDlg

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.dispatch.emailDlg')


class EmailDialog(ui_emailDlg.Ui_emailDialog, QtGui.QDialog):
    """Establishes a email settings """

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.allEdit.setFocus()
        self.settings = QtCore.QSettings()
        self.getValues()
        self.connect(self.importantBox, QtCore.SIGNAL('toggled(bool)'), self.importantWarn)

    def importantWarn(self, bool):
        if bool:
            response = QtGui.QMessageBox.warning(self,
                            'Editing Important Emails',
                            'Only edit these addresses if you are the system administrator', QtGui.QMessageBox.Ok| QtGui.QMessageBox.Cancel)
            if response == QtGui.QMessageBox.Ok:
                self.importantEdit.setEnabled(True)
            else:
                self.importantEdit.setEnabled(False)
                self.importantBox.setChecked(False)


    def exec_(self):
        if QtGui.QDialog.exec_(self):
            self.setValues()

    def accept(self):
        self.setValues()
        QtGui.QDialog.accept(self)

    def setValues(self):
            self.settings.setValue('Email/emailDlgGeometry',
                          QtCore.QVariant(self.saveGeometry()))
            self.settings.setValue('Email/server',
                          QtCore.QVariant(self.serverEdit.text()))
            self.settings.setValue('Email/port',
                          QtCore.QVariant(self.portSpin.value()))
            self.settings.setValue('Email/user',
                          QtCore.QVariant(self.loginEdit.text()))
            self.settings.setValue('Email/pwd',
                          QtCore.QVariant(self.passEdit.text()))
            self.settings.setValue('Email/mailFrom',
                          QtCore.QVariant(self.fromEdit.text()))
            self.settings.setValue('Email/importantAddresses',
                          QtCore.QVariant(self.importantEdit.document().toPlainText()))
            self.settings.setValue('Email/regularAddresses',
                          QtCore.QVariant(self.allEdit.document().toPlainText()))
            self.settings.setValue('Email/tls',
                          QtCore.QVariant(self.tlsCheck.isChecked()))
            self.settings.setValue('Email/secure',
                          QtCore.QVariant(self.secureCheck.isChecked()))

    def getValues(self):
        self.restoreGeometry(self.settings.value('Email/emailDlgGeometry').toByteArray())
        self.serverEdit.setText(self.settings.value('Email/server').toString())
        self.portSpin.setValue(self.settings.value('Email/port').toInt()[0])
        self.loginEdit.setText(self.settings.value('Email/user').toString())
        self.passEdit.setText(self.settings.value('Email/pwd').toString())
        self.fromEdit.setText(self.settings.value('Email/mailFrom').toString())
        self.importantEdit.setText(self.settings.value('Email/importantAddresses').toString())
        self.allEdit.setText(self.settings.value('Email/regularAddresses').toString())
        self.tlsCheck.setChecked(self.settings.value('Email/tls').toBool())
        self.secureCheck.setChecked(self.settings.value('Email/secure').toBool())



if __name__ == "__main__":
#    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = EmailDialog()
    myapp.show()
    sys.exit(app.exec_())
