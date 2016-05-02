class CustomException(Exception):

    def __init__(self, theReason=""):
        self._reason = theReason

    def __str__(self):
        return repr(self._reason)

    def getReason(self):
        return self._reason
