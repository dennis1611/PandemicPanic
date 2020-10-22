import unittest
from project.models.measure import Measure
from project.models.score import Score
from project.models.region import Region


class MyTestCase(unittest.TestCase):
    def generate_test_case(self):
        inh = 100000
        inf = 100
