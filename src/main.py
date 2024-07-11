import ast
import os
import argparse
import yaml
import json
from mccabe import PathGraphingAstVisitor

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
        self.check_complexity(tree, file_path)
        self.check_docstrings(tree)
        
        return self.issues

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
        if not self.config.get('check_variable_naming', True):
            return
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and not node.id.islower():
                self.issues.append({
                    "type": "variable_naming",
                    "message": f"Variable '{node.id}' should be in lowercase with words separated by underscores.",
                    "line": node.lineno
                })

    def check_import_style(self, tree):
        if not self.config.get('check_import_style', True):
            return
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                if any('*' in alias.name for alias in node.names):
                    self.issues.append({
                        "type": "import_style",
                        "message": f"Avoid using 'from module import *'. It's better to import specific names.",
                        "line": node.lineno
                    })

    def check_complexity(self, tree, filename):
        max_complexity = self.config.get('max_complexity', 10)
        visitor = PathGraphingAstVisitor()
        visitor.preorder(tree, visitor)
        for graph in visitor.graphs.values():
            if graph.complexity() > max_complexity:
                self.issues.append({
                    "type": "complexity",
                    "message": f"Function '{graph.entity}' is too complex (complexity: {graph.complexity()})",
                    "line": graph.lineno
                })

    def check_docstrings(self, tree):
        if not self.config.get('check_docstrings', True):
            return
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if not ast.get_docstring(node):
                    node_type = type(node).__name__.lower().replace('def', '')
                    if isinstance(node, ast.Module):
                        line_num = 1
                        name = 'module'
                    else:
                        line_num = node.lineno
                        name = node.name
                    self.issues.append({
                        "type": "missing_docstring",
                        "message": f"{node_type.capitalize()} '{name}' is missing a docstring.",
                        "line": line_num
                    })

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="CodeSage: A Code Review Assistant")
    parser.add_argument('path', help="Path to the file or directory to analyze")
    parser.add_argument('-c', '--config', default='config.yaml', help="Path to the configuration file")
    parser.add_argument('-f', '--format', choices=['text', 'json', 'html'], default='text', help="Output format")
    parser.add_argument('-o', '--output', help="Output file for JSON or HTML format")
    parser.add_argument('--check-coverage', action='store_true', help="Check test coverage")
    args = parser.parse_args()

    # ... rest of the main function ...
    config = load_config(args.config)
    sage = CodeSage(config)

    if os.path.isfile(args.path):
        files = [args.path]
    else:
        files = [os.path.join(root, file) for root, _, files in os.walk(args.path) for file in files if file.endswith('.py')]

    results = {}
    for file_path in files:
        issues = sage.analyze_file(file_path)
        results[file_path] = issues

    if args.format == 'text':
        for file_path, issues in results.items():
            print(f"Issues in {file_path}:")
            if issues:
                for issue in issues:
                    print(f"- Line {issue['line']}: [{issue['type']}] {issue['message']}")
            else:
                print("No issues found.")
            print()
    elif args.format == 'json':
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()