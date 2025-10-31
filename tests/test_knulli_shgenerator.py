# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/knulli/shGenerator.py
Tests module structure by reading the source file directly
"""

import os
import sys
import unittest
from pathlib import Path


class TestKnulliShGenerator(unittest.TestCase):
    """Test Knulli shGenerator module structure"""

    def setUp(self):
        """Set up test file path"""
        self.sh_generator_file = Path(__file__).parent.parent / 'PortMaster' / 'knulli' / 'shGenerator.py'

    def test_file_exists(self):
        """Test that shGenerator.py file exists"""
        self.assertTrue(self.sh_generator_file.exists())

    def test_has_shgenerator_class(self):
        """Test file contains ShGenerator class definition"""
        content = self.sh_generator_file.read_text()
        self.assertIn('class ShGenerator', content)

    def test_has_generate_method(self):
        """Test file contains generate method"""
        content = self.sh_generator_file.read_text()
        self.assertIn('def generate(', content)

    def test_has_getmousemode_method(self):
        """Test file contains getMouseMode method"""
        content = self.sh_generator_file.read_text()
        self.assertIn('def getMouseMode(', content)

    def test_imports_required_modules(self):
        """Test file imports required modules"""
        content = self.sh_generator_file.read_text()
        self.assertIn('import Command', content)
        self.assertIn('import controllersConfig', content)

    def test_valid_python_syntax(self):
        """Test file has valid Python syntax"""
        content = self.sh_generator_file.read_text()
        try:
            compile(content, str(self.sh_generator_file), 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in shGenerator.py: {e}")


if __name__ == '__main__':
    unittest.main()
