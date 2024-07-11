import unittest
import ast
from src.main import CodeSage

class TestCodeSage(unittest.TestCase):
    def setUp(self):
        self.sage = CodeSage()

    def test_check_function_length(self):
        code = """
def long_function():
    pass
    pass
    # ... (repeat 'pass' 20 more times)
    pass
        """
        tree = ast.parse(code)
        self.sage.check_function_length(tree)
        self.assertEqual(len(self.sage.issues), 1)
        self.assertTrue("too long" in self.sage.issues[0])

    def test_check_variable_naming(self):
        code = "badVariableName = 10"
        tree = ast.parse(code)
        self.sage.check_variable_naming(tree)
        self.assertEqual(len(self.sage.issues), 1)
        self.assertTrue("should be in lowercase" in self.sage.issues[0])

    def test_check_import_style(self):
        code = "from module import *"
        tree = ast.parse(code)
        self.sage.check_import_style(tree)
        self.assertEqual(len(self.sage.issues), 1)
        self.assertTrue("Avoid using 'from module import *'" in self.sage.issues[0])

if __name__ == '__main__':
    unittest.main()