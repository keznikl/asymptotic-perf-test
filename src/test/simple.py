
import unittest
import re


class RETest(unittest.TestCase):
    def setUp(self):
        self.regexp = '\s*O\((\d+)\)\s*<\s*(\d+)\s*\*\s*O\((\d+)\)\s*'
        self.test_value = 'O(1000) < 2*O(1)'
        self.m = re.match(self.regexp, self.test_value)
    def testReScaleNone(self):
        self.assertIsNotNone(self.m, "Ra exp. does not match")
    def testReScaleGroups(self):
        self.assertEqual(self.m.group(1), "1000", "Ra exp. group 1 does not match")
        self.assertEqual(self.m.group(2), "2", "Ra exp. group 2 does not match")
        self.assertEqual(self.m.group(3), "1", "Ra exp. group 3 does not match")
