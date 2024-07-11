import ast
import os
import argparse
import yaml

class CodeSage:
    def __init__(self, config):
        self.issues = []
        self.config = config

    def analyze_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        
        tree = ast.parse(content)
        self.check_function_length(tree)
        self.check_variable_naming(tree)
        self.check_import_style(tree)
        
        return self.issues

    def check_function_length(self, tree):
        max_length = self.config.get('max_function_length', 20)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > max_length:
                    self.issues.append(f"Function '{node.name}' is too long ({len(node.body)} lines). Consider breaking it down.")

    def check_variable_naming(self, tree):
        if not self.config.get('check_variable_naming', True):
            return
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and not node.id.islower():
                self.issues.append(f"Variable '{node.id}' should be in lowercase with words separated by underscores.")

    def check_import_style(self, tree):
        if not self.config.get('check_import_style', True):
            return
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                if any('*' in alias.name for alias in node.names):
                    self.issues.append(f"Avoid using 'from module import *'. It's better to import specific names.")

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="CodeSage: A Code Review Assistant")
    parser.add_argument('path', help="Path to the file or directory to analyze")
    parser.add_argument('-c', '--config', default='config.yaml', help="Path to the configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    sage = CodeSage(config)

    if os.path.isfile(args.path):
        files = [args.path]
    else:
        files = [os.path.join(root, file) for root, _, files in os.walk(args.path) for file in files if file.endswith('.py')]

    for file_path in files:
        issues = sage.analyze_file(file_path)
        if issues:
            print(f"Issues in {file_path}:")
            for issue in issues:
                print(f"- {issue}")
        else:
            print(f"No issues found in {file_path}")

if __name__ == "__main__":
    main()