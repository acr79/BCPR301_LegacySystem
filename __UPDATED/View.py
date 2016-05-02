from AbstractView import AbstractView


def getViewClass():
    return View


class DudViewPlot(object):

    def bar(self, *args):
        pass

    def pie(self, *args):
        pass

    def show(self, *args):
        pass


try:
    import matplotlib.pyplot as viewPlot
except ImportError:
    viewPlot = DudViewPlot()


class View(AbstractView):

    def __init__(self):
        self._viewPlot = globals()["viewPlot"]

    def show(self, message):
        if message is not None:
            print(message)

    def barChart(self, labels, values):
        self._viewPlot.bar(range(len(labels)), values)
        self._viewPlot.show()

    def pieChart(self, data):
        if isinstance(data, list):
            theLabels = []
            theValues = []
            for d in data:
                if isinstance(d, tuple) and len(d) == 2:
                    l, v = d
                    theLabels.append(l)
                    theValues.append(v)
            self._viewPlot.pie(theValues, labels=theLabels)
            self._viewPlot.show()
