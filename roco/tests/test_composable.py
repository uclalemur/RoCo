import sys
import os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from roco.api.composable import Composable  # Imports the Composable class
from roco.api.interface import Interface  # Imports the Interface class

class TestComposable(unittest.TestCase):
	def setUp(self):
        self.c = Composable()

    def test_new(self):
        self.assertIsInstance(self.c.new, Composable)  # Checks if c.new is an instance of the Composable class
        
    def test_add_interface(self):
    	inter = Interface()
        try:
			self.c.add_interface(inter)
			self.assertEqual(True,True)
		except:
			self.assertEqual(True,False)

if __name__ == '__main__':
    unittest.main()
