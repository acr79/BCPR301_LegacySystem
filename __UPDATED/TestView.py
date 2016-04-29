"""
Not a test case
"""

def getViewClass():
    return TestView

from AbstractView import AbstractView

theLog = []
theStalls = 0


def clearLog():
    global theLog
    theLog = []

def clearStalls():
    global theStalls
    theStalls = 0

class TestView(AbstractView):

    def show(self, message):
        global theLog
        theLog.append(message)

    def stall(self):
        global theStalls
        theStalls += 1

    def barChart(self, *args):
        pass

    def pieChart(self, *args):
        pass
