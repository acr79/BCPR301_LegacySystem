class LimitedInt(object):

    def __init__(self, lowLimit, highLimit):
        self._low = int(min(lowLimit, highLimit))
        self._high = int(max(lowLimit, highLimit))
        self._value = self._low

    def set(self, newValue):
        trial = None
        if isinstance(newValue, int):
            trial = newValue
        elif isinstance(newValue, str):
            try:
                trial = int(newValue)
            except ValueError:
                pass
        if trial is not None and (self._low <= trial <= self._high):
            self._value = trial

    def get(self):
        return self._value
