# PortMaster Tests

This directory contains the test suite for PortMaster.

## Running Tests

### Run all tests
```bash
python3 -m unittest discover tests -v
```

### Run a specific test file
```bash
python3 -m unittest tests.test_util -v
```

### Run a specific test class
```bash
python3 -m unittest tests.test_util.TestNiceSize -v
```

### Run a specific test method
```bash
python3 -m unittest tests.test_util.TestNiceSize.test_bytes -v
```

## Test Coverage

To run tests with coverage:
```bash
pip install coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generate HTML report
```

## Test Structure

- `test_util.py` - Tests for utility functions (nice_size, version_parse, etc.)
- `test_config.py` - Tests for configuration module
- More test files will be added as the test suite expands

## Writing Tests

Tests should:
1. Follow the existing naming convention (`test_*.py`)
2. Use descriptive test method names
3. Include docstrings explaining what is being tested
4. Be independent and not rely on execution order
5. Clean up any resources they create
