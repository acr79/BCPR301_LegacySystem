from abc import ABCMeta, abstractmethod


class AbstractObjectInfo(metaclass=ABCMeta):

    @abstractmethod
    def getAsString(self):
        pass

    @abstractmethod
    def getFunctionDesc(self):
        pass

    @abstractmethod
    def getClassObject(self):
        pass
