import cmd
import sys
from Controller import Controller
from View import View
from RecordCollection import RecordCollection
from Record import Record

#
viewTest = View()

def serialLoad(arg):
    report = ""
    import pickle
    x = None
    try:
        with open(arg, 'rb') as f:
            x = pickle.load(f)
    except IOError as e:
        report = "Failed to do serial load: {}\n".format(str(e))
    except AttributeError as e:
        report += "Failed to do serial load: {}\n".format(str(e))
    if isinstance(x, RecordCollection):
        report += "Serial load of record collection successful\n"
        return (x, report)
    else:
        return (None, report)


if __name__ == "__main__":
    report = ""
    existingColl = None
    for a in sys.argv:
        if a.upper()[0:5] == "COLL:":
            existingColl, report = serialLoad(a[5:])
    Controller(View(report), existingColl).cmdloop()
