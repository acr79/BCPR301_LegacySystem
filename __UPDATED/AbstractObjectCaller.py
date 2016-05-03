from abc import ABCMeta, abstractmethod


class AbstractObjectCaller(metaclass=ABCMeta):

    @abstractmethod
    def setObject(self, theObject):
        pass

    @abstractmethod
    def callObject(self):
        pass
