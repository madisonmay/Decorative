import unittest

from decorative import typecheck, TypeCheckError


@typecheck(a=float, b=float)
def f(a, b):
    return a / b


class TypeCheckTestCase(unittest.TestCase):

    def test_typecheck(self):
        
        # valid inputs
        self.assertEqual(f(1., 2.), 0.5)

        # invalid inputs
        with self.assertRaises(TypeCheckError):
            f(1, 2)
        with self.assertRaises(TypeCheckError):
            f("one", "two")
