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
import random

thePaths = sys.argv[1:]
for path in thePaths:
    sys.path.append(path)

sys.argv = sys.argv[:1]

import RunMain
import TestView
from Controller import Controller
from RecordCollection import RecordCollection


class TestFilerFunctionClass(unittest.TestCase):

    def _addSomeRecords(self, theRC, number):
        # auto id, default attrs
        for x in range(number):
            theRC.addRecord("", "m", None, None, None, None, True, False)

    def _addSomeRecordsViaController(self, theCont, number):
        # auto id, default attrs
        theCont.do_select_option("AUTOID")
        theCont.do_on("")
        for x in range(number):
            theCont.do_add_rec(" m    ")

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
    def test_SerialLoad_02(self, mockMeth):
        """
        Handles IOError
        - Because the IOError message is expected to be determined by the
           IOError constructor, the message will be randomised
        """
        message = str(random.randrange(100))
        TestView.clearLog()
        mockMeth.side_effect = IOError(message)
        RunMain.main(False, ["coll:", "view:TestView"])
        expectedShow = "Failed to do serial load: {}".format(message)
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('pickle.load')
    @patch('builtins.open')
    def test_SerialLoad_03(self, mock_open, mock_load):
        """
        Handles AtrributeError
        - Because the AttributeError message is expected to be determined by
           the AttributeError constructor, the message will be randomised
        """
        message = str(random.randrange(100))
        TestView.clearLog()

        # mockMeth.return_value = BytesIO(b'\x80\x03c__main__\nUnfamiliar\nq\x00)\x81q\x01.')
        mock_open.return_value = BytesIO()
        mock_load.side_effect = AttributeError(message)

        RunMain.main(False, ["coll:", "view:TestView"])
        expectedShow = "Failed to do serial load: {}".format(message)
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('builtins.open')
    def test_SerialLoad_04(self, mockMeth):
        """
        Successful loading of RecordCollection
        - Because Controller will end up with an instance of RecordCollection
           regardless of the outcome of a serial load, the object loaded will
           come with 10 Records
        """
        theRC = RecordCollection()
        self._addSomeRecords(theRC, 10)
        theDumpStream = BytesIO()
        pickle.dump(theRC, theDumpStream)
        theDump = theDumpStream.getvalue()
        mockMeth.return_value = BytesIO(theDump)

        TestView.clearLog()
        RunMain.main(False, ["coll:", "view:TestView"])
        expected_1 = "Serial load of record collection successful"
        expected_2 = "Records in ERP: 10"
        self.assertEqual(expected_1, TestView.theLog[0])
        TestView.clearLog()
        RunMain.theController.do_neutral("")
        self.assertEqual(expected_2, TestView.theLog[0])

    @patch('builtins.open')
    def test_TextLoad_01(self, mockMeth):
        """
        Load a record from text, test for correct attribute parsing
        - This test does not add coverage if test_TextLoad_02 is exercised
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

        mockMeth.return_value = StringIO(theData)

        theController = Controller(TestView.TestView(), None)
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
    def test_TextLoad_02(self, mockMeth):
        """
        Can handle bad lines in text load
        - Line 2 in textData (between \n\n) is bad as nothing can be
           interpreted
        - Also 2 records will be added
        """
        textData = "a001 f 36 92 normal 700\n\nb222 m 1 1 normal 9"
        mockMeth.return_value = StringIO(textData)
        theController = Controller(TestView.TestView(), None)

        TestView.clearLog()
        theController.do_text_load("")
        expectedShow = "Records Added: 2\nProblems: \nBAD LINE 2: 'Not Enough \
Arguments Provided'\n\n"
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('builtins.open')
    def test_TextLoad_03(self, mockMeth):
        """
        Handles IOError
        - Because the IOError message is expected to be determined by the
           IOError constructor, the message will be randomised
        """
        message = str(random.randrange(100))
        mockMeth.side_effect = IOError(message)
        theController = Controller(TestView.TestView(), None)

        TestView.clearLog()
        theController.do_text_load("")
        expectedShow = "EXCEPTION: {}\n".format(message)
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

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
        theController = Controller(TestView.TestView(), None)
        # add 10 Records, reset view log, then serial save
        self._addSomeRecordsViaController(theController, 10)
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

    @patch('builtins.open')
    @patch('os.path.isfile')
    def test_SerialSave_02(self, mock_isfile, mock_open):
        """
        Ensure that a serial save does not happen when file exists
        - isfile will return true
        - Ensure open does not get called: If it does an error will be raised
        """
        mock_isfile.return_value = True
        mock_open.side_effect = AssertionError()
        theController = Controller(TestView.TestView(), None)

        TestView.clearLog()
        theController.do_serial_save("")
        expectedShow = "Will not overwrite an existing file\nPlease, enter a \
new file when using serial_save\n"
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('builtins.open')
    @patch('os.path.isfile')
    def test_SerialSave_03(self, mock_isfile, mock_open):
        """
        Handles IOError
        - Because the IOError message is expected to be determined by the
           IOError constructor, the message will be randomised
        """
        message = str(random.randrange(100))
        mock_isfile.return_value = False
        mock_open.side_effect = IOError(message)
        theController = Controller(TestView.TestView(), None)
        TestView.clearLog()
        theController.do_serial_save("")
        expectedShow = "EXCEPTION: {}\n".format(message)
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('builtins.open')
    @patch('os.path.isfile')
    def test_TextSave_01(self, mock_isfile, mock_open):
        """
        Ensure that a text save does not happen when file exists
        - isfile will return true
        - Ensure open does not get called: If it does an error will be raised
        """
        mock_isfile.return_value = True
        mock_open.side_effect = AssertionError()
        theController = Controller(TestView.TestView(), None)

        TestView.clearLog()
        theController.do_text_save("")
        expectedShow = "Will not overwrite an existing file\nPlease, enter a \
new file when using text_save\n"
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('builtins.open')
    @patch('os.path.isfile')
    def test_TextSave_02(self, mock_isfile, mock_open):
        """
        Handles IOError
        - Because the IOError message is expected to be determined by the
           IOError constructor, the message will be randomised
        """
        message = str(random.randrange(100))
        mock_isfile.return_value = False
        mock_open.side_effect = IOError(message)
        theController = Controller(TestView.TestView(), None)
        TestView.clearLog()
        theController.do_text_save("")
        expectedShow = "EXCEPTION: {}\n".format(message)
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)

    @patch('builtins.open')
    @patch('os.path.isfile')
    def test_TextSave_03(self, mock_isfile, mock_open):
        """
        Add 2 Records, then expect the text save to produce 2 text lines
        """
        def doText():
            doText.theText = theTextStream.getvalue()

        theTextStream = StringIO()
        theTextStream.close = Mock(side_effect=doText)
        mock_isfile.return_value = False
        mock_open.return_value = theTextStream

        theController = Controller(TestView.TestView(), None)
        self._addSomeRecordsViaController(theController, 2)

        TestView.clearLog()
        theController.do_text_save("")

        # Part 1: Text data
        expectedData = "A000 M 0 0 Normal 0\nA001 M 0 0 Normal 0"
        actualData = doText.theText
        self.assertEqual(expectedData, actualData)

        # Part 2: Show
        expectedShow = "Saved As Text"
        actualShow = TestView.theLog[0]
        self.assertEqual(expectedShow, actualShow)


if __name__ == "__main__":
    unittest.main()
        