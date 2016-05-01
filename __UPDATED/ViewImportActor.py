from AbstractActor import AbstractActor
from AbstractView import AbstractView


class ViewImportActor(AbstractActor):

    def __init__(self):
        self._viewClass = None

    def getImportedViewClass(self):
        return self._viewClass

    def doAction(self, strData):
        report = ""
        self._viewClass = None
        try:
            viewMod = __import__(strData)
            self._viewClass = viewMod.getViewClass()
            if issubclass(self._viewClass, AbstractView):
                print("OK")
                report = "Loading of View class successful"
            else:
                self._viewClass = None
                raise TypeError("Class does not implement AbstractView")
        except ImportError as e:
            report = "Failed to load specific View module: {}".format(str(e))
        except AttributeError as e:
            report = "Failed to load specific View module: {}".format(str(e))
        except TypeError as e:
            report = "Failed to load AbstractView implementation: {}\
".format(str(e))
        return report
