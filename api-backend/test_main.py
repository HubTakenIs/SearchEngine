import unittest

from main import *


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(["hello","world"],processBooleanQuery("multimedia AND images OR CATS"))
        


if __name__ == '__main__':
    unittest.main()