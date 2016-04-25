# UPDATE: REFACTORED (0425)

from CustomException import CustomException
from StringEnum import StringEnum
from GlobalMethod import typeCheckStringERR
from LimitedInt import LimitedInt

class InvalidGenderException(CustomException):

    def __init__(self, theReason="Invalid Gender"):
        super(InvalidGenderException, self).__init__(theReason)

# SMELL: Duplicate Code
# SMELL? Primitive Obsession
# # setAge()
# # setSales()
# # setIncome()
# These methods practically have the same behaviour pattern
# Initial idea: Create a class for the stylised int attribute,
#  so (in this version) Record would have three instances
# # _age : SpecialInt
# # _sales : SpecialInt
# # _income : SpecialInt

class Record(object):

    _enumBMI = StringEnum()
    _enumBMI.addValue("Normal")
    _enumBMI.addValue("Overweight")
    _enumBMI.addValue("Obesity")
    _enumBMI.addValue("Underweight")
    _enumBMI.commit("Normal")

    def __init__(self, newID, newGender):
        typeCheckStringERR(newGender)
        gender = newGender.upper()
        if (gender != "M" and gender != "F"):
            raise InvalidGenderException()
        self._id = newID
        self._gender = gender
        self._age = LimitedInt(0, 99)
        self._sales = LimitedInt(0, 999)
        self._bmi = Record._enumBMI.getValue("")  # default
        self._income = LimitedInt(0, 999)

    def setAge(self, newAge):
        self._age.set(newAge)

    def setSales(self, newSales):
        self._sales.set(newSales)

    def setBMI(self, newBMI):
        if isinstance(newBMI, str) and (Record._enumBMI.hasKey(newBMI)):
            self._bmi = Record._enumBMI.getValue(newBMI)

    def setIncome(self, newIncome):
        self._income.set(newIncome)

    def getID(self):
        return self._id

    def getGender(self):
        return self._gender

    def getAge(self):
        return self._age.get()

    def getSales(self):
        return self._sales.get()

    def getBMI(self):
        return self._bmi

    def getIncome(self):
        return self._income.get()
