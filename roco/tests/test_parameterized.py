import sys
import os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from parameterized import Parameterized # Imports the Parameterized class

class TestParameterized(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual(True, True)  # To check if the code works
        
    def test_add_parameter(self):
    	p = Parameterized()
        self.assertRaises(Exception,p.add_parameter,"1","RandomValue")  # Fails if an exception is raised

if __name__ == '__main__':
    unittest.main()