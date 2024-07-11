import ast
import os
import argparse
import yaml
import json
from mccabe import PathGraphingAstVisitor
from jinja2 import Template
import coverage

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

def check_test_coverage(path):
    cov = coverage.Coverage()
    cov.start()

    # Run the tests
    import unittest
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(path)
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)

    cov.stop()
    cov.save()

    total_coverage = cov.report()
    return total_coverage

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def generate_html_report(results):
    template = Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CodeSage Report</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .file { margin-bottom: 20px; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
            .file h2 { margin-top: 0; color: #34495e; }
            .issue { margin-bottom: 10px; }
            .issue-type { font-weight: bold; color: #e74c3c; }
        </style>
    </head>
    <body>
        <h1>CodeSage Report</h1>
        {% for file, issues in results.items() %}
        <div class="file">
            <h2>{{ file }}</h2>
            {% if issues %}
                {% for issue in issues %}
                <div class="issue">
                    <span class="issue-type">[{{ issue.type }}]</span> Line {{ issue.line }}: {{ issue.message }}
                </div>
                {% endfor %}
            {% else %}
                <p>No issues found.</p>
            {% endif %}
        </div>
        {% endfor %}
        {% if results.test_coverage %}
        <div class="file">
            <h2>Test Coverage</h2>
            <p>Overall test coverage: {{ results.test_coverage }}</p>
        </div>
        {% endif %}
    </body>
    </html>
    ''')
    return template.render(results=results)

def main():
    parser = argparse.ArgumentParser(description="CodeSage: A Code Review Assistant")
    parser.add_argument('path', help="Path to the file or directory to analyze")
    parser.add_argument('-c', '--config', default='config.yaml', help="Path to the configuration file")
    parser.add_argument('-f', '--format', choices=['text', 'json', 'html'], default='text', help="Output format")
    parser.add_argument('-o', '--output', help="Output file for JSON or HTML format")
    parser.add_argument('--check-coverage', action='store_true', help="Check test coverage")
    args = parser.parse_args()

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

    if args.check_coverage:
        coverage = check_test_coverage(args.path)
        results['test_coverage'] = f"{coverage:.2f}%"

    if args.format == 'text':
        for file_path, issues in results.items():
            if file_path == 'test_coverage':
                print(f"Test coverage: {issues}")
            else:
                print(f"Issues in {file_path}:")
                if issues:
                    for issue in issues:
                        print(f"- Line {issue['line']}: [{issue['type']}] {issue['message']}")
                else:
                    print("No issues found.")
            print()
    elif args.format == 'json':
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
        else:
            print(json.dumps(results, indent=2))
    elif args.format == 'html':
        html_report = generate_html_report(results)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(html_report)
        else:
            print(html_report)

if __name__ == "__main__":
    main()