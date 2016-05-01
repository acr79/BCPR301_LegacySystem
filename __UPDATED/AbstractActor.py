from abc import ABCMeta, abstractmethod


class AbstractActor(metaclass=ABCMeta):

    @abstractmethod
    def doAction(self, strData):
        pass
