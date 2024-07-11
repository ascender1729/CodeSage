from math import *

def LongFunctionNameWithManyLines():
    """This function is intentionally long and does nothing useful."""
    x = 1
    y = 2
    z = 3
    a = 4
    b = 5
    c = 6
    d = 7
    e = 8
    f = 9
    g = 10
    h = 11
    i = 12
    j = 13
    k = 14
    l = 15
    m = 16
    n = 17
    o = 18
    p = 19
    q = 20
    r = 21
    return x + y + z + a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r

def complex_function(n):
    if n <= 1:
        return n
    elif n % 2 == 0:
        return complex_function(n // 2)
    else:
        return complex_function(3 * n + 1)

class undocumented_class:
    def __init__(self):
        self.BadlyNamedVariable = 42

    def undocumented_method(self):
        pass

GLOBAL_CONSTANT = 10

def function_without_docstring():
    print("This function has no docstring")

very_long_line = "This is a very long line that exceeds the maximum line length and should trigger a line length warning in our enhanced analysis."

if __name__ == "__main__":
    print(LongFunctionNameWithManyLines())
    print(complex_function(27))
    obj = undocumented_class()
    obj.undocumented_method()
    function_without_docstring()