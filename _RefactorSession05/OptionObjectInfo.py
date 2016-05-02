from AbstractObjectInfo import AbstractObjectInfo
from Option import Option
from CustomException import CustomException


class OptionObjectInfo(AbstractObjectInfo):

    def __init__(self, newOption, functionDesc):
        if not isinstance(self, newOption):
            raise customException("Not an Option object")
        self._option = newOption
        self._funcStr = functionDesc

    def getAsString(self):
        state = "OFF"
        if self._option.isOn():
            state = "ON"
        return "{}: TURNED {}\n. . .\nON: {}\nOFF: {}\n\n\
".format(self._option.getName(), state, self._option.getOnDescription(),
         self._option.getOffDescription())

    def getFunctionDesc(self):
        return self._funcStr

    def getClassObject(self):
        return self._option
