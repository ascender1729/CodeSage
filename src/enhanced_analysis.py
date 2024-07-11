import ast
import re

class EnhancedCodeSage:
    def __init__(self, config):
        self.config = config
        self.issues = []

    def analyze_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        
        tree = ast.parse(content)
        self.check_function_length(tree)
        self.check_variable_naming(tree)
        self.check_import_style(tree)
        self.check_complexity(tree)
        self.check_docstrings(tree)
        self.check_line_length(content)
        self.check_function_naming(tree)
        self.check_class_naming(tree)
        
        return self.issues

    # ... (include all previous check methods)

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