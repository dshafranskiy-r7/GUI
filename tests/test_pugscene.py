# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/pugscene.py
Tests module structure without deep SDL2 integration
"""

import os
import sys
import unittest
from pathlib import Path


class TestPugsceneStructure(unittest.TestCase):
    """Test pugscene module structure"""

    def setUp(self):
        """Set up test file path"""
        self.pugscene_file = Path(__file__).parent.parent / 'PortMaster' / 'pylibs' / 'pugscene.py'

    def test_file_exists(self):
        """Test that pugscene.py file exists"""
        self.assertTrue(self.pugscene_file.exists())

    def test_file_has_classes(self):
        """Test file contains expected classes"""
        content = self.pugscene_file.read_text()
        # Check for common class definitions
        self.assertIn('class ', content)

    def test_file_imports_required_modules(self):
        """Test file imports required modules"""
        content = self.pugscene_file.read_text()
        self.assertIn('import sdl2', content)
        self.assertIn('import harbourmaster', content)

    def test_valid_python_syntax(self):
        """Test file has valid Python syntax"""
        content = self.pugscene_file.read_text()
        try:
            compile(content, str(self.pugscene_file), 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in pugscene.py: {e}")

    def test_module_can_be_imported(self):
        """Test pugscene module can be imported"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))
        import pugscene
        self.assertIsNotNone(pugscene)


if __name__ == '__main__':
    unittest.main()
