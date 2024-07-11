import ast
import os

class CodeSage:
    def __init__(self):
        self.issues = []

    def analyze_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        
        tree = ast.parse(content)
        self.check_function_length(tree)
        self.check_variable_naming(tree)
        self.check_import_style(tree)
        
        return self.issues

    def check_function_length(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:
                    self.issues.append(f"Function '{node.name}' is too long ({len(node.body)} lines). Consider breaking it down.")

    def check_variable_naming(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and not node.id.islower():
                self.issues.append(f"Variable '{node.id}' should be in lowercase with words separated by underscores.")

    def check_import_style(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                if any('*' in alias.name for alias in node.names):
                    self.issues.append(f"Avoid using 'from module import *'. It's better to import specific names.")

def main():
    sage = CodeSage()
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                issues = sage.analyze_file(file_path)
                if issues:
                    print(f"Issues in {file_path}:")
                    for issue in issues:
                        print(f"- {issue}")
                else:
                    print(f"No issues found in {file_path}")

if __name__ == "__main__":
    main()