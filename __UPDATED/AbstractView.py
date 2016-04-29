from abc import ABCMeta, abstractmethod

class AbstractView(metaclass=ABCMeta):

    @abstractmethod
    def show(self, message):
        pass

    @abstractmethod
    def stall(self):
        pass

    @abstractmethod
    def barChart(self, labels, values):
        pass

    @abstractmethod
    def pieChart(self, data):
        pass