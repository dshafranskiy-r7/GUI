# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/harbourmaster/__init__.py
"""

import os
import sys
import unittest

# Add PortMaster/pylibs to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))

import harbourmaster


class TestHarbourmasterInit(unittest.TestCase):
    """Test harbourmaster module initialization"""

    def test_version_constant(self):
        """Test HARBOURMASTER_VERSION is defined"""
        self.assertIsNotNone(harbourmaster.HARBOURMASTER_VERSION)
        self.assertIsInstance(harbourmaster.HARBOURMASTER_VERSION, str)

    def test_config_imports(self):
        """Test config module imports"""
        self.assertTrue(hasattr(harbourmaster, 'HM_TOOLS_DIR'))
        self.assertTrue(hasattr(harbourmaster, 'HM_PORTS_DIR'))
        self.assertTrue(hasattr(harbourmaster, 'HM_SCRIPTS_DIR'))
        self.assertTrue(hasattr(harbourmaster, 'HM_TESTING'))

    def test_util_imports(self):
        """Test util module imports"""
        self.assertTrue(hasattr(harbourmaster, 'HarbourException'))
        self.assertTrue(hasattr(harbourmaster, 'json_safe_load'))
        self.assertTrue(hasattr(harbourmaster, 'json_safe_loads'))
        self.assertTrue(hasattr(harbourmaster, 'fetch_json'))
        self.assertTrue(hasattr(harbourmaster, 'nice_size'))
        self.assertTrue(hasattr(harbourmaster, 'name_cleaner'))
        self.assertTrue(hasattr(harbourmaster, 'version_parse'))

    def test_info_imports(self):
        """Test info module imports"""
        self.assertTrue(hasattr(harbourmaster, 'port_info_load'))

    def test_captain_imports(self):
        """Test captain module imports"""
        self.assertTrue(hasattr(harbourmaster, 'check_port'))

    def test_source_imports(self):
        """Test source module imports"""
        self.assertTrue(hasattr(harbourmaster, 'BaseSource'))

    def test_hardware_imports(self):
        """Test hardware module imports"""
        self.assertTrue(hasattr(harbourmaster, 'device_info'))

    def test_platform_imports(self):
        """Test platform module imports"""
        self.assertTrue(hasattr(harbourmaster, 'PlatformBase'))

    def test_harbour_imports(self):
        """Test harbour module imports"""
        self.assertTrue(hasattr(harbourmaster, 'HarbourMaster'))

    def test_all_exports(self):
        """Test __all__ exports"""
        self.assertIn('HarbourMaster', harbourmaster.__all__)


if __name__ == '__main__':
    unittest.main()
