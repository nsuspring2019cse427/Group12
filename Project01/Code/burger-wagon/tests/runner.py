import os
import unittest

loader = unittest.TestLoader()
tests_dir = os.path.abspath(os.path.dirname(__file__))
suite = loader.discover(tests_dir)

runner = unittest.TextTestRunner(verbosity=50)


if __name__ == '__main__':
    runner.run(suite)
