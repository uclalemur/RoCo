import sys
import os
import unittest

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
        # Are there any other invalid characters?

    def test_get_interface(self):
    	p = Port()
    	self.c.add_interface("AnInterface",p)
        self.assertEqual(self.c.get_interface("AnInterface"), p) # Is this a correct comparison?
        # Adds an interface, and then checks it
        
    def test_get_subcomponent(self):
        self.c.add_subcomponent("TestSubcomponent", "Component")
        self.assertEqual(isinstance(self.c.get_subcomponent("TestSubcomponent"), Component()), True)
        
    def test_make(self):
        try:
	    self.c.make()
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
			
    def test_delete_subcomponent(self):
	self.c.add_subcomponent("TestSubcomponent", "Component")
        try:
	    self.c.delete_subcomponent("TestSubcomponent")
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
	    
    def test_delete_interface(self):
	p = Port()
    	self.c.add_interface("AnInterface",p)
        try:
	    self.c.delete_interface("AnInterface")
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
    	
    def test_define(self):
	try:
	    self.c.define()
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
			
    def test_to_yaml(self):
	# p = Port(); self.c.add_interface("AnInterface",p)
    	self.c.add_parameter("Width",79)
    	self.c.to_yaml("testfile")
    	c2 = Component()
    	c2.from_yaml("testfile")
	self.assertEqual(c2.get_parameter("Width"), 79)
	    
    def test_assemble(self):
	try:
	    self.c.assemble()
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
			
    def test_make(self):
	try:
	    self.c.make()
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
			
    def test_reset(self):
	try:
	    self.c.reset()
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
			
    def test_make_component_tree(self):
	try:
	    self.c.make_component_tree("FileName","TreeName")
	    self.assertEqual(True,True)
	except:
	    self.assertEqual(True,False)
			

if __name__ == '__main__':
    unittest.main()
