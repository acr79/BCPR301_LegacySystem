from Record import Record
from RecordCollection import Record

from abc import ABCMeta, abstractmethod

class AbstractCont(metaclass=ABCMeta):
    @abstractmethod
    def report(self, content):
        pass

    @abstractmethod
    def getRecordCollection(self):
        pass

    @abstractmethod
    def getAllRecords(self):
        pass

    @abstractmethod
    def addRecordData(self, data):
        pass


class Filer(object):
    """
    Filer dedicated for the needs of ERP
    """

    def serialLoad(self, strRef, aCont):
        report = ""
        import pickle
        x = None
        try:
            with open(strRef, 'rb') as f:
                x = pickle.load(f)
        except IOError as e:
            aCont.report("Failed to do serial load: {}\n".format(str(e)))
        except AttributeError as e:
            aCont.report("Failed to do serial load: {}\n".format(str(e)))
        if isinstance(x, RecordCollection):
            aCont.report("Serial load of record collection successful\n")
            return x
        else:
            return None

    def serialSave(self, strRef, aCont):
        import pickle
        import os
        if not os.path.isfile(strRef):  # protection from overwriting files
            try:
                with open(strRef, 'wb') as f:
                    pickle.dump(aCont.getRecordCollection(), f)
            except IOError as e:
                aCont.report("EXCEPTION: {}\n".format(str(e)))
        else:
            aCont.report("Will not overwrite an existing file\n\
Please, enter a new file when using serial_save\n")

    def textLoad(self, strRef, aCont):
        try:
            theFile = open(strRef, 'r')
            theLines = theFile.readlines()
            theFile.close()
            added = 0
            for i in range(len(theLines)):
                data = ""
                if 0 < len(theLines[i]) and theLines[i][-1] == '\n':
                    data = theLines[i][0:-1]
                else:
                    data = theLines[i]
                try:
                    aCont.addRecordData(data)
                except CustomException as e:
                    aCont.report("BAD LINE {}: {}\n".format(i + 1, str(e)))
                else:
                    added += 1
        except IOError as e:
            aCont.report("EXCEPTION: {}\n".format(str(e)))
        else:
            aCont.report("Records Added: {}\nProblems: \n{}\n\
".format(added, report))


    def textSave(self, strRef, aCont):
        import os
        if not os.path.isfile(arg):
            try:
                theFile = open(arg, 'w')
                theLines = []
                allRecords = aCont.getAllRecords()
                total = len(allRecords)
                for i in range(total):
                    r = allRecords[i]
                    asStr = "{} {} {} {} {} {}".format(r.getID(),
                                                       r.getGender(),
                                                       r.getAge(),
                                                       r.getSales(),
                                                       r.getBMI(),
                                                       r.getIncome())
                    if i < (total - 1):
                        asStr += "\n"
                    theLines.append(asStr)
                theFile.writelines(theLines)
                theFile.close()
            except IOError as e:
                aCont.report("EXCEPTION: {}\n".format(str(e)))
            else:
                aCont.report("Saved As Text")
            
            # D self._stall()
        else:
            aCont.report("Will not overwrite an existing file\n\
Please, enter a new file when using serial_save\n")
