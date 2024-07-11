import ast
import re
from main import CodeSage

class EnhancedCodeSage(CodeSage):
    def __init__(self, config):
        super().__init__(config)

    def check_line_length(self, tree):
        max_line_length = self.config.get('max_line_length', 79)
        with open(self.file_path, 'r') as file:
            for i, line in enumerate(file, 1):
                if len(line.rstrip()) > max_line_length:
                    self.issues.append({
                        "type": "line_length",
                        "message": f"Line is too long ({len(line.rstrip())} > {max_line_length} characters)",
                        "line": i
                    })

    def check_naming_conventions(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                self.issues.append({
                    "type": "class_naming",
                    "message": f"Class name '{node.name}' should use CamelCase",
                    "line": node.lineno
                })
            elif isinstance(node, ast.FunctionDef) and not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                self.issues.append({
                    "type": "function_naming",
                    "message": f"Function name '{node.name}' should use snake_case",
                    "line": node.lineno
                })

    def analyze_file(self, file_path):
        self.file_path = file_path
        issues = super().analyze_file(file_path)
        self.check_line_length(ast.parse(open(file_path).read()))
        self.check_naming_conventions(ast.parse(open(file_path).read()))
        return self.issues