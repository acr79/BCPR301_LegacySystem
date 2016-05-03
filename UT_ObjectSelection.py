import sys
import unittest
import random

thePaths = sys.argv[1:]
for path in thePaths:
    sys.path.append(path)

sys.argv = sys.argv[1:]

import TestView
from Controller import Controller
from RecordCollection import RecordCollection
from Record import Record


class TestObjectSelectionClass(unittest.TestCase):

    _expRecordHeader = "Selected Record"
    _expRecordFunctions = "Use the following with the \
appropriate argument to edit the record:\n+ edit_age\n+ edit_sales\n+ \
edit_bmi\n+ edit_income\n"
    _expOptionHeader = "Selected Option"
    _expOptionFunctions = "Use the following to set the \
option:\n+ on\n+ off\n"

    def _getRecordColl_OneMaleRecord_RandomID(self):
        theRC = RecordCollection()
        draftID = "A"
        for x in range(3):
            draftID += str(random.randrange(10))
        theRC.addRecord(draftID, "M", None, None, None, None, False, False)
        return theRC

    def _getRecordStateMessage(self, id, gender="M", age="0", sales="0",
                               bmi="Normal", income="0"):
        return "ID: {}\nGENDER: {}\nAGE: {}\nSALES: {}\nBMI: {}\nINCOME: {}\n\
".format(id, gender, age, sales, bmi, income)

    def test_NoRecordSelected(self):
        """
        This can be asserted by attempting to select an option
        - Regardless if the attempt works or not, one expected outcome is that
           no record will be selected
        """
        theController = Controller(TestView.TestView(), None)
        theController.do_select_option("")
        # For the method calls below, the main flow requires a record to be
        #  selected, therefore the alternative show message is expected
        expectedMessage = "No record selected"
        TestView.clearLog()
        theController.do_edit_age("")
        theController.do_edit_sales("")
        theController.do_edit_bmi("")
        theController.do_edit_income("")
        # 4 calls
        self.assertEqual(4, len(TestView.theLog))
        for actualMessage in TestView.theLog:
            self.assertEqual(expectedMessage, actualMessage)

    def test_NoOptionSelected(self):
        """
        This can be asserted by attempting to select a record
        - Regardless if the attempt works or not, one expected outcome is that
           no option will be selected
        """
        theController = Controller(TestView.TestView(), None)
        theController.do_select_rec("")
        # For the method calls below, the main flow requires an option to be
        #  selected, therefore the alternative show message is expected
        expectedMessage = "No option selected"
        TestView.clearLog()
        theController.do_on("")
        theController.do_off("")
        # 2 calls
        self.assertEqual(2, len(TestView.theLog))
        for actualMessage in TestView.theLog:
            self.assertEqual(expectedMessage, actualMessage)

    def test_DoesNotSelectRecord(self):
        """
        To successfully select a record, the correct ID must be provided
        - No correct ID provided would expect an alternative show message
        """
        expected = "There is no record with that ID\n"
        incorrectID = ""
        theController = Controller(TestView.TestView(), None)
        TestView.clearLog()
        # Call
        theController.do_select_rec(incorrectID)
        self.assertEqual(expected, TestView.theLog[0])

    def test_DoesNotSelectOption(self):
        """
        To successfully select an option, the correct code must be provided
        - No correct code provided would expect an alternative show message
        """
        expected = "There is no option\n"
        incorrectCode = ""
        theController = Controller(TestView.TestView(), None)
        TestView.clearLog()
        # Call
        theController.do_select_option(incorrectCode)
        self.assertEqual(expected, TestView.theLog[0])

    def test_SelectedRecord_EditAge(self):
        """
        A RecordCollection with one Record will be provided to Controller
        - Random ID, male, default attributes
        - Randomise an age
        - Methodology for picking a new age will be (original age + 1) % 100
        """
        theRC = self._getRecordColl_OneMaleRecord_RandomID()
        theRecord = theRC.getAllRecords()[0]
        theID = theRecord.getID()
        theRecord.setAge(random.randrange(100))
        originalAge = theRecord.getAge()
        newAge = (originalAge + 1) % 100  # 100 is age limit
        theController = Controller(TestView.TestView(), theRC)
        # From here the record will be manipulated via theController
        # Successful calls will represent the record via show message
        expected_1 = self._getRecordStateMessage(theID, age=originalAge)
        expected_2 = self._getRecordStateMessage(theID, age=newAge)

        # Call 1, selecting the record. 3 show messages
        expectedList = [TestObjectSelectionClass._expRecordHeader, expected_1,
                        TestObjectSelectionClass._expRecordFunctions]
        TestView.clearLog()
        theController.do_select_rec(theID)
        self.assertEqual(expectedList, TestView.theLog)

        # Call 2, editing the age. 3 show messages
        expectedList[1] = expected_2
        TestView.clearLog()
        theController.do_edit_age(newAge)
        self.assertEqual(expectedList, TestView.theLog)

    def test_SelectedRecord_EditSales(self):
        """
        A RecordCollection with one Record will be provided to Controller
        - Random ID, male, default attributes
        - Randomise a sales
        - Methodology for picking a new sales will be
           (original sales + 1) % 1000
        """
        theRC = self._getRecordColl_OneMaleRecord_RandomID()
        theRecord = theRC.getAllRecords()[0]
        theID = theRecord.getID()
        theRecord.setSales(random.randrange(1000))
        originalSales = theRecord.getSales()
        newSales = (originalSales + 1) % 1000  # 1000 is sales limit
        theController = Controller(TestView.TestView(), theRC)
        # From here the record will be manipulated via theController
        # Successful calls will represent the record via show message
        expected_1 = self._getRecordStateMessage(theID, sales=originalSales)
        expected_2 = self._getRecordStateMessage(theID, sales=newSales)

        # Call 1, selecting the record. 3 show messages
        expectedList = [TestObjectSelectionClass._expRecordHeader, expected_1,
                        TestObjectSelectionClass._expRecordFunctions]
        TestView.clearLog()
        theController.do_select_rec(theID)
        self.assertEqual(expectedList, TestView.theLog)

        # Call 2, editing the sales. 3 show messages
        expectedList[1] = expected_2
        TestView.clearLog()
        theController.do_edit_sales(newSales)
        self.assertEqual(expectedList, TestView.theLog)

    def test_SelectedRecord_EditBMI(self):
        """
        A RecordCollection with one Record will be provided to Controller
        - Random ID, male, default attributes
        - New BMI will be Overweight
        """
        theRC = self._getRecordColl_OneMaleRecord_RandomID()
        theRecord = theRC.getAllRecords()[0]
        theID = theRecord.getID()
        newBMI = "Overweight"
        theController = Controller(TestView.TestView(), theRC)
        # From here the record will be manipulated via theController
        # Successful calls will represent the record via show message
        expected_1 = self._getRecordStateMessage(theID)
        expected_2 = self._getRecordStateMessage(theID, bmi=newBMI)

        # Call 1, selecting the record. 3 show messages
        expectedList = [TestObjectSelectionClass._expRecordHeader, expected_1,
                        TestObjectSelectionClass._expRecordFunctions]
        TestView.clearLog()
        theController.do_select_rec(theID)
        self.assertEqual(expectedList, TestView.theLog)

        # Call 2, editing the BMI. 3 show messages
        expectedList[1] = expected_2
        TestView.clearLog()
        theController.do_edit_bmi(newBMI)
        self.assertEqual(expectedList, TestView.theLog)

    def test_SelectedRecord_EditIncome(self):
        """
        A RecordCollection with one Record will be provided to Controller
        - Random ID, male, default attributes
        - Randomise an income
        - Methodology for picking a new income will be
           (original sales + 1) % 1000
        """
        theRC = self._getRecordColl_OneMaleRecord_RandomID()
        theRecord = theRC.getAllRecords()[0]
        theID = theRecord.getID()
        theRecord.setIncome(random.randrange(1000))
        originalIncome = theRecord.getIncome()
        newIncome = (originalIncome + 1) % 1000  # 1000 is income limit
        theController = Controller(TestView.TestView(), theRC)
        # From here the record will be manipulated via theController
        # Successful calls will represent the record via show message
        expected_1 = self._getRecordStateMessage(theID, income=originalIncome)
        expected_2 = self._getRecordStateMessage(theID, income=newIncome)

        # Call 1, selecting the record. 3 show messages
        expectedList = [TestObjectSelectionClass._expRecordHeader, expected_1,
                        TestObjectSelectionClass._expRecordFunctions]
        TestView.clearLog()
        theController.do_select_rec(theID)
        self.assertEqual(expectedList, TestView.theLog)

        # Call 2, editing the income. 3 show messages
        expectedList[1] = expected_2
        TestView.clearLog()
        theController.do_edit_income(newIncome)
        self.assertEqual(expectedList, TestView.theLog)

    def test_SelectedOption_TurnOnAndOff(self):
        """
        Options cannot be dynamically added to Controller
        This test is based on the fact that Auto ID option exists
        - Originally turned off
        - Can be selected with argument "autoid"
        - Its string descriptions are hard-coded, and ERP functionality states
           what they must contain
        """

        def getAutoIDStateMessage(expectOn):
            state = "OFF"
            if expectOn:
                state = "ON"
            return "Auto ID: TURNED {}\n. . .\nON: If an invalid or \
duplicate ID is specified when adding a record, that record is assigned an \
ID automatically (a blank ID is invalid)\nOFF: No automatic IDs will be used \
when adding records\n\n".format(state)

        # Option will start off, then get turned on, then off again
        expectedOff = getAutoIDStateMessage(False)
        expectedOn = getAutoIDStateMessage(True)
        theController = Controller(TestView.TestView(), None)

        # Call 1, selecting the option. 3 show messages
        expectedList = [TestObjectSelectionClass._expOptionHeader,
                        expectedOff,
                        TestObjectSelectionClass._expOptionFunctions]
        TestView.clearLog()
        theController.do_select_option("autoid")
        self.assertEqual(expectedList, TestView.theLog)

        # Call 2, turn off. 3 show messages
        expectedList[1] = expectedOn
        TestView.clearLog()
        theController.do_on("")
        self.assertEqual(expectedList, TestView.theLog)

        # Call 3, turn on. 3 show messages
        expectedList[1] = expectedOff
        TestView.clearLog()
        theController.do_off("")
        self.assertEqual(expectedList, TestView.theLog)


if __name__ == "__main__":
    unittest.main()
