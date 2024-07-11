import unittest
import ast
from src.main import CodeSage

class TestCodeSage(unittest.TestCase):
    def setUp(self):
        self.sage = CodeSage({
            'max_function_length': 20,
            'check_variable_naming': True,
            'check_import_style': True,
            'max_complexity': 10,
            'check_docstrings': True
        })

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
        self.assertTrue("too long" in self.sage.issues[0]['message'])

    def test_check_variable_naming(self):
        code = "badVariableName = 10"
        tree = ast.parse(code)
        self.sage.check_variable_naming(tree)
        self.assertEqual(len(self.sage.issues), 1)
        self.assertTrue("should be in lowercase" in self.sage.issues[0]['message'])

    def test_check_import_style(self):
        code = "from module import *"
        tree = ast.parse(code)
        self.sage.check_import_style(tree)
        self.assertEqual(len(self.sage.issues), 1)
        self.assertTrue("Avoid using 'from module import *'" in self.sage.issues[0]['message'])

    def test_check_docstrings(self):
        code = """
def function_without_docstring():
    pass

class ClassWithoutDocstring:
    def method_without_docstring(self):
        pass
        """
        tree = ast.parse(code)
        self.sage.check_docstrings(tree)
        self.assertEqual(len(self.sage.issues), 3)
        self.assertTrue(any("function 'function_without_docstring' is missing a docstring" in issue['message'].lower() for issue in self.sage.issues))
        self.assertTrue(any("class 'classwithoutdocstring' is missing a docstring" in issue['message'].lower() for issue in self.sage.issues))
        self.assertTrue(any("function 'method_without_docstring' is missing a docstring" in issue['message'].lower() for issue in self.sage.issues))

    def test_check_complexity(self):
        code = """
def complex_function(n):
    if n <= 1:
        return n
    elif n % 2 == 0:
        return complex_function(n // 2)
    else:
        return complex_function(3 * n + 1)
        """
        tree = ast.parse(code)
        self.sage.check_complexity(tree, 'test_file.py')
        self.assertEqual(len(self.sage.issues), 1)
        self.assertTrue("is too complex" in self.sage.issues[0]['message'])

if __name__ == '__main__':
    unittest.main()