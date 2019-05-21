import sys
import os

# Set root folder one level up, just for this example
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import unittest

#Import the function that we want to test
from calculate_chart import plot_psychro

class TestBuildingSim(unittest.TestCase):

	def test_T_MRT_forced_psy(self):
		graph1_url, T_MRT_forced_psy = plot_psychro();

		#Just testing two numbers from the T_MRT_forced_psy array and comparing them to their "true" values
		self.assertEqual(round(T_MRT_forced_psy[1,3], 5), 20.98606)
		self.assertEqual(round(T_MRT_forced_psy[5,9], 5), 21.05975)



if __name__ == '__main__':
    unittest.main()