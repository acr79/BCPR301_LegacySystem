import cmd
import sys
from Controller import Controller
from AbstractView import AbstractView
from View import View
from RecordCollection import RecordCollection
from Record import Record


def serialLoad(arg):
    report = ""
    import pickle
    x = None
    try:
        with open(arg, 'rb') as f:
            x = pickle.load(f)
    except IOError as e:
        report = "Failed to do serial load: {}".format(str(e))
    except AttributeError as e:
        report = "Failed to do serial load: {}".format(str(e))
    else:
        if isinstance(x, RecordCollection):
            report = "Serial load of record collection successful"
        else:
            x = None
            report = "Failed to do serial load: No instance of record \
collection"
    return (x, report)


def viewImport(arg):
    report = ""
    x = None
    try:
        viewMod = __import__(arg)
        x = viewMod.getViewClass()
        if issubclass(x, AbstractView):
            report = "Loading of View class successful"
        else:
            x = None
            raise TypeError("Class does not implement AbstractView")
    except ImportError as e:
        report = "Failed to load specific View module: {}".format(str(e))
    except AttributeError as e:
        report = "Failed to load specific View module: {}".format(str(e))
    except TypeError as e:
        report = "Failed to load AbstractView implementation: {}\
".format(str(e))
    return (x, report)


def main(run, arguments):
    global theController
    ViewClass = None
    theReports = []
    existingColl = None
    for a in arguments:
        if a.upper()[0:5] == "COLL:":
            existingColl, report = serialLoad(a[5:])
            theReports.append(report)
        elif a.upper()[0:5] == "VIEW:":
            ViewClass, report = viewImport(a[5:])
            theReports.append(report)
    if ViewClass is None:
        ViewClass = View
    theView = ViewClass()
    for aReport in theReports:
        theView.show(aReport)
    theController = Controller(theView, existingColl)
    if run:
        theController.cmdloop()

theController = None

if __name__ == "__main__":
    main(True, sys.argv[1:])
