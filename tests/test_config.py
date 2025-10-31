#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

"""
Tests for harbourmaster.config module
"""

import sys
import unittest
from pathlib import Path

# Add PortMaster modules to path
PORTMASTER_DIR = Path(__file__).parent.parent / "PortMaster"
sys.path.insert(0, str(PORTMASTER_DIR / "pylibs"))
sys.path.insert(0, str(PORTMASTER_DIR / "exlibs"))

from harbourmaster.config import (
    HM_GENRES,
    HM_SORT_ORDER,
    HM_SOURCE_DEFAULTS,
)


class TestConfigConstants(unittest.TestCase):
    """Test configuration constants"""

    def test_genres_is_list(self):
        """Test that HM_GENRES is a list"""
        self.assertIsInstance(HM_GENRES, list)
        self.assertGreater(len(HM_GENRES), 0)

    def test_genres_are_strings(self):
        """Test that all genres are strings"""
        for genre in HM_GENRES:
            self.assertIsInstance(genre, str)

    def test_sort_order_is_list(self):
        """Test that HM_SORT_ORDER is a list"""
        self.assertIsInstance(HM_SORT_ORDER, list)
        self.assertGreater(len(HM_SORT_ORDER), 0)

    def test_source_defaults_is_dict(self):
        """Test that HM_SOURCE_DEFAULTS is a dict"""
        self.assertIsInstance(HM_SOURCE_DEFAULTS, dict)
        self.assertGreater(len(HM_SOURCE_DEFAULTS), 0)

    def test_source_defaults_keys(self):
        """Test that source defaults have expected structure"""
        import json
        for key, value in HM_SOURCE_DEFAULTS.items():
            self.assertIsInstance(key, str)
            # Values are JSON strings
            self.assertIsInstance(value, str)
            # Should be valid JSON
            parsed = json.loads(value)
            self.assertIsInstance(parsed, dict)
            # Each source should have at least a 'url' key
            self.assertIn('url', parsed)


if __name__ == '__main__':
    unittest.main()
