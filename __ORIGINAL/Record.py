from CustomException import CustomException
from StringEnum import StringEnum
from GlobalMethod import typeCheckStringERR


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
        self._age = 0
        self._sales = 0
        self._bmi = Record._enumBMI.getValue("")  # default
        self._income = 0

    def setAge(self, newAge):
        trial = None
        if isinstance(newAge, int):
            trial = newAge
        elif isinstance(newAge, str):
            try:
                trial = int(newAge)
            except ValueError:
                pass
        if trial is not None and (0 <= trial <= 99):
            self._age = trial

    def setSales(self, newSales):
        trial = None
        if isinstance(newSales, int):
            trial = newSales
        elif isinstance(newSales, str):
            try:
                trial = int(newSales)
            except ValueError:
                pass
        if trial is not None and (0 <= trial <= 999):
            self._sales = trial

    def setBMI(self, newBMI):
        if isinstance(newBMI, str) and (Record._enumBMI.hasKey(newBMI)):
            self._bmi = Record._enumBMI.getValue(newBMI)

    def setIncome(self, newIncome):
        trial = None
        if isinstance(newIncome, int):
            trial = newIncome
        elif isinstance(newIncome, str):
            try:
                trial = int(newIncome)
            except ValueError:
                pass
        if trial is not None and (0 <= trial <= 999):
            self._income = trial

    def getID(self):
        return self._id

    def getGender(self):
        return self._gender

    def getAge(self):
        return self._age

    def getSales(self):
        return self._sales

    def getBMI(self):
        return self._bmi

    def getIncome(self):
        return self._income
