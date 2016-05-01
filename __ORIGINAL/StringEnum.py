from CustomException import CustomException
from GlobalMethod import typeCheckStringERR


class EnumException(CustomException):

    def __init__(self, theReason="Enum not Committed"):
        super(EnumException, self).__init__(theReason)


class StringEnum(object):

    def __init__(self):
        self._values = {}
        self._default = None
        self._committed = False

    def addValue(self, newString):
        typeCheckStringERR(newString)
        if (not self._committed) and (newString.upper() not in self._values):
            self._values[newString.upper()] = newString

    def commit(self, default):
        typeCheckStringERR(default)
        if (not self._committed) and (default.upper() in self._values):
            self._committed = True
            self._default = self._values[default.upper()]

    def getValue(self, key):
        typeCheckStringERR(key)
        if not self._committed:
            raise EnumException()
        if key.upper() in self._values:
            return self._values[key.upper()]
        else:
            return self._default

    def hasKey(self, key):
        typeCheckStringERR(key)
        if key.upper() in self._values:
            return True
        else:
            return False
