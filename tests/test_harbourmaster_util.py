# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/harbourmaster/util.py
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add PortMaster/pylibs to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))

from harbourmaster import util


class TestJsonFunctions(unittest.TestCase):
    """Test JSON loading functions"""

    def test_json_safe_loads_valid(self):
        """Test json_safe_loads with valid JSON"""
        result = util.json_safe_loads('{"key": "value"}')
        self.assertEqual(result, {"key": "value"})

    def test_json_safe_loads_invalid(self):
        """Test json_safe_loads with invalid JSON"""
        result = util.json_safe_loads('not valid json')
        self.assertIsNone(result)

    def test_json_safe_load_valid(self):
        """Test json_safe_load with valid JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump({"test": "data"}, f)
            temp_file = f.name

        try:
            with open(temp_file, 'r') as f:
                result = util.json_safe_load(f)
            self.assertEqual(result, {"test": "data"})
        finally:
            os.unlink(temp_file)

    def test_json_safe_load_invalid(self):
        """Test json_safe_load with invalid JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("not valid json")
            temp_file = f.name

        try:
            with open(temp_file, 'r') as f:
                result = util.json_safe_load(f)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_file)


class TestFetchFunctions(unittest.TestCase):
    """Test fetch functions"""

    @patch('harbourmaster.util.requests.get')
    def test_fetch_success(self, mock_get):
        """Test fetch with successful response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = util.fetch("http://example.com")
        self.assertIsNotNone(result)
        self.assertEqual(result.status_code, 200)

    @patch('harbourmaster.util.requests.get')
    def test_fetch_failure(self, mock_get):
        """Test fetch with failed response"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = util.fetch("http://example.com")
        self.assertIsNone(result)

    @patch('harbourmaster.util.requests.get')
    def test_fetch_connection_error(self, mock_get):
        """Test fetch with connection error"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result = util.fetch("http://example.com")
        self.assertIsNone(result)

    @patch('harbourmaster.util.fetch')
    def test_fetch_data(self, mock_fetch):
        """Test fetch_data"""
        mock_response = MagicMock()
        mock_response.content = b"test content"
        mock_fetch.return_value = mock_response

        result = util.fetch_data("http://example.com")
        self.assertEqual(result, b"test content")

    @patch('harbourmaster.util.fetch')
    def test_fetch_json(self, mock_fetch):
        """Test fetch_json"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_fetch.return_value = mock_response

        result = util.fetch_json("http://example.com")
        self.assertEqual(result, {"test": "data"})

    @patch('harbourmaster.util.fetch')
    def test_fetch_text(self, mock_fetch):
        """Test fetch_text"""
        mock_response = MagicMock()
        mock_response.text = "test text"
        mock_fetch.return_value = mock_response

        result = util.fetch_text("http://example.com")
        self.assertEqual(result, "test text")

    @patch('harbourmaster.util.fetch')
    def test_fetch_data_none(self, mock_fetch):
        """Test fetch_data returns None when fetch fails"""
        mock_fetch.return_value = None

        result = util.fetch_data("http://example.com")
        self.assertIsNone(result)


class TestNiceSize(unittest.TestCase):
    """Test nice_size function"""

    def test_nice_size_bytes(self):
        """Test nice_size with bytes"""
        result = util.nice_size(100)
        self.assertEqual(result, "100 B")

    def test_nice_size_kilobytes(self):
        """Test nice_size with kilobytes"""
        result = util.nice_size(1024)
        self.assertIn("KB", result)

    def test_nice_size_megabytes(self):
        """Test nice_size with megabytes"""
        result = util.nice_size(1024 * 1024)
        self.assertIn("MB", result)

    def test_nice_size_gigabytes(self):
        """Test nice_size with gigabytes"""
        result = util.nice_size(1024 * 1024 * 1024)
        self.assertIn("GB", result)

    def test_nice_size_zero(self):
        """Test nice_size with zero"""
        result = util.nice_size(0)
        self.assertEqual(result, "0 B")


class TestOxfordCommaJoin(unittest.TestCase):
    """Test oc_join function"""

    def test_oc_join_empty(self):
        """Test oc_join with empty list"""
        result = util.oc_join([])
        self.assertEqual(result, "")

    def test_oc_join_single(self):
        """Test oc_join with single item"""
        result = util.oc_join(["item1"])
        self.assertEqual(result, "item1")

    def test_oc_join_two(self):
        """Test oc_join with two items"""
        result = util.oc_join(["item1", "item2"])
        self.assertEqual(result, "item1 and item2")

    def test_oc_join_three(self):
        """Test oc_join with three items"""
        result = util.oc_join(["item1", "item2", "item3"])
        self.assertEqual(result, "item1, item2, and item3")

    def test_oc_join_multiple(self):
        """Test oc_join with multiple items"""
        result = util.oc_join(["a", "b", "c", "d"])
        self.assertEqual(result, "a, b, c, and d")


