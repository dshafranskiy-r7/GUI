"""
Minimal unit tests for harbourmaster module.
Tests basic utility functions until import issues are resolved.
"""
import unittest
import sys
from pathlib import Path

# Add the PortMaster pylibs directory to the path
portmaster_base = Path(__file__).parent.parent.parent / 'PortMaster'
portmaster_pylibs = portmaster_base / 'pylibs'

sys.path.insert(0, str(portmaster_pylibs))

# Import after adding to path
try:
    from harbourmaster.util import add_dict_list_unique, get_dict_list
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False


@unittest.skipIf(not IMPORTS_AVAILABLE, "harbourmaster module not available")
class TestUtilFunctions(unittest.TestCase):
    """Test utility functions used by harbourmaster"""

    def test_add_dict_list_unique_new_key(self):
        """Test add_dict_list_unique with a new key"""
        base_dict = {}
        add_dict_list_unique(base_dict, 'key1', 'value1')
        self.assertEqual(base_dict['key1'], 'value1')

    def test_add_dict_list_unique_existing_string(self):
        """Test add_dict_list_unique with existing string value"""
        base_dict = {'key1': 'value1'}
        add_dict_list_unique(base_dict, 'key1', 'value2')
        self.assertEqual(base_dict['key1'], ['value1', 'value2'])

    def test_add_dict_list_unique_existing_list(self):
        """Test add_dict_list_unique with existing list value"""
        base_dict = {'key1': ['value1']}
        add_dict_list_unique(base_dict, 'key1', 'value2')
        self.assertEqual(base_dict['key1'], ['value1', 'value2'])

    def test_add_dict_list_unique_duplicate(self):
        """Test add_dict_list_unique with duplicate value"""
        base_dict = {'key1': ['value1']}
        add_dict_list_unique(base_dict, 'key1', 'value1')
        self.assertEqual(base_dict['key1'], ['value1'])

    def test_get_dict_list_missing_key(self):
        """Test get_dict_list with missing key"""
        base_dict = {}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, [])

    def test_get_dict_list_string_value(self):
        """Test get_dict_list with string value"""
        base_dict = {'key1': 'value1'}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, ['value1'])

    def test_get_dict_list_list_value(self):
        """Test get_dict_list with list value"""
        base_dict = {'key1': ['value1', 'value2']}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, ['value1', 'value2'])

    def test_get_dict_list_none_value(self):
        """Test get_dict_list with None value"""
        base_dict = {'key1': None}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
