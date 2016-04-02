import sys
import unittest
from StringIO import StringIO

from decorative import debug


@debug
def f(a, b):
    return a + b


class DebugTestCase(unittest.TestCase):

    def test_debug(self):
        
        saved_stdout = sys.stdout
        try:
            fake_stdout = StringIO()
            sys.stdout = fake_stdout

            f(1, 2)
            output = fake_stdout.getvalue().strip()
            assert output == "f(a=1, b=2) --> 3" 
        finally:
            sys.stdout = saved_stdout
