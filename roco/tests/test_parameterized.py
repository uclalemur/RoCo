import sys
import os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from api.parameterized import Parameterized  # Imports the Parameterized class

class TestParameterized(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual(True, True)  # Check if the code works
        
    def test_add_parameter_keyerror(self):
    	p = Parameterized()
    	p.add_parameter("1","RandomValue")
        self.assertRaises(KeyError,p.add_parameter,"1","RandomValue")  # Fails if a KeyError is not raised
        # A KeyError should be raised because a parameter called 1 has already been created
        # Therefore this test should succeed
        
    def test_add_parameter_return(self):
    	p = Parameterized()
        self.assertIsNotNone(p.add_parameter("1","RandomValue"))  # Fails if add_parameter doesn't return anything

    def test_check_constraints(self):
    	p = Parameterized()
        self.assertEqual(p.check_constraints(),True)  # Fails if any of the constraints is not satisfied
        
    def test_del_parameter(self):
    	p = Parameterized()
    	p.add_parameter("1","RandomValue")
        self.assertEqual(p.del_parameter(1),"RandomValue")  #  Should return the removed parameter called 1

if __name__ == '__main__':
    unittest.main()