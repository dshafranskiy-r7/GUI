# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/pySDL2gui.py
Tests module structure without deep SDL2 integration
"""

import os
import sys
import unittest
from pathlib import Path


class TestPySDL2guiStructure(unittest.TestCase):
    """Test pySDL2gui module structure"""

    def setUp(self):
        """Set up test file path"""
        self.pysdl2gui_file = Path(__file__).parent.parent / 'PortMaster' / 'pylibs' / 'pySDL2gui.py'

    def test_file_exists(self):
        """Test that pySDL2gui.py file exists"""
        self.assertTrue(self.pysdl2gui_file.exists())

    def test_file_has_classes(self):
        """Test file contains expected classes"""
        content = self.pysdl2gui_file.read_text()
        # Check for common class definitions
        self.assertIn('class ', content)

    def test_file_imports_required_modules(self):
        """Test file imports required modules"""
        content = self.pysdl2gui_file.read_text()
        self.assertIn('import sdl2', content)

    def test_valid_python_syntax(self):
        """Test file has valid Python syntax"""
        content = self.pysdl2gui_file.read_text()
        try:
            compile(content, str(self.pysdl2gui_file), 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in pySDL2gui.py: {e}")

    def test_module_can_be_imported(self):
        """Test pySDL2gui module can be imported"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))
        import pySDL2gui
        self.assertIsNotNone(pySDL2gui)


if __name__ == '__main__':
    unittest.main()
