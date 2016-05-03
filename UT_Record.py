import sys
import unittest

thePaths = sys.argv[1:]
for path in thePaths:
    sys.path.append(path)

sys.argv = sys.argv[:1]

from Record import Record, InvalidGenderException


class TestRecordClass(unittest.TestCase):

    def test_InvalidGenderException(self):
        """
        Ensure that a correct definition of gender is adhered to
        """
        self.assertRaises(InvalidGenderException, Record, None, "")

    def test_DefaultAttributes(self):
        """
        Expect default atttibute values (age 0, sales 0, BMI Normal, income 0)
        """
        expAge = 0
        expSales = 0
        expBMI = "Normal"
        expIncome = 0
        rec = Record(None, "M")
        self.assertEqual(expAge, rec.getAge())
        self.assertEqual(expSales, rec.getSales())
        self.assertEqual(expBMI, rec.getBMI())
        self.assertEqual(expIncome, rec.getIncome())

    def test_GenderCapitalLetter(self):
        """
        Expect gender to be represented by a capital M/F, even when set as m/f
        """
        expM = "M"
        recM = Record(None, "m")
        self.assertEqual(expM, recM.getGender())
        expF = "F"
        recF = Record(None, "f")
        self.assertEqual(expF, recF.getGender())

    def test_NoChangeAge01(self):
        """
        Expect age to remain after attempting to set it to 100 (over the limit)
        """
        expAge = 99
        rec = Record(None, "M")
        """Default values proven in other test"""
        rec.setAge(expAge)
        rec.setAge(100)
        self.assertEqual(expAge, rec.getAge())

    def test_NoChangeAge02(self):
        """
        Expect age to remain after attempting to set it to 40.5 (decimal)
        """
        expAge = 41
        rec = Record(None, "F")
        """Default values proven in other test"""
        rec.setAge(expAge)
        rec.setAge(40.5)
        self.assertEqual(expAge, rec.getAge())

    def test_NoChangeAge03(self):
        """
        Expect age to remain after attempting to set it to "A"
        String can be used for the method, but "A" represents no number
        """
        expAge = 30
        ageStr = str(30)
        rec = Record(None, "F")
        """Default values proven in other test"""
        rec.setAge(ageStr)
        rec.setAge("A")
        self.assertEqual(expAge, rec.getAge())

    def test_NoChangeSales01(self):
        """
        Expect sales to remain after attempting to set it to 1000
        (over the limit)
        """
        expSales = 999
        rec = Record(None, "M")
        """Default values proven in other test"""
        rec.setSales(expSales)
        rec.setSales(1000)
        self.assertEqual(expSales, rec.getSales())

    def test_NoChangeSales02(self):
        """
        Expect sales to remain after attempting to set it to 406.5 (decimal)
        """
        expSales = 410
        rec = Record(None, "F")
        """Default values proven in other test"""
        rec.setSales(expSales)
        rec.setSales(406.5)
        self.assertEqual(expSales, rec.getSales())

    def test_NoChangeSales03(self):
        """
        Expect sales to remain after attempting to set it to "A"
        String can be used for the method, but "A" represents no number
        """
        expSales = 330
        salesStr = str(330)
        rec = Record(None, "F")
        """Default values proven in other test"""
        rec.setSales(salesStr)
        rec.setSales("A")
        self.assertEqual(expSales, rec.getSales())

    def test_NoChangeIncome01(self):
        """
        Expect income to remain after attempting to set it to 1000
        (over the limit)
        """
        expIncome = 999
        rec = Record(None, "M")
        """Default values proven in other test"""
        rec.setIncome(expIncome)
        rec.setIncome(1000)
        self.assertEquals(expIncome, rec.getIncome())

    def test_NoChangeIncome02(self):
        """
        Expect sales to remain after attempting to set it to 406.5 (decimal)
        """
        expIncome = 410
        rec = Record(None, "F")
        """Default values proven in other test"""
        rec.setIncome(expIncome)
        rec.setIncome(406.5)
        self.assertEqual(expIncome, rec.getIncome())

    def test_NoChangeIncome03(self):
        """
        Expect income to remain after attempting to set it to "A"
        String can be used for the method, but "A" represents no number
        """
        expIncome = 220
        incomeStr = str(220)
        rec = Record(None, "F")
        """Default values proven in other test"""
        rec.setIncome(incomeStr)
        rec.setIncome("A")
        self.assertEqual(expIncome, rec.getIncome())

    def test_NoChangeBMI(self):
        """
        Expect BMI to remain after attempting to set it to 'other' (not
        recognised in enumeration)
        """
        expBMI = "Overweight"
        rec = Record(None, "M")
        """Default values proven in other test"""
        rec.setBMI(expBMI)
        rec.setBMI("other")
        self.assertEqual(expBMI, rec.getBMI())


if __name__ == "__main__":
    unittest.main()
