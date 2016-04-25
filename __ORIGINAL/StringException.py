from CustomException import CustomException

class StringException(CustomException):

    def __init__(self, theReason="Supplied Variable is not a String"):
        super(StringException, self).__init__(theReason)