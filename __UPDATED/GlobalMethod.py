from CustomException import CustomException
from StringException import StringException


def typeCheckStringERR(*trials):
    for t in trials:
        if not (isinstance(t, str)):
            raise StringException()


def safeInt(trial, default):
    result = 0
    if isinstance(default, int):
        result = default
    try:
        result = int(trial)
    except ValueError:
        pass
    return result