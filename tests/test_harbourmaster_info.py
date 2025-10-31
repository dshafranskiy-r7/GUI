# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/harbourmaster/info.py
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add PortMaster/pylibs to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))

from harbourmaster import info


class TestPortInfoConstants(unittest.TestCase):
    """Test port info constants"""

    def test_port_info_root_attrs_exists(self):
        """Test PORT_INFO_ROOT_ATTRS is defined"""
        self.assertIsInstance(info.PORT_INFO_ROOT_ATTRS, dict)
        self.assertIn('version', info.PORT_INFO_ROOT_ATTRS)
        self.assertIn('name', info.PORT_INFO_ROOT_ATTRS)

    def test_port_info_attr_attrs_exists(self):
        """Test PORT_INFO_ATTR_ATTRS is defined"""
        self.assertIsInstance(info.PORT_INFO_ATTR_ATTRS, dict)
        self.assertIn('title', info.PORT_INFO_ATTR_ATTRS)
        self.assertIn('desc', info.PORT_INFO_ATTR_ATTRS)

    def test_port_info_optional_root_attrs_exists(self):
        """Test PORT_INFO_OPTIONAL_ROOT_ATTRS is defined"""
        self.assertIsInstance(info.PORT_INFO_OPTIONAL_ROOT_ATTRS, list)


class TestPortInfoLoad(unittest.TestCase):
    """Test port_info_load function"""

    def test_port_info_load_from_dict(self):
        """Test loading port info from dict"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': ['file1.sh'],
            'attr': {
                'title': 'Test Port',
                'desc': 'Test description'
            }
        }
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'test_port')
        self.assertEqual(result['attr']['title'], 'Test Port')

    def test_port_info_load_from_file(self):
        """Test loading port info from file"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': ['file1.sh'],
            'attr': {
                'title': 'Test Port',
                'desc': 'Test description'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_info, f)
            temp_file = f.name
        
        try:
            result = info.port_info_load(Path(temp_file))
            self.assertIsNotNone(result)
            self.assertEqual(result['name'], 'test_port')
        finally:
            os.unlink(temp_file)

    def test_port_info_load_invalid_json(self):
        """Test loading port info from invalid JSON"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("not valid json")
            temp_file = f.name
        
        try:
            result = info.port_info_load(Path(temp_file))
            self.assertIsNone(result)
        finally:
            os.unlink(temp_file)

    def test_port_info_load_with_default(self):
        """Test loading port info with default flag"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("not valid json")
            temp_file = f.name
        
        try:
            result = info.port_info_load(Path(temp_file), do_default=True)
            self.assertIsNotNone(result)
            # Should return a valid port info structure with defaults
            self.assertIn('version', result)
        finally:
            os.unlink(temp_file)

    def test_port_info_load_version_1_upgrade(self):
        """Test upgrading version 1 port info"""
        test_info = {
            'version': 1,
            'source': 'http://example.com/test_port',
            'attr': {
                'title': '',
                'runtime': None
            }
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result['version'], 2)
        self.assertEqual(result['name'], 'test_port')

    def test_port_info_load_version_2_upgrade(self):
        """Test upgrading version 2 port info"""
        test_info = {
            'version': 2,
            'name': 'test_port',
            'items': [],
            'attr': {
                'runtime': None
            }
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result['version'], 3)

    def test_port_info_load_version_3_upgrade(self):
        """Test upgrading version 3 port info"""
        test_info = {
            'version': 3,
            'name': 'test_port',
            'items': [],
            'attr': {
                'runtime': None
            }
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertEqual(result['version'], 4)
        self.assertEqual(result['attr']['runtime'], [])

    def test_port_info_load_version_too_new(self):
        """Test loading port info with version too new"""
        test_info = {
            'version': 999,
            'name': 'test_port',
            'attr': {}
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNone(result)

    def test_port_info_load_porter_string_to_list(self):
        """Test converting porter from string to list"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {
                'porter': 'John Doe'
            }
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertIsInstance(result['attr']['porter'], list)
        self.assertIn('John Doe', result['attr']['porter'])

    def test_port_info_load_runtime_string_to_list(self):
        """Test converting runtime from string to list"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {
                'runtime': 'mono'
            }
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertIsInstance(result['attr']['runtime'], list)
        self.assertIn('mono', result['attr']['runtime'])

    def test_port_info_load_items_validation(self):
        """Test that items list validates against bad paths"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': ['/etc/passwd', '../../../etc/passwd', 'valid_file.sh'],
            'attr': {}
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        # Should remove bad paths
        self.assertEqual(len(result['items']), 1)
        self.assertEqual(result['items'][0], 'valid_file.sh')

    def test_port_info_load_version_string(self):
        """Test that string version is converted to int"""
        test_info = {
            'version': '4',
            'name': 'test_port',
            'items': [],
            'attr': {}
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertIsInstance(result['version'], int)

    def test_port_info_load_reqs_dict_to_list(self):
        """Test converting reqs from dict to list"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {
                'reqs': {'req1': True, 'req2': False}
            }
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertIsInstance(result['attr']['reqs'], list)

    def test_port_info_load_blank_runtime(self):
        """Test handling of blank runtime"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {
                'runtime': 'blank'
            }
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        # Should be converted to list
        self.assertIsInstance(result['attr']['runtime'], list)

    def test_port_info_load_optional_attrs(self):
        """Test loading optional attributes"""
        test_info = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'status': {'source': 'test', 'status': 'installed'},
            'files': ['file1.sh'],
            'source': 'http://example.com',
            'attr': {}
        }
        
        result = info.port_info_load(test_info, source_name="test")
        self.assertIsNotNone(result)
        self.assertIn('status', result)
        self.assertIn('files', result)
        self.assertIn('source', result)


if __name__ == '__main__':
    unittest.main()
