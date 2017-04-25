import sys
import os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from roco.api.component import Component  # Imports the Component class
from roco.api.port import Port  # Imports the Port class

class TestComponent(unittest.TestCase):

    def setUp(self):
        self.c = Component()
        # Creates a single set-up code for all test cases that need an instance of Component
        # It is called for every single test case

    def test_add_connection(self):
    	self.assertRaises(Exception,self.c.add_connection,(from_subcomponent,from_interface),(to_subcomponent,to_interface))
    	# Assuming there should be an error if since the subcomponents have not been defined yet
    	
    def test_add_interface_valueerror(self):
        self.assertRaises(ValueError,self.p.add_interface,"invalid_name",Port())
        # A ValueError should be raised because the name cannot have underscores
        
    def test_get_all_defaults(self):
        ???
        
    def test_get_defaults(self):
        ???
        
    def test_get_interface(self):
    	p = Port()
    	self.c.add_interface("AnInterface",p)
        self.assertEqual(self.p.get_interface("AnInterface"), p) # Is this a correct comparison?
        # Adds an interface, and then checks it
        
    def test_get_component(self):
        ???
        
    def test_make(self):
        ???
    	

if __name__ == '__main__':
    unittest.main()
