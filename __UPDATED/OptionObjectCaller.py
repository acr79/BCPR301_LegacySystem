from AbstractObjectCaller import AbstractObjectCaller
from Option import Option
from CustomException import CustomException


class OptionObjectCaller(AbstractObjectCaller):

    def __init__(self):
        self._option = None

    def setObject(self, theObject):
        if not isinstance(theObject, Option):
            raise CustomException()
        self._option = theObject

    def callObject(self):
        if self._option is None:
            raise CustomException()


class OOC_TurnOn(OptionObjectCaller):

    def callObject(self):
        super().callObject()
        self._option.turnOn()


class OOC_TurnOff(OptionObjectCaller):

    def callObject(self):
        super().callObject()
        self._option.turnOff()
