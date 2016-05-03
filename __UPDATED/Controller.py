import cmd

from CustomException import CustomException
from Record import Record
from RecordCollection import RecordCollection
from Option import Option
from Filer import Filer

from AbstractView import AbstractView
from AbstractController import AbstractController

from AbstractObjectInfo import AbstractObjectInfo
from OptionObjectInfo import OptionObjectInfo
from RecordObjectInfo import RecordObjectInfo

from AbstractObjectCaller import AbstractObjectCaller
import OptionObjectCaller
import RecordObjectCaller

from GlobalMethod import safeInt


class ViewException(CustomException):

    def __init__(self, theReason="Not a View"):
        super(ViewException, self).__init__(theReason)


class InsufficientArgumentsException(CustomException):

    def __init__(self, theReason="Not Enough Arguments Provided"):
        super(InsufficientArgumentsException, self).__init__(theReason)


class Controller(cmd.Cmd, AbstractController, AbstractObjectInfo):

    _autoid_onStr = "If an invalid or duplicate ID is specified when adding \
a record, that record is assigned an ID automatically (a blank ID is invalid)"
    _autoid_offStr = "No automatic IDs will be used when adding records"
    _overwrite_onStr = "If a duplicate ID is specified when adding a \
record, the original record with the same ID is removed (this overpowers \
auto ID)"
    _overwrite_offStr = "No records will be removed when adding records"
    _record_selectedStr = "Selected Record"
    _record_unselectedStr = "No record selected"
    _option_selectedStr = "Selected Option"
    _option_unselectedStr = "No option selected"

    def __init__(self, newView, newRecordColl=None):
        super(Controller, self).__init__()
        if not isinstance(newView, AbstractView):
            raise ViewException()
        self.prompt = "ERP "
        self._myView = newView
        self._options = {}
        self._options["AUTOID"] = Option("Auto ID", "If an invalid or \
duplicate ID is specified when adding a record, that record is assigned \
an ID automatically (a blank ID is invalid)", "No automatic IDs will be \
used when adding records")
        self._options["OVERWRITE"] = Option("Overwrite", "If a duplicate \
ID is specified when adding a record, the original record with the same \
ID is removed (this overpowers auto ID)", "No records will be removed \
when adding records")
        if (newRecordColl is not None and
                isinstance(newRecordColl, RecordCollection)):
            self._theColl = newRecordColl
        else:
            self._theColl = RecordCollection()
        self._selectedObject = self
        self._myView.show("EMPLOYEE RECORD PROGRAM - ")

    # Protected

    def _add(self, data):
        recArgs = data.split(" ")
        if 6 <= len(recArgs):
            self._theColl.addRecord(recArgs[0], recArgs[1], recArgs[2],
                                    recArgs[3], recArgs[4], recArgs[5],
                                    self._options["AUTOID"].isOn(),
                                    self._options["OVERWRITE"].isOn())
        else:
            raise InsufficientArgumentsException()

    def _showSelectedObjectInfo(self, headerStr):
        self._myView.show(headerStr)
        self._myView.show(self._selectedObject.getAsString())
        self._myView.show(self._selectedObject.getFunctionDesc())

    def _callSelectedObject(self, theObjectCaller, mainMessage, excMessage):
        trial = self._selectedObject.getClassObject()
        try:
            theObjectCaller.setObject(trial)
            theObjectCaller.callObject()
            self._showSelectedObjectInfo(mainMessage)
        except CustomException as e:
            self._selectedObject = self
            self._myView.show(excMessage)

    # Public

    def do_view_records(self, arg):
        """
        View all the records
        """
        allRecords = self._theColl.getAllRecords()
        result = ""
        for r in allRecords:
            result += "{} {} {} {} {} {}\n".format(r.getID(), r.getGender(),
                                                   r.getAge(), r.getSales(),
                                                   r.getBMI(), r.getIncome())
        self._myView.show(result)

    def do_view_options(self, arg):
        """
        View the options and their purpose
        """
        for code in self._options:
            theOption = OptionSelectable(self._options[code], "")
            self._myView.show("Option Code: {}".format(code))
            self._myView.show(theOption.getAsString())

    def do_select_rec(self, arg):
        """
        Select a record by ID, for inspection and editing
        arg: The ID of the existing record

        """
        trial = self._theColl.getRecord(arg)
        if trial is not None:
            self._selectedObject = RecordObjectInfo(trial, "Use the \
following with the appropriate argument to edit the record:\n+ edit_age\n+ \
edit_sales\n+ edit_bmi\n+ edit_income\n")
            self._showSelectedObjectInfo(Controller._record_selectedStr)
        else:
            self._myView.show("There is no record with that ID\n")
            self._selectedObject = self

    def do_select_option(self, arg):
        """
        Select an option for turning on/off, and seeing what it will do
        arg: The option code
        For option codes, please command view_options
        """
        trial = arg.upper()
        if trial in self._options:
            self._selectedObject = OptionObjectInfo(self._options[trial], "\
Use the following to set the option:\n+ on\n+ off\n")
            self._showSelectedObjectInfo(Controller._option_selectedStr)
        else:
            self._myView.show("There is no option\n")
            self._selectedObject = self

    def do_text_load(self, arg):
        """
        Load records from a text file; depending on their IDs and the options,
        ERP will attempt to append all records to the collection
        arg: The loaction of the text file
        """
        self._selectedObject = self
        Filer().textLoad(arg, self)

    def do_text_save(self, arg):
        """
        Save records to a text file
        arg: The location of the text file
        Please specify a non existing file
        """
        Filer().textSave(arg, self)
        self._selectedObject = self

    def do_serial_load(self, arg):
        """
        Instructions for loading a serial record collection as the ERP starts
        """
        myView.show("++ APPLIES TO SERIAL COLLECTION, NOT TEXT ++\n\
When starting ERP via the command line, enter the argument\
\n    COLL:[file location]\nERP will then attempt to load the collection \
from that\n")

    def do_serial_save(self, arg):
        """
        Save records as serial data
        arg: The location of the text file
        Please specify a non existing file
        For instructions on loading serial data, please command serial_load
        """
        Filer().serialSave(arg, self)
        self._selectedObject = self

    def do_add_rec(self, arg):
        """
        Add a record to the collection
        Separate each argument with a space
        arg 1: ID [A-Z][0-9]{3}
        arg 2: Gender (M|F)
        arg 3: Age [0-9]{2}
        arg 4: Sales [0-9]{3}
        arg 5: BMI (Normal|Overweight|Obesity|Underweight)
        arg 6: Income [0-9]{2,3}
        """
        self._selectedObject = self
        try:
            self._add(arg)
        except CustomException as e:
            self._myView.show("EXCEPTION: {}\n".format(str(e)))
        else:
            self._myView.show("Record added\n")

    def do_edit_age(self, arg):
        """
        A record must be selected
        Change the age of the record
        arg: [0-9]{2}
        """
        theObjectCaller = RecordObjectCaller.ROC_SetAge(arg)
        self._callSelectedObject(theObjectCaller,
                                 Controller._record_selectedStr,
                                 Controller._record_unselectedStr)

    def do_edit_sales(self, arg):
        """
        A record must be selected
        Change the sales of the record
        arg: [0-9]{3}
        """
        theObjectCaller = RecordObjectCaller.ROC_SetSales(arg)
        self._callSelectedObject(theObjectCaller,
                                 Controller._record_selectedStr,
                                 Controller._record_unselectedStr)

    def do_edit_bmi(self, arg):
        """
        A record must be selected
        Change the BMI of the record
        arg: (Normal|Overweight|Obesity|Underweight)
        """
        theObjectCaller = RecordObjectCaller.ROC_SetBMI(arg)
        self._callSelectedObject(theObjectCaller,
                                 Controller._record_selectedStr,
                                 Controller._record_unselectedStr)

    def do_edit_income(self, arg):
        """
        A record must be selected
        Change the income of the record
        arg: [0-9]{3}
        """
        theObjectCaller = RecordObjectCaller.ROC_SetIncome(arg)
        self._callSelectedObject(theObjectCaller,
                                 Controller._record_selectedStr,
                                 Controller._record_unselectedStr)

    def do_on(self, arg):
        """
        An option must be selected
        Turn the option on
        """
        theObjectCaller = OptionObjectCaller.OOC_TurnOn()
        self._callSelectedObject(theObjectCaller,
                                 Controller._option_selectedStr,
                                 Controller._option_unselectedStr)

    def do_off(self, arg):
        """
        An option must be selected
        Turn the option off
        """
        theObjectCaller = OptionObjectCaller.OOC_TurnOff()
        self._callSelectedObject(theObjectCaller,
                                 Controller._option_selectedStr,
                                 Controller._option_unselectedStr)

    def do_neutral(self, arg):
        """
        Put the control of ERP in a neutral state
        """
        self._selectedObject = self
        self._showSelectedObjectInfo(None)
        # self._enterNeutralState()
        # self._representERP()

    def do_exit(self, arg):
        """
        If a record or an option is selected, ERP enters a neutral state
        Otherwise, ERP ends
        """
        if self._selectedObject is self:
            self._myView.show("END")
            return True
        else:
            self._selectedObject = self
            self._showSelectedObjectInfo(None)

    def do_help(self, arg):
        """
        Special help
        """
        super(Controller, self).do_help(arg)

    # As AbstractController

    def getRecordCollection(self):
        return self._theColl

    def getAllRecords(self):
        return self._theColl.getAllRecords()

    def addRecordData(self, data):
        self._add(data)

    def show(self, message):
        self._myView.show(message)

    # As AbstractObjectInfo

    def getAsString(self):
        return "Records in ERP: {}".format(len(self._theColl.getAllRecords()))

    def getFunctionDesc(self):
        return ""

    def getClassObject(self):
        return self

    # Graphic

    def do_graphic_gender_pie_chart(self, arg):  # pragma: no cover
        """
        Graphic: Pie chart representing gender ratio of employee records
        """
        mCount = 0
        fCount = 0
        allRecords = self._theColl.getAllRecords()
        for r in allRecords:
            if r.getGender() == "M":
                mCount += 1
            elif r.getGender() == "F":
                fCount += 1
        self._myView.pieChart([("Males", mCount), ("Females", fCount)])

    # SMELL: Long Method
    def do_graphic_age_bar_chart(self, arg):  # pragma: no cover
        """
        Graphic: Bar chart representing number of people per age group
        arg1: Lowest age (default 0)
        arg2: Highest age (default 100)
        arg3: Size of each age group (default 5)
        The arguments are optional, for example if you only enter one
        argument then that is the lowest age
        """
        start = 0
        end = 100
        interval = 5
        spec = arg.split(" ")
        if 2 < len(spec):
            trial = safeInt(spec[2], interval)
            if trial != 0:
                interval = trial
        if 1 < len(spec):
            end = safeInt(spec[1], end)
        if 0 < len(spec):
            start = safeInt(spec[0], start)
        limits = []
        ageCount = []
        for i in range(start, end, interval):
            limits.append(i)
            ageCount.append(0)
        allRecords = self._theColl.getAllRecords()
        for r in allRecords:
            a = r.getAge()
            lastLimit = None
            k = 0
            while k < len(limits) and limits[k] < a:
                lastLimit = k
                k += 1
            if lastLimit is not None:
                ageCount[lastLimit] += 1
        self._myView.barChart(limits, ageCount)
