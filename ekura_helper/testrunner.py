import unittest

loader = unittest.TestLoader()
start_dir = 'ekura_helper/tests'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)