#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

"""
Tests for harbourmaster.util module
"""

import sys
import unittest
from pathlib import Path

# Add PortMaster modules to path
PORTMASTER_DIR = Path(__file__).parent.parent / "PortMaster"
sys.path.insert(0, str(PORTMASTER_DIR / "pylibs"))
sys.path.insert(0, str(PORTMASTER_DIR / "exlibs"))

from harbourmaster.util import (
    nice_size,
    oc_join,
    version_parse,
    name_cleaner,
)


class TestNiceSize(unittest.TestCase):
    """Test the nice_size function"""

    def test_bytes(self):
        """Test byte formatting"""
        self.assertEqual(nice_size(0), "0 B")
        self.assertEqual(nice_size(100), "100 B")
        self.assertEqual(nice_size(767), "767 B")

    def test_kilobytes(self):
        """Test kilobyte formatting"""
        self.assertEqual(nice_size(1024), "1.00 KB")
        self.assertEqual(nice_size(2048), "2.00 KB")
        # Test the threshold behavior (768 KB transitions to next unit)
        self.assertEqual(nice_size(500 * 1024), "500.00 KB")

    def test_megabytes(self):
        """Test megabyte formatting"""
        self.assertEqual(nice_size(1024 * 1024), "1.00 MB")
        self.assertEqual(nice_size(10 * 1024 * 1024), "10.00 MB")

    def test_gigabytes(self):
        """Test gigabyte formatting"""
        self.assertEqual(nice_size(1024 * 1024 * 1024), "1.00 GB")

    def test_terabytes(self):
        """Test terabyte formatting"""
        self.assertEqual(nice_size(1024 * 1024 * 1024 * 1024), "1.00 TB")


class TestOxfordCommaJoin(unittest.TestCase):
    """Test the oc_join (Oxford comma join) function"""

    def test_empty_list(self):
        """Test empty list"""
        self.assertEqual(oc_join([]), "")

    def test_single_item(self):
        """Test single item"""
        self.assertEqual(oc_join(["apple"]), "apple")

    def test_two_items(self):
        """Test two items"""
        self.assertEqual(oc_join(["apple", "banana"]), "apple and banana")

    def test_three_items(self):
        """Test three items with Oxford comma"""
        self.assertEqual(oc_join(["apple", "banana", "cherry"]), "apple, banana, and cherry")

    def test_four_items(self):
        """Test four items with Oxford comma"""
        self.assertEqual(
            oc_join(["apple", "banana", "cherry", "date"]),
            "apple, banana, cherry, and date"
        )


class TestVersionParse(unittest.TestCase):
    """Test the version_parse function"""

    def test_simple_version(self):
        """Test simple numeric version"""
        self.assertEqual(version_parse("1.0"), (1, 0))
        self.assertEqual(version_parse("1.2.3"), (1, 2, 3))

    def test_version_with_suffix(self):
        """Test version with text suffix"""
        self.assertEqual(version_parse("1.0beta"), (1, 0, "beta"))
        self.assertEqual(version_parse("2.1.0-rc1"), (2, 1, 0, "rc", 1))

    def test_complex_version(self):
        """Test complex version strings"""
        result = version_parse("1.2.3-alpha.4")
        self.assertEqual(result, (1, 2, 3, "alpha", 4))

    def test_version_caching(self):
        """Test that version_parse caches results"""
        # Call twice with same input
        result1 = version_parse("1.0.0")
        result2 = version_parse("1.0.0")
        # Should be the same object due to caching
        self.assertIs(result1, result2)


class TestNameCleaner(unittest.TestCase):
    """Test the name_cleaner function"""

    def test_simple_name(self):
        """Test simple name cleaning"""
        self.assertEqual(name_cleaner("Half Life"), "half.life")
        self.assertEqual(name_cleaner("Doom II"), "doom.ii")

    def test_special_characters(self):
        """Test removal of special characters"""
        self.assertEqual(name_cleaner("Game: The Adventure"), "game.the.adventure")
        self.assertEqual(name_cleaner("Test@Game#123"), "testgame123")

    def test_multiple_spaces(self):
        """Test multiple spaces collapsed to single dot"""
        self.assertEqual(name_cleaner("A   B   C"), "a.b.c")

    def test_dots_and_spaces(self):
        """Test dots and spaces handling"""
        self.assertEqual(name_cleaner("Half.Life 2"), "half.life.2")

    def test_caching(self):
        """Test that name_cleaner caches results"""
        result1 = name_cleaner("Test Game")
        result2 = name_cleaner("Test Game")
        self.assertIs(result1, result2)


if __name__ == '__main__':
    unittest.main()
