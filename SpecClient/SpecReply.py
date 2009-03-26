#$Id: SpecReply.py,v 1.1 2004/08/23 11:16:09 guijarro Exp $
"""SpecReply module

This module defines the SpecReply class
"""

__author__ = 'Matias Guijarro'
__version__ = '1.0'

import SpecEventsDispatcher

REPLY_ID_LIMIT = 2**30
current_id = 0


def getNextReplyId():
    global current_id
    current_id = (current_id + 1) % REPLY_ID_LIMIT
    return current_id


class SpecReply:
    """SpecReply class

    Represent a reply received from a remote Spec server

    Signals:
    replyFromSpec(self) -- emitted on update
    """
    def __init__(self):
        """Constructor."""
        self.data = None
        self.error = False
        self.error_code = 0 #no error
        self.id = getNextReplyId()


    def update(self, data, error, error_code):
        """Emit the 'replyFromSpec' signal."""
        self.data = data
        self.error = error
        self.error_code = error_code

        SpecEventsDispatcher.emit(self, 'replyFromSpec', (self, ))


    def getValue(self):
        """Return the value of the reply object (data field)."""
        return self.data
