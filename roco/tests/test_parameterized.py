import sys
import os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from api.parameterized import Parameterized  # Imports the Parameterized class

class TestParameterized(unittest.TestCase):
    def setUp(self):
        self.p = Parameterized()
        # Creates a single set-up code for all test cases that need an instance of Parameterized
        # It is called for every single test case

        
    def test_dummy(self):
        self.assertEqual(True, True)  # Check if the code works
        
    def test_add_parameter_keyerror(self):
    	self.p.add_parameter("1","RandomValue")
        self.assertRaises(KeyError,self.p.add_parameter,"1","RandomValue")  # Fails if a KeyError is not raised
        # A KeyError should be raised because a parameter called 1 has already been created
        # Therefore this test should succeed
        
    def test_add_parameter_return(self):
        self.assertIsNotNone(self.p.add_parameter("1","RandomValue"))  # Fails if add_parameter doesn't return anything
        # Should return the newly added parameter, so the test should succeed

    def test_check_constraints(self):
        self.assertEqual(self.p.check_constraints(),True)  # Fails if any of the constraints is not satisfied
        
    def test_del_parameter(self):
        self.p.add_parameter("1","RandomValue",is_literal=True)
        self.assertEqual(self.p.del_parameter("1"),"RandomValue")  # Should return the removed parameter called 1
        
    def test_get_all_subs(self):
        self.assertIsNotNone(self.p.get_all_subs())  # Fails if get_all_subs doesn't return anything
        # Should return a dictionary containing all (parameter, value) pairs found
        
    def test_get_constraints(self):
        self.assertIsNotNone(self.p.get_constraints())  # Fails if get_constraints doesn't return anything
        # Should return a list containing all constraint expressions
        
    def test_get_name(self):
    	self.p.set_name("Hello_World")
        self.assertEqual(self.p.get_name(), "Hello_World")
        # Sets the name, and then checks it
        
    def test_get_parameter(self):
        self.assertRaises(KeyError,self.p.get_parameter("3")) # Fails if a KeyError is not raised
        # A KeyError should be raised because that parameter does not exist
        # Therefore this test should succeed
        # This method can be tested for further details

if __name__ == '__main__':
    unittest.main()
