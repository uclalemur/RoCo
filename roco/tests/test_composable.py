import sys
import os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from api.composable import Composable  # imports the Composable class

class TestComposable(unittest.TestCase):

    def test_new(self):
    	c = Composable()
        self.assertIsInstance(c, Composable)  # checks if c is an instance of the Composable class

if __name__ == '__main__':
    unittest.main()
    