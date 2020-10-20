import unittest
from project.models.measure import Measure


class MyTestCase(unittest.TestCase):
    def test_attributes(self):
        number = 1
        name = "test_measure"
        desc = "this measure does nothing"
        factor = 1
        measure = Measure(number, name, desc, factor)
        self.assertEqual(1, measure.number)
        self.assertEqual("test_measure", measure.name)
        self.assertEqual("this measure does nothing", measure.desc)
        self.assertEqual(1, measure.factor)

    def test_menu(self):
        number = 1
        name = "test_measure"
        desc = "this measure does nothing"
        factor = 1
        measure = Measure(number, name, desc, factor)
        string = str(measure)
        self.assertEqual("#1| False| test_measure: this measure does nothing", string)

    def test_effect(self):
        number = 1
        name = "test_measure"
        desc = "this measure does something"
        factor = 0.5
        measure = Measure(number, name, desc, factor)
        # pylint: disable=invalid-name
        R0 = 1
        R1 = R0 * measure.factor
        R2 = R1 * measure.factor
        self.assertAlmostEqual(1, R0)
        self.assertAlmostEqual(0.5, R1)
        self.assertAlmostEqual(0.25, R2)

    def test_update_return_factor(self):
        measure = Measure(1, "name", "description", 0.8)
        self.assertFalse(measure.active)
        factor_on = measure.update_return_factor()
        self.assertEqual(0.8, factor_on)
        self.assertTrue(measure.is_active())
        factor_off = measure.update_return_factor()
        self.assertEqual(1.25, factor_off)
        self.assertFalse(measure.is_active())


if __name__ == '__main__':
    unittest.main()
