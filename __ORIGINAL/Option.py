class Option(object):

    def __init__(self, newName, newOnDesc, newOffDesc):
        self._name = newName
        self._onDescription = newOnDesc
        self._offDescription = newOffDesc
        self._on = False

    def isOn(self):
        return self._on

    def turnOn(self):
        self._on = True

    def turnOff(self):
        self._on = False

    def getName(self):
        return self._name

    def getOnDescription(self):
        return self._onDescription

    def getOffDescription(self):
        return self._offDescription
