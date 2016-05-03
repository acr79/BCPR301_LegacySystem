import sys
import unittest

thePaths = sys.argv[:1]
for path in thePaths:
    sys.path.append(path)

from UT_AffectedFunctions import TestAffectedFunctionsClass
from UT_FilerFunctionality import TestFilerFunctionClass
from UT_ObjectSelection import TestObjectSelectionClass
from UT_Record import TestRecordClass

sys.argv = sys.argv[:1]


def getSuite():
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(TestAffectedFunctionsClass))
    theSuite.addTest(unittest.makeSuite(TestFilerFunctionClass))
    theSuite.addTest(unittest.makeSuite(TestObjectSelectionClass))
    theSuite.addTest(unittest.makeSuite(TestRecordClass))
    return theSuite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    theSuite = getSuite()
    runner.run(theSuite)
