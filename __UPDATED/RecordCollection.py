from CustomException import CustomException
from GlobalMethod import typeCheckStringERR
from Record import Record


class InvalidIDException(CustomException):

    def __init__(self, theReason="Invalid ID"):
        super(InvalidIDException, self).__init__(theReason)


class DuplicateIDException(CustomException):

    def __init__(self, theReason="ID Already Taken"):
        super(DuplicateIDException, self).__init__(theReason)


class MaxRecordsException(CustomException):

    def __init__(self, theReason="ERP has the Maximum Amount of Records"):
        super(MaxRecordsException, self).__init__(theReason)


class RecordCollection(object):

    _letters = []
    _letters[:] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _numerals = []
    _numerals[:] = "0123456789"

    def __init__(self):
        self._allMyRecords = []

    def _prepID(self, theID):
        typeCheckStringERR(theID)
        if len(theID) != 4:
            raise InvalidIDException()
        prep = theID.upper()
        if prep[0] not in RecordCollection._letters:
            raise InvalidIDException()
        for x in range(1, 4):
            if prep[x] not in RecordCollection._numerals:
                raise InvalidIDException()
        return prep

    def _prot_findRecord(self, theID):
        if len(self._allMyRecords) == 0:
            return (None, 0)
        else:
            low = 0
            high = len(self._allMyRecords)
            i = int(high / 2)
            while low != high:
                record = self._allMyRecords[i]
                if theID < record.getID():
                    high = i
                elif record.getID() < theID:
                    if low == i:
                        low += 1
                    else:
                        low = i
                else:  # match found
                    return (record, i)
                i = int((high + low) / 2)
            return (None, i)  # (no match, index for prospect ID)

    def _autoID(self):
        theLength = len(self._allMyRecords)
        if 26000 <= theLength:
            raise MaxRecordsException()
        i = 0
        ch = 0
        while ch < len(RecordCollection._letters):
            n = 1000
            while n < 2000:
                trial = RecordCollection._letters[ch] + str(n)[1:4]
                if theLength == i:
                    return (trial, i)
                elif self._allMyRecords[i].getID() != trial:
                    return (trial, i)
                i += 1
                n += 1
            ch += 1

    # SMELL? Long Method
    # SMELL? Long Parameter List
    # Initial ideas:
    # # Use replace parameter with method call,
    # #  which might need an interface defined in this module
    # # Use replace method with method object
    def addRecord(self, newID, newGender, newAge, newSales, newBMI, newIncome,
                  autoID, overwrite):
        typeCheckStringERR(newID)
        preppedID = None
        invalidID = False
        origRec = None
        insertPos = None
        overwriteSignal = 0  # will become 1 if overwriting will be used
        try:
            preppedID = self._prepID(newID)
            origRec, insertPos = self._prot_findRecord(preppedID)
        except InvalidIDException:
            invalidID = True
        if origRec is not None and overwrite:
            overwriteSignal = 1
        elif (origRec is not None or invalidID) and autoID:
            preppedID, insertPos = self._autoID()
            # doNotUse, insertPos = self._prot_findRecord(preppedID)
        elif origRec is not None:
            raise DuplicateIDException()
        elif invalidID:
            raise InvalidIDException()
        newRec = Record(preppedID, newGender)
        self._allMyRecords[insertPos:insertPos + overwriteSignal] = [newRec]
        newRec.setAge(newAge)
        newRec.setSales(newSales)
        newRec.setBMI(newBMI)
        newRec.setIncome(newIncome)

    def getRecord(self, theID):
        try:
            trial = self._prepID(theID)
            rec, p = self._prot_findRecord(trial)
            return rec
        except InvalidIDException:
            return None

    def getAllRecords(self):
        return self._allMyRecords

    def clearRecords(self):
        self._allMyRecords = []

    def deleteRecord(self, theID):
        preppedID = self._prepID(theID)
        origRec, pos = self._prot_findRecord(preppedID)
        if origRec is not None:
            del self._allMyRecords[pos]
            return True
        else:
            return False
