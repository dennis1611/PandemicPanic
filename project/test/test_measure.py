import unittest
from project.measure import Measure


class MyTestCase(unittest.TestCase):
    def test_attributes(self):
        number = 1
        name = "test_measure"
        desc = "this measure does nothing"
        factor = 1
        m1 = Measure(number, name, desc, factor)
        self.assertEqual(1, m1.number)
        self.assertEqual("test_measure", m1.name)
        self.assertEqual("this measure does nothing", m1.desc)
        self.assertEqual(1, m1.factor)

    def test_menu(self):
        number = 1
        name = "test_measure"
        desc = "this measure does nothing"
        factor = 1
        m1 = Measure(number, name, desc, factor)
        string = str(m1)
        self.assertEqual("#1| False| test_measure: this measure does nothing", string)

    def test_effect(self):
        number = 1
        name = "test_measure"
        desc = "this measure does something"
        factor = 0.5
        m1 = Measure(number, name, desc, factor)
        R0 = 1
        R1 = R0 * m1.factor
        R2 = R1 * m1.factor
        self.assertAlmostEqual(1, R0)
        self.assertAlmostEqual(0.5, R1)
        self.assertAlmostEqual(0.25, R2)

    def test_active(self):
        number = 1
        name = "test_measure"
        desc = "this measure does nothing"
        factor = 1
        m1 = Measure(number, name, desc, factor)
        self.assertFalse(m1.active)
        m1.activate()
        self.assertTrue(m1.is_active())
        m1.deactivate()
        self.assertFalse(m1.active)


if __name__ == '__main__':
    unittest.main()
