#
# Exception class
#
class SpecClientError(Exception):
    def __init__(self, error = None, err = None):
        Exception.__init__(self)

        self.error = error
        self.err = err


    def __str__(self):
        return (self.error is not None and str(self.error) or '') + (self.err is not None and ' (%s)' % str(self.err) or '')


class SpecClientTimeoutError(SpecClientError):
    pass


class SpecClientNotConnectedError(SpecClientError):
    pass
