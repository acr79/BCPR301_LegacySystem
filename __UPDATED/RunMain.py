import cmd
import sys
from Controller import Controller
from AbstractView import AbstractView
from View import View
from RecordCollection import RecordCollection
from AbstractActor import AbstractActor
from SerialLoadActor import SerialLoadActor
from ViewImportActor import ViewImportActor


class Initialiser(object):

    def __init__(self):
        self._actionMap = {}
        self._theSerialLoad = SerialLoadActor()
        self._theViewImport = ViewImportActor()
        self._actionMap["COLL"] = self._theSerialLoad
        self._actionMap["VIEW"] = self._theViewImport

    def getController(self, arguments):
        theReports = []
        for arg in arguments:
            if ":" in arg:
                cut = arg.index(":")
                prefix = arg[0:cut].upper()
                strData = arg[(cut + 1):]
                if prefix in self._actionMap:
                    report = self._actionMap[prefix].doAction(strData)
                    theReports.append(report)
        # can be None
        theRecordCollection = self._theSerialLoad.getLoadedRecordCollection()
        # instantiate an AbstractView implementer
        ViewClass = self._theViewImport.getImportedViewClass()
        if ViewClass is None:
            ViewClass = View
        theView = ViewClass()
        for rep in theReports:
            theView.show(rep)
        # construct Controller
        return Controller(theView, theRecordCollection)


# globals
theInit = Initialiser()
theController = None


def main(startController, arguments):
    global theInit
    global theController
    theController = theInit.getController(arguments)
    if startController:
        theController.cmdloop()

if __name__ == "__main__":
    main(True, sys.argv[1:])
