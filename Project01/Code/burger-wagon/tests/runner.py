import os
import unittest

""" This is a test suite that tests integration of all modules and tests. Automates the boring stuffs. """

loader = unittest.TestLoader()
tests_dir = os.path.abspath(os.path.dirname(__file__))
suite = loader.discover(tests_dir)

runner = unittest.TextTestRunner(verbosity=50)


if __name__ == '__main__':
    runner.run(suite)