class TestVersionParse(unittest.TestCase):
    """Test version_parse function"""

    def test_version_parse_simple(self):
        """Test version_parse with simple version"""
        result = util.version_parse("1.0.0")
        self.assertEqual(result, (1, 0, 0))

    def test_version_parse_with_suffix(self):
        """Test version_parse with suffix"""
        result = util.version_parse("1.0.0-beta")
        self.assertIn(1, result)
        self.assertIn("beta", result)

    def test_version_parse_complex(self):
        """Test version_parse with complex version"""
        result = util.version_parse("2.1.3-alpha2")
        self.assertGreater(len(result), 0)

    def test_version_parse_cache(self):
        """Test that version_parse uses cache"""
        # Call twice with same value
        result1 = util.version_parse("1.0.0")
        result2 = util.version_parse("1.0.0")
        self.assertEqual(result1, result2)


class TestNameCleaner(unittest.TestCase):
    """Test name_cleaner function"""

    def test_name_cleaner_basic(self):
        """Test name_cleaner with basic string"""
        result = util.name_cleaner("Test Name")
        self.assertEqual(result, "test.name")

    def test_name_cleaner_special_chars(self):
        """Test name_cleaner removes special characters"""
        result = util.name_cleaner("Test@Name#123")
        self.assertEqual(result, "testname123")

    def test_name_cleaner_spaces(self):
        """Test name_cleaner converts spaces to dots"""
        result = util.name_cleaner("Test  Name  Here")
        self.assertEqual(result, "test.name.here")

    def test_name_cleaner_lowercase(self):
        """Test name_cleaner converts to lowercase"""
        result = util.name_cleaner("UPPERCASE")
        self.assertEqual(result, "uppercase")


class TestPMSignatureFunctions(unittest.TestCase):
    """Test PM signature functions"""

    def test_load_pm_signature_nonexistent(self):
        """Test load_pm_signature with non-existent file"""
        result = util.load_pm_signature("/nonexistent/file.sh")
        self.assertIsNone(result)

    def test_load_pm_signature_wrong_extension(self):
        """Test load_pm_signature with wrong file extension"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test")
            temp_file = f.name

        try:
            result = util.load_pm_signature(temp_file)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_file)

    def test_load_pm_signature_valid(self):
        """Test load_pm_signature with valid signature"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            f.write("#!/bin/bash\n")
            f.write("# PORTMASTER: test, signature\n")
            f.write("echo 'test'\n")
            temp_file = f.name

        try:
            result = util.load_pm_signature(temp_file)
            self.assertEqual(result, ["test", "signature"])
        finally:
            os.unlink(temp_file)

    def test_load_pm_signature_no_signature(self):
        """Test load_pm_signature with no signature"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'test'\n")
            temp_file = f.name

        try:
            result = util.load_pm_signature(temp_file)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_file)

    def test_add_pm_signature_new(self):
        """Test add_pm_signature adds new signature"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'test'\n")
            temp_file = f.name

        try:
            util.add_pm_signature(temp_file, ["new", "signature"])
            result = util.load_pm_signature(temp_file)
            self.assertEqual(result, ["new", "signature"])
        finally:
            os.unlink(temp_file)

    def test_add_pm_signature_replace(self):
        """Test add_pm_signature replaces existing signature"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            f.write("#!/bin/bash\n")
            f.write("# PORTMASTER: old, signature\n")
            f.write("echo 'test'\n")
            temp_file = f.name

        try:
            util.add_pm_signature(temp_file, ["new", "signature"])
            result = util.load_pm_signature(temp_file)
            self.assertEqual(result, ["new", "signature"])
        finally:
            os.unlink(temp_file)

    def test_remove_pm_signature(self):
        """Test remove_pm_signature removes signature"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            f.write("#!/bin/bash\n")
            f.write("# PORTMASTER: test, signature\n")
            f.write("echo 'test'\n")
            temp_file = f.name

        try:
            util.remove_pm_signature(temp_file)
            result = util.load_pm_signature(temp_file)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
