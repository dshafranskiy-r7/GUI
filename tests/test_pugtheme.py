# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/pugtheme.py
"""

import os
import sys
import unittest

# Add PortMaster/pylibs to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))


class TestPugthemeFunctions(unittest.TestCase):
    """Test pugtheme module functions"""

    def test_module_imports(self):
        """Test pugtheme module can be imported"""
        import pugtheme
        self.assertIsNotNone(pugtheme)

    def test_extract_requirements_function(self):
        """Test extract_requirements function exists"""
        import pugtheme
        self.assertTrue(hasattr(pugtheme, 'extract_requirements'))
        self.assertTrue(callable(pugtheme.extract_requirements))

    def test_extract_requirements_no_brackets(self):
        """Test extract_requirements with no requirements"""
        import pugtheme
        text, reqs = pugtheme.extract_requirements("simple_text")
        self.assertEqual(text, "simple_text")
        self.assertEqual(reqs, [])

    def test_extract_requirements_with_requirements(self):
        """Test extract_requirements with requirements"""
        import pugtheme
        text, reqs = pugtheme.extract_requirements("element[req1, req2]")
        self.assertEqual(text, "element")
        self.assertEqual(reqs, ["req1", "req2"])

    def test_extract_requirements_strict_mode(self):
        """Test extract_requirements in strict mode"""
        import pugtheme
        text, reqs = pugtheme.extract_requirements("simple_text", strict=True)
        self.assertEqual(text, "simple_text")
        self.assertIsNone(reqs)

    def test_extract_requirements_malformed(self):
        """Test extract_requirements with malformed input"""
        import pugtheme
        text, reqs = pugtheme.extract_requirements("bad[[req]")
        self.assertIn("bad", text)

    def test_theme_update_function_exists(self):
        """Test theme_update function exists"""
        import pugtheme
        self.assertTrue(hasattr(pugtheme, 'theme_update'))
        self.assertTrue(callable(pugtheme.theme_update))

    def test_theme_merge_function_exists(self):
        """Test theme_merge function exists"""
        import pugtheme
        self.assertTrue(hasattr(pugtheme, 'theme_merge'))
        self.assertTrue(callable(pugtheme.theme_merge))

    def test_theme_check_images_function_exists(self):
        """Test theme_check_images function exists"""
        import pugtheme
        self.assertTrue(hasattr(pugtheme, 'theme_check_images'))
        self.assertTrue(callable(pugtheme.theme_check_images))

    def test_theme_apply_function_exists(self):
        """Test theme_apply function exists"""
        import pugtheme
        self.assertTrue(hasattr(pugtheme, 'theme_apply'))
        self.assertTrue(callable(pugtheme.theme_apply))


class TestThemeMergeFunctions(unittest.TestCase):
    """Test theme merge/update functions"""

    def test_theme_merge_empty_dicts(self):
        """Test theme_merge with empty dicts"""
        import pugtheme
        result = pugtheme.theme_merge({}, {})
        self.assertEqual(result, {})

    def test_theme_merge_simple(self):
        """Test theme_merge with simple dicts"""
        import pugtheme
        target = {'key1': 'value1'}
        source = {'key2': 'value2'}
        result = pugtheme.theme_merge(target, source)

        self.assertIn('key1', result)
        self.assertIn('key2', result)
        self.assertEqual(result['key1'], 'value1')
        self.assertEqual(result['key2'], 'value2')


if __name__ == '__main__':
    unittest.main()
