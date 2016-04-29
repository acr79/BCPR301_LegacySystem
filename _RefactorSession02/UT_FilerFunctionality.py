import sys
import io
from io import StringIO
from io import BytesIO
import unittest
from unittest.mock import Mock
from unittest.mock import patch
import os
from os.path import isfile
import builtins
import pickle

thePaths = sys.argv[1:]
for path in thePaths:
    sys.path.append(path)

sys.argv = sys.argv[:1]

import RunMain
import TestView
from RecordCollection import RecordCollection


class TestFilerFunctionClass(unittest.TestCase):

    def _addSomeRecords(self, theRC, number):
        # auto id, default attrs
        for x in range(number):
            theRC.addRecord("", "m", None, None, None, None, True, False)

    @patch('builtins.open')
    def test_SerialLoad_01(self, mockMeth):
        """
        Can only load an instance of RecordCollection
        - Reject other class object
        """
        TestView.clearLog()
        object = set()
        thePickle = BytesIO()
        pickle.dump(object, thePickle)
        theDump = thePickle.getvalue()

        # builtins.open
        mockMeth.return_value = BytesIO(theDump)

        # Set up Controller via RunMain module
        # order important for list of string-codes
        # "coll:" triggers serial load
        # "view:TestView" will store uses of TestView() to TestView.py module
        RunMain.main(False, ["coll:", "view:TestView"])
        expectedShow = "Failed to do serial load: No instance of record \
collection"
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('builtins.open')
    def test_TextLoad_01(self, mockMeth):
        """
        Load some records from text
        """
        expID = "A001"
        expGender = "F"
        expAge = 36
        expSales = 92
        expBMI = "Normal"
        expIncome = 700
        theData = "{} {} {} {} {} {}".format(expID, expGender, expAge,
expSales, expBMI, expIncome)
        # theData = "A001 F 36 92 Normal 700"

        # builtins.open return value
        mockMeth.return_value = StringIO(theData)

        # Set up Controller via RunMain module
        RunMain.main(False, ["view:TestView"])
        theController = RunMain.theController
        theController.do_text_load("")
        theController.do_select_rec("a001")
        theRec = theController._selectedRecord
        self.assertEqual(expID, theRec.getID())
        self.assertEqual(expGender, theRec.getGender())
        self.assertEqual(expAge, theRec.getAge())
        self.assertEqual(expSales, theRec.getSales())
        self.assertEqual(expBMI, theRec.getBMI())
        self.assertEqual(expIncome, theRec.getIncome())

    @patch('builtins.open')
    @patch('os.path.isfile')
    def test_SerialSave_01(self, mock_isfile, mock_open):
        """
        Saving a RecordCollection with 10 Records
        """
        def doDump():
            doDump.theDump = theDumpStream.getvalue()

        theDumpStream = BytesIO()
        theDumpStream.close = Mock(side_effect=doDump)
        
        # So that it is know that file does not exist
        mock_isfile.return_value = False
        mock_open.return_value = theDumpStream
        # Set up Controller via RunMain module
        RunMain.main(False, ["view:TestView"])
        theController = RunMain.theController
        # add 10 Records, reset view log, then serial save
        self._addSomeRecords(theController._theColl, 10)
        TestView.clearLog()
        theController.do_serial_save("")

        # Part 1: Check contents of theDumpStream
        # theDump = theDumpStream.getvalue()
        expectedRecords = 10
        fromDump = pickle.load(BytesIO(doDump.theDump))
        actualRecords = len(fromDump.getAllRecords())
        self.assertEqual(expectedRecords, actualRecords)

        # Part 2: Check no show() messages on theLog
        expectedLog = 0
        actualLog = len(TestView.theLog)
        self.assertEqual(expectedLog, actualLog)


if __name__ == "__main__":
    unittest.main()
        