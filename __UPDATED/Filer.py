import pickle
import os
from RecordCollection import RecordCollection
from AbstractController import AbstractController
from CustomException import CustomException


class Filer(object):
    """
    Filer dedicated for the needs of ERP
    """

    def _checkACont(self, aCont):
        if not isinstance(aCont, AbstractController):
            raise CustomException("No AbstractController stated")

    def serialSave(self, strRef, aCont):
        self._checkACont(aCont)
        if not os.path.isfile(strRef):  # protection from overwriting files
            try:
                theFile = open(strRef, 'wb')
                pickle.dump(aCont.getRecordCollection(), theFile)
                theFile.close()
            except IOError as e:
                aCont.show("EXCEPTION: {}\n".format(str(e)))
        else:
            aCont.show("Will not overwrite an existing file\nPlease, enter a \
new file when using serial_save\n")

    def textLoad(self, strRef, aCont):
        self._checkACont(aCont)
        problems = ""
        try:
            theFile = open(strRef, 'r')
            theLines = theFile.readlines()
            theFile.close()
            added = 0
            report = ""
            for i in range(len(theLines)):
                data = ""
                if 0 < len(theLines[i]) and theLines[i][-1] == '\n':
                    data = theLines[i][0:-1]
                else:
                    data = theLines[i]
                try:
                    aCont.addRecordData(data)
                except CustomException as e:
                    problems += "BAD LINE {}: {}\n".format(i + 1, str(e))
                else:
                    added += 1
        except IOError as e:
            aCont.show("EXCEPTION: {}\n".format(str(e)))
        else:
            aCont.show("Records Added: {}\nProblems: \n{}\n\
".format(added, problems))

    def textSave(self, strRef, aCont):
        self._checkACont(aCont)
        if not os.path.isfile(strRef):
            try:
                theFile = open(strRef, 'w')
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
                aCont.show("EXCEPTION: {}\n".format(str(e)))
            else:
                aCont.show("Saved As Text")
        else:
            aCont.show("Will not overwrite an existing file\nPlease, enter a \
new file when using text_save\n")
