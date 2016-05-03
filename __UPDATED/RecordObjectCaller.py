from AbstractObjectCaller import AbstractObjectCaller
from Record import Record
from CustomException import CustomException


class RecordObjectCaller(AbstractObjectCaller):

    def __init__(self, newData):
        self._record = None
        self._newData = newData

    def setObject(self, theObject):
        if not isinstance(theObject, Record):
            raise CustomException()
        self._record = theObject

    def callObject(self):
        if self._record is None:
            raise CustomException()


class ROC_SetAge(RecordObjectCaller):

    def callObject(self):
        super().callObject()
        self._record.setAge(self._newData)


class ROC_SetSales(RecordObjectCaller):

    def callObject(self):
        super().callObject()
        self._record.setSales(self._newData)


class ROC_SetBMI(RecordObjectCaller):

    def callObject(self):
        super().callObject()
        self._record.setBMI(self._newData)


class ROC_SetIncome(RecordObjectCaller):

    def callObject(self):
        super().callObject()
        self._record.setIncome(self._newData)
