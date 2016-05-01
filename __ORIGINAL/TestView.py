"""
Not a test case
"""
from AbstractView import AbstractView


def getViewClass():
    return TestView


theLog = []


def clearLog():
    global theLog
    theLog = []


class TestView(AbstractView):

    def show(self, message):
        global theLog
        theLog.append(message)

    def barChart(self, *args):
        pass

    def pieChart(self, *args):
        pass
