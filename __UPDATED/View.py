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


class View(object):

    def __init__(self, message=None):
        if message is not None:
            print(message)

    def show(self, message):
        print(message)

    def stall(self):
        input("- Enter to continue -")

    def barChart(self, labels, values):

        viewPlot.bar(range(len(labels)), values)
        viewPlot.show()

    def pieChart(self, data):
        if isinstance(data, list):
            theLabels = []
            theValues = []
            for d in data:
                if isinstance(d, tuple) and len(d) == 2:
                    l, v = d
                    theLabels.append(l)
                    theValues.append(v)
            viewPlot.pie(theValues, labels=theLabels)
            viewPlot.show()
