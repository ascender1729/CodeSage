# CodeSage

CodeSage is an intelligent code review assistant designed to enhance the software development process. It provides automated insights, best practice suggestions, and helps maintain code quality across projects.

## Features

- Function length check
- Variable naming convention check
- Import style check
- Command-line interface for easy use

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

You can run CodeSage from the command line:

```
python src/main.py [path] [-c CONFIG]
```

Arguments:
- `path`: Path to the file or directory to analyze (required)
- `-c CONFIG`, `--config CONFIG`: Path to the configuration file (optional, defaults to 'config.yaml')

Examples:
1. Analyze a single file:
   ```
   python src/main.py path/to/your/file.py
   ```
2. Analyze an entire directory:
   ```
   python src/main.py path/to/your/project/
   ```
3. Use a custom configuration file:
   ```
   python src/main.py path/to/your/project/ -c path/to/custom_config.yaml
   ```

## Configuration

You can modify the `config.yaml` file to adjust the behavior of CodeSage. The default configuration is:

```yaml
max_function_length: 20
check_variable_naming: true
check_import_style: true
```

## Running Tests

To run the unit tests:

```
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.