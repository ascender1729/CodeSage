import ast
import re

class EnhancedCodeSage:
    def __init__(self, config):
        self.config = config
        self.issues = []

    def analyze_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            self.issues.append({
                "type": "syntax_error",
                "message": f"SyntaxError: {str(e)}",
                "line": e.lineno
            })
            return self.issues

        self.check_function_length(tree)
        self.check_variable_naming(tree)
        self.check_import_style(tree)
        self.check_complexity(tree)
        self.check_docstrings(tree)
        self.check_line_length(content)
        self.check_function_naming(tree)
        self.check_class_naming(tree)
        
        return self.issues

    # ... (rest of the methods remain the same)
    def check_function_length(self, tree):
        max_length = self.config.get('max_function_length', 20)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > max_length:
                    self.issues.append({
                        "type": "function_length",
                        "message": f"Function '{node.name}' is too long ({len(node.body)} lines). Consider breaking it down.",
                        "line": node.lineno
                    })

    def check_variable_naming(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and not node.id.islower():
                self.issues.append({
                    "type": "variable_naming",
                    "message": f"Variable '{node.id}' should be in lowercase with words separated by underscores.",
                    "line": node.lineno
                })

    def check_import_style(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                if any('*' in alias.name for alias in node.names):
                    self.issues.append({
                        "type": "import_style",
                        "message": f"Avoid using 'from module import *'. It's better to import specific names.",
                        "line": node.lineno
                    })

    def check_complexity(self, tree):
        max_complexity = self.config.get('max_complexity', 10)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.comprehension, ast.Try, ast.ExceptHandler)):
                        complexity += 1
                if complexity > max_complexity:
                    self.issues.append({
                        "type": "complexity",
                        "message": f"Function '{node.name}' is too complex (complexity: {complexity}). Consider refactoring.",
                        "line": node.lineno
                    })

    def check_docstrings(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if not ast.get_docstring(node):
                    node_type = type(node).__name__.lower().replace('def', '')
                    name = getattr(node, 'name', 'module')
                    self.issues.append({
                        "type": "missing_docstring",
                        "message": f"{node_type.capitalize()} '{name}' is missing a docstring.",
                        "line": getattr(node, 'lineno', 1)
                    })

    def check_line_length(self, content):
        max_line_length = self.config.get('max_line_length', 79)
        for i, line in enumerate(content.split('\n'), 1):
            if len(line) > max_line_length:
                self.issues.append({
                    "type": "line_length",
                    "message": f"Line is too long ({len(line)} > {max_line_length} characters)",
                    "line": i
                })

    def check_function_naming(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                self.issues.append({
                    "type": "function_naming",
                    "message": f"Function name '{node.name}' should use snake_case",
                    "line": node.lineno
                })

    def check_class_naming(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                self.issues.append({
                    "type": "class_naming",
                    "message": f"Class name '{node.name}' should use CamelCase",
                    "line": node.lineno
                })