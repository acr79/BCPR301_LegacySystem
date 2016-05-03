from AbstractObjectInfo import AbstractObjectInfo
from Record import Record
from CustomException import CustomException


class RecordObjectInfo(AbstractObjectInfo):

    def __init__(self, newRecord, functionDesc):
        if not isinstance(newRecord, Record):
            raise CustomException("Not a Record object")
        self._record = newRecord
        self._funcStr = functionDesc

    def getAsString(self):
        return "ID: {}\nGENDER: {}\nAGE: {}\nSALES: {}\nBMI: {}\nINCOME: \
{}\n".format(self._record.getID(), self._record.getGender(),
             self._record.getAge(), self._record.getSales(),
             self._record.getBMI(), self._record.getIncome())

    def getFunctionDesc(self):
        return self._funcStr

    def getClassObject(self):
        return self._record
