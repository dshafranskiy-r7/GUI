# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/utility.py
"""

import io
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add PortMaster/pylibs to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))

import utility


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""

    def test_to_str_with_string(self):
        """Test to_str with string input"""
        result = utility.to_str("hello")
        self.assertEqual(result, "hello")

    def test_to_str_with_int(self):
        """Test to_str with integer input"""
        result = utility.to_str(42)
        self.assertEqual(result, "42")

    def test_to_str_with_none(self):
        """Test to_str with None input"""
        result = utility.to_str(None)
        self.assertEqual(result, "None")

    @patch('os.isatty')
    def test_in_terminal_true(self, mock_isatty):
        """Test in_terminal returns True when in terminal"""
        mock_isatty.return_value = True
        result = utility.in_terminal()
        self.assertTrue(result)

    @patch('os.isatty')
    def test_in_terminal_false(self, mock_isatty):
        """Test in_terminal returns False when not in terminal"""
        mock_isatty.return_value = False
        result = utility.in_terminal()
        self.assertFalse(result)

    def test_do_color_enable(self):
        """Test do_color enables color output"""
        utility.do_color(True)
        # Just ensure it doesn't crash
        self.assertTrue(True)

    def test_do_color_disable(self):
        """Test do_color disables color output"""
        utility.do_color(False)
        # Just ensure it doesn't crash
        self.assertTrue(True)

    def test_cstrip_removes_ansi(self):
        """Test cstrip removes ANSI codes"""
        result = utility.cstrip("<b>bold text</b>")
        self.assertEqual(result, "bold text")

    def test_cprint_to_string_io(self):
        """Test cprint outputs to string buffer"""
        output = io.StringIO()
        utility.cprint("test message", file=output)
        result = output.getvalue()
        self.assertIn("test message", result)

    def test_do_cprint_output(self):
        """Test setting custom output file handle"""
        output = io.StringIO()
        utility.do_cprint_output(output)
        utility.cprint("test")
        result = output.getvalue()
        self.assertIn("test", result)
        # Reset to None
        utility.do_cprint_output(None)


if __name__ == '__main__':
    unittest.main()
