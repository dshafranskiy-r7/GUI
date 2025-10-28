# PortMaster Tests

This directory contains unit tests for the PortMaster project.

## Running Tests

### Run All Tests
```bash
# Run all tests in the harbourmaster module
python3 -m unittest tests.harbourmaster.test_harbour_load_ports -v
```

### Run Specific Test Class
```bash
python3 -m unittest tests.harbourmaster.test_harbour_load_ports.TestLoadPortsPhase1 -v
python3 -m unittest tests.harbourmaster.test_harbour_load_ports.TestLoadPortsPhase2 -v
```

### Run Specific Test Method
```bash
python3 -m unittest tests.harbourmaster.test_harbour_load_ports.TestLoadPortsPhase1.test_phase1_empty_port_files -v
```

### Run with Coverage
```bash
coverage run -m unittest tests.harbourmaster.test_harbour_load_ports
coverage report
coverage html  # Generate HTML report in htmlcov/
```

## Test Structure

```
tests/
├── __init__.py
├── README.md
└── harbourmaster/
    ├── __init__.py
    └── test_harbour_load_ports.py  # Tests for harbour.py load_ports phases
```

## Test Coverage

### test_harbour_load_ports.py
Tests for the refactored `load_ports()` method in `PortMaster/pylibs/harbourmaster/harbour.py`:

- **TestLoadPortsPhase1**: Tests Phase 1 - Loading *.port.json files
  - Empty port files
  - Single valid port
  - Port with None porter
  - Port with string porter (portsmd_fix lookup)
  - Port with optional items

- **TestLoadPortsPhase2**: Tests Phase 2 - Checking files/dirs in ports_dir
  - Empty ports directory
  - Skipping excluded files (gamelist.xml, etc.)
  - Skipping NO TOUCHY files
  - Handling known port files
  - Tracking unknown files
  - Tracking file renames

- **TestUtilFunctions**: Tests for utility functions
  - add_dict_list_unique with various inputs
  - get_dict_list with various inputs

## Requirements

The tests require the following dependencies:
- Python 3.9 or newer
- loguru (included in PortMaster/exlibs)
- coverage (for coverage reports)

Install test dependencies:
```bash
pip install -r requirements.txt
```

## Writing New Tests

When adding new tests:

1. Follow the existing test structure and naming conventions
2. Use unittest's built-in assertions
3. Mock external dependencies where appropriate
4. Test both success and failure cases
5. Include docstrings describing what each test verifies

Example:
```python
def test_my_feature(self):
    """Test that my feature handles valid input correctly"""
    # Setup
    input_data = {...}
    
    # Execute
    result = my_function(input_data)
    
    # Assert
    self.assertEqual(result, expected_value)
```
