"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.external.SpecClient import SpecCommand

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = False


class QtSpecCommandA(SpecCommand.SpecCommandA, QtCore.QObject):

    def __init__(self, cmd, specVersion):
        QtCore.QObject.__init__(self)
        SpecCommand.SpecCommandA.__init__(self, cmd, specVersion)

    def beingWait(self):
        if DEBUG: print 'Command %s was sent'%self.command
    
    def connected(self):
       if DEBUG: print "Command %s connected"% self.command
       self.Reply = None
    
    def disconnected(self):
        if DEBUG: print "Command %s disconnected"% self.command
                
    def statusChanged(self, ready):
        state = ["In progress","Complete","Unknown"]
        if DEBUG: print "Status is %s"%state[ready]

