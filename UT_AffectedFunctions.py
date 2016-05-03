"""
These tests are focused on other functions of Controller that will be affected
 by the refactoring session, that introduces a new pattern that uses the
 concept interfaces AbstractObjectCaller and AbstractObjectInfo
"""

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


class TestAffectedFunctionsClass(unittest.TestCase):

    def _getRecordColl_OneMaleRecord_RandomID(self):
        # Returns tuple, 2 elements
        theRC = RecordCollection()
        draftID = "A"
        for x in range(3):
            draftID += str(random.randrange(10))
        theRC.addRecord(draftID, "M", None, None, None, None, False, False)
        return (theRC, draftID)

    def test_ControllerExit_ReturnTrue_Condition(self):
        """
        Concerned with the show ouput on command
        > exit
         if a record/option is selected
        Otherwise that method returns True
        """
        neutralStr = "Records in ERP: 1"
        # Start Controller with RecordCollection, with 1 record
        theRC, testID = self._getRecordColl_OneMaleRecord_RandomID()
        theController = Controller(TestView.TestView(), theRC)

        TestView.clearLog()
        expected_1 = "Selected Record"
        expected_2 = neutralStr
        # Call 1. Select record, then exit
        theController.do_select_rec(testID)
        actual_1 = TestView.theLog[0]
        TestView.clearLog()
        theReturn = theController.do_exit("")
        actual_2 = TestView.theLog[0]
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertNotEqual(True, theReturn)

        TestView.clearLog()
        expected_3 = "Selected Option"
        expected_4 = neutralStr
        # Call 2. Select option, then exit
        theController.do_select_option("autoid")
        actual_3 = TestView.theLog[0]
        TestView.clearLog()
        theReturn = theController.do_exit("")
        actual_4 = TestView.theLog[0]
        self.assertEqual(expected_3, actual_3)
        self.assertEqual(expected_4, actual_4)
        self.assertNotEqual(True, theReturn)

        # Different outcome when Controller in neutral state
        TestView.clearLog()
        expected_5 = "END"
        theReturn = theController.do_exit("")
        actual_5 = TestView.theLog[0]
        self.assertEqual(expected_5, actual_5)
        self.assertTrue(theReturn)

    def test_ControllerNeutralState(self):
        """
        Concerned with the show output on command
        > neutral

        Concerned with no record/option selected
        """
        # Start Controller with RecordCollection, with 1 record
        theRC, testID = self._getRecordColl_OneMaleRecord_RandomID()
        theController = Controller(TestView.TestView(), theRC)

        # Call 1, do neutral. Expect number of records to be 1
        expected_1 = "Records in ERP: 1"
        TestView.clearLog()

        theController.do_neutral("")
        actual_1 = TestView.theLog[0]
        self.assertEqual(expected_1, actual_1)

        # Call 2, 3. Select the record.
        # Then go neutral and no record is selected
        expected_2 = "Selected Record"
        TestView.clearLog()
        theController.do_select_rec(testID)
        actual_2 = TestView.theLog[0]
        self.assertEqual(expected_2, actual_2)

        theController.do_neutral("")
        expected_3 = "No record selected"
        TestView.clearLog()
        theController.do_edit_age("")
        actual_3 = TestView.theLog[0]
        self.assertEqual(expected_3, actual_3)

        # Call 4, 5. Select the option.
        # Then go neutral and no option is selected
        expected_4 = "Selected Option"
        TestView.clearLog()
        theController.do_select_option("autoid")
        actual_4 = TestView.theLog[0]
        self.assertEqual(expected_4, actual_4)

        theController.do_neutral("")
        expected_5 = "No option selected"
        TestView.clearLog()
        theController.do_on("")
        actual_5 = TestView.theLog[0]
        self.assertEqual(expected_5, actual_5)

    # def test_ViewTheOptions(self):
    # inapplicable, cannot predict show order
    # changes would have to be made in __ORIGINAL

if __name__ == "__main__":
    unittest.main()
