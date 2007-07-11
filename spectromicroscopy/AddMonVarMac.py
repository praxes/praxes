import SpecClient
SpecClient.setLoggingOff()
from SpecClient import SpecMotor, Spec, SpecEventsDispatcher, SpecVariable, SpecCommand
MonDef="def MonitorLoop 'IndexVar+=1'"
    ## add to user_scan_loop
SetDef="def SetMon 'global IndexVar IndexVar= -1'"
    ## add to user_scan_tail
    ## add to _cleanup2 in order to ensure reset at abort
A='cdef("user_scan_loop", "MonitorLoop;","zru",0x01)'
B='cdef("user_scan_tail","SetMon","zru",0x01)'
C='cdef("_cleanup2","SetMon","zru",0x01])'
spec = Spec.Spec("f3.chess.cornell.edu:xrf", 500)
anycmd=SpecCommand.SpecCommandA('p','f3.chess.cornell.edu:xrf')
anycmd("connected")
anycmd.executeCommand(SetDef)
anycmd.executeCommand(MonDef)
anycmd.executeCommand(A)
anycmd.executeCommand(B)
anycmd.executeCommand(C)





##cdef("name", string [, "key" [, flags ]])
##    Defines parts of chained macros. A chained macro definition is maintained in pieces that can be selectively included to form the complete macro definition. The argument name is the name of the macro. The argument string contains a piece to add to the macro.
##
##    The chained macro can have three parts: a beginning, a middle and an end. Pieces included in each of the parts of the macros are sorted lexicographically by the keys when putting together the macro definition. Pieces without a key are placed in the middle in the order in which they were added, but after any middle pieces that include a key.
##
##    The key argument allows a piece to be selectively replaced or deleted, and also controls the order in which the piece is placed into the macro definition. The flags argument controls whether the pieces are added to the beginning or to the end of the macro, and also whether the pieces should be selectively included in the definition depending on whether key is the mnemonic of a configured motor or counter.
##
##    The bit meanings for flags are as follows:
##
##    0x01 - only include if key is a motor mnemonic
##    0x02 - only include if key is a counter mnemonic
##    0x10 - place in the beginning part of the macro
##    0x20 - place in the end part of the macro
##
##    If flag is the string "delete", the piece associated with key is deleted from the table. If the name is the null string, the piece associated with key is deleted from all the chained macros. If key is the null string, the flags have no effect.
##
##    The cdef() function will remove any existing macro defined using def or rdef. However, the commands lsdef, prdef and undef will function with chained macros.
##
##    When spec starts and when the reconfig command is run (or the config macro is invoked), all the chained macros are adjusted for the currently configured motors and counters.


    
