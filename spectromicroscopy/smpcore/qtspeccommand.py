"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import sys
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.external.SpecClient import SpecCommand

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class TestSpecCommand(SpecCommand.SpecCommandA):

    def beingWait(self):
        if DEBUG: print 'Command %s was sent'%self.command
    
    def replyArrived(self, reply):
        self.Reply=reply
        if (reply.error):
            print "command %s received an error message: %s"% \
                (self.command, reply.data)
        else:
            print "Command %s received a reply: %s"%(self.command, reply.data)
    
    def connected(self):
       if DEBUG: print "Command %s connected"% self.command
       self.Reply = None
    
    def disconnected(self):
        if DEBUG: print "Command %s disconnected"% self.command
                
    def statusChanged(self, ready):
        state = ["In progress","Complete","Unknown"]
        if DEBUG: print "Status is %s"%state[ready]
    
    def get_Reply(self):
        return self.Reply
