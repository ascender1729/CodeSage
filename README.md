# CodeSage

CodeSage is an intelligent code review assistant designed to enhance the software development process. It provides automated insights, best practice suggestions, and helps maintain code quality across projects.

## Features

- Function length check
- Variable naming convention check
- Import style check
- Complexity check using McCabe metric
- Command-line interface for easy use
- Multiple output formats (text, JSON, HTML)
- Git integration for automated pull request analysis

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ascender1729/CodeSage.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command-line Usage

You can run CodeSage from the command line:

```
python src/main.py [path] [-c CONFIG] [-f {text,json,html}] [-o OUTPUT]
```

Arguments:
- `path`: Path to the file or directory to analyze (required)
- `-c CONFIG`, `--config CONFIG`: Path to the configuration file (optional, defaults to 'config.yaml')
- `-f {text,json,html}`, `--format {text,json,html}`: Output format (optional, defaults to 'text')
- `-o OUTPUT`, `--output OUTPUT`: Output file for JSON or HTML format (optional)

Examples:
1. Analyze a single file with text output:
   ```
   python src/main.py path/to/your/file.py
   ```
2. Analyze an entire directory with JSON output:
   ```
   python src/main.py path/to/your/project/ -f json -o report.json
   ```
3. Use a custom configuration file and generate an HTML report:
   ```
   python src/main.py path/to/your/project/ -c path/to/custom_config.yaml -f html -o report.html
   ```

### Git Integration

To use CodeSage for automated pull request analysis, you need to set up the following environment variables:

- `REPO_PATH`: Path to the local repository
- `BASE_BRANCH`: Base branch of the pull request (default is 'main')
- `HEAD_BRANCH`: Head branch of the pull request
- `GITHUB_TOKEN`: Your GitHub personal access token
- `REPO_NAME`: Name of the repository in the format 'owner/repo'
- `PR_NUMBER`: Number of the pull request

Then run:

```
python src/git_integration.py
```

This will analyze the changes in the pull request and post the results as a comment on the pull request.

## Configuration

You can modify the `config.yaml` file to adjust the behavior of CodeSage. The default configuration is:

```yaml
max_function_length: 20
check_variable_naming: true
check_import_style: true
max_complexity: 10
```

## Running Tests

To run the unit tests:

```
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.