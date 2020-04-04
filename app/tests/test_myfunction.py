import unittest
from django.test import TestCase

from app import math


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(math.add(3, 5), 8)


if __name__ == '__main__':
    unittest.main()
