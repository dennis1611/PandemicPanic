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

    def test_active(self):
        number = 1
        name = "test_measure"
        desc = "this measure does nothing"
        factor = 1
        measure = Measure(number, name, desc, factor)
        self.assertFalse(measure.active)
        measure.activate()
        self.assertTrue(measure.is_active())
        measure.deactivate()
        self.assertFalse(measure.active)


if __name__ == '__main__':
    unittest.main()
