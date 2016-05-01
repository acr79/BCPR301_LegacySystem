from abc import ABCMeta, abstractmethod


class AbstractController(metaclass=ABCMeta):

    @abstractmethod
    def getRecordCollection(self):
        pass

    @abstractmethod
    def getAllRecords(self):
        pass

    @abstractmethod
    def addRecordData(self, data):
        pass

    @abstractmethod
    def show(self, message):
        pass
