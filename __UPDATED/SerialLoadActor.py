import pickle
from AbstractActor import AbstractActor
from RecordCollection import RecordCollection


class SerialLoadActor(AbstractActor):

    def __init__(self):
        self._loadedRC = None

    def getLoadedRecordCollection(self):
        return self._loadedRC

    def doAction(self, strData):
        report = ""
        self._loadedRC = None
        try:
            with open(strData, 'rb') as f:
                self._loadedRC = pickle.load(f)
        except IOError as e:
            report = "Failed to do serial load: {}".format(str(e))
        except AttributeError as e:
            report = "Failed to do serial load: {}".format(str(e))
        else:
            if isinstance(self._loadedRC, RecordCollection):
                report = "Serial load of record collection successful"
            else:
                self._loadedRC = None
                report = "Failed to do serial load: No instance of record \
collection"
        return report
