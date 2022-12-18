import os
import gzip, pickle

import unittest

from tools.handler import readLocalData
from tools.handler import writeLocalData

class TestHandler(unittest.TestCase):
    def testWritingAndReading(self):
        '''Test the writing and reading functions of the handler.py script.
        '''
        test_data = {
            'VAR1': 'simple_string',
            'VAR2': ['a', 'list'],
            'VAR3': {'a':'dictionary'},
            'VAR4': (True, False, False),
        }
        test_path = 'ekura_helper/test_file.py'
        writeLocalData(test_data, test_path)
        red_data = readLocalData(test_path)
        os.remove(test_path) # Delete the temporary file
        self.assertEqual(test_data, red_data)

if __name__ == '__main__':
    unittest.main()