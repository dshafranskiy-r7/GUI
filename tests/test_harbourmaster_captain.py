# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/harbourmaster/captain.py
"""

import io
import json
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

# Add PortMaster/pylibs to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))

from harbourmaster import captain


class TestBadPort(unittest.TestCase):
    """Test BadPort exception"""

    def test_badport_exception(self):
        """Test BadPort exception can be raised"""
        with self.assertRaises(captain.BadPort):
            raise captain.BadPort()


class TestCheckPort(unittest.TestCase):
    """Test check_port function"""

    def _create_test_zip(self, files):
        """Helper to create a test zip file"""
        temp_zip = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.zip')
        temp_zip.close()
        
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            for filename, content in files.items():
                if isinstance(content, str):
                    zf.writestr(filename, content)
                elif isinstance(content, bytes):
                    zf.writestr(filename, content)
                elif content is None:
                    # Create an empty file
                    zf.writestr(filename, "")
        
        return temp_zip.name

    def test_check_port_valid(self):
        """Test check_port with valid port"""
        port_json = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {
                'title': 'Test Port',
                'desc': 'A test port'
            }
        }
        
        files = {
            'testport/': None,
            'testport/port.json': json.dumps(port_json),
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            result = captain.check_port('testport', zip_file)
            self.assertIsNotNone(result)
            self.assertEqual(result['name'], 'testport')
            self.assertIn('items', result)
        finally:
            os.unlink(zip_file)

    def test_check_port_illegal_absolute_path(self):
        """Test check_port rejects absolute paths"""
        files = {
            '/etc/passwd': 'bad',
            'testport/': None,
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            with self.assertRaises(captain.BadPort):
                captain.check_port('testport', zip_file)
        finally:
            os.unlink(zip_file)

    def test_check_port_illegal_parent_path(self):
        """Test check_port rejects parent directory paths"""
        files = {
            '../etc/passwd': 'bad',
            'testport/': None,
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            with self.assertRaises(captain.BadPort):
                captain.check_port('testport', zip_file)
        finally:
            os.unlink(zip_file)

    def test_check_port_illegal_traversal(self):
        """Test check_port rejects path traversal"""
        files = {
            'testport/../etc/passwd': 'bad',
            'testport/': None,
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            with self.assertRaises(captain.BadPort):
                captain.check_port('testport', zip_file)
        finally:
            os.unlink(zip_file)

    def test_check_port_no_directories(self):
        """Test check_port rejects ports without directories"""
        files = {
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            with self.assertRaises(captain.BadPort):
                captain.check_port('testport', zip_file)
        finally:
            os.unlink(zip_file)

    def test_check_port_no_scripts(self):
        """Test check_port rejects ports without scripts"""
        files = {
            'testport/': None,
            'testport/readme.txt': 'test'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            with self.assertRaises(captain.BadPort):
                captain.check_port('testport', zip_file)
        finally:
            os.unlink(zip_file)

    def test_check_port_with_extra_info(self):
        """Test check_port with extra_info parameter"""
        port_json = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {}
        }
        
        files = {
            'testport/': None,
            'testport/port.json': json.dumps(port_json),
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        extra_info = {}
        
        try:
            result = captain.check_port('testport', zip_file, extra_info=extra_info)
            self.assertIsNotNone(result)
            self.assertIn('port_info_file', extra_info)
            self.assertIn('port_dir', extra_info)
        finally:
            os.unlink(zip_file)

    def test_check_port_with_gameinfo_xml(self):
        """Test check_port with gameinfo.xml"""
        port_json = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {}
        }
        
        files = {
            'testport/': None,
            'testport/port.json': json.dumps(port_json),
            'testport/gameinfo.xml': '<game></game>',
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        extra_info = {}
        
        try:
            result = captain.check_port('testport', zip_file, extra_info=extra_info)
            self.assertIsNotNone(result)
            self.assertIn('gameinfo_xml', extra_info)
        finally:
            os.unlink(zip_file)

    def test_check_port_no_port_json(self):
        """Test check_port without port.json"""
        files = {
            'testport/': None,
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            result = captain.check_port('testport', zip_file)
            self.assertIsNotNone(result)
            # Should still work with defaults
            self.assertEqual(result['name'], 'testport')
        finally:
            os.unlink(zip_file)

    def test_check_port_invalid_port_json(self):
        """Test check_port with invalid port.json"""
        files = {
            'testport/': None,
            'testport/port.json': 'not valid json',
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        
        try:
            with self.assertRaises(captain.BadPort):
                captain.check_port('testport', zip_file)
        finally:
            os.unlink(zip_file)

    def test_check_port_top_level_port_json(self):
        """Test check_port with top-level port.json"""
        port_json = {
            'version': 4,
            'name': 'test_port',
            'items': [],
            'attr': {}
        }
        
        files = {
            'testport/': None,
            'port.json': json.dumps(port_json),
            'run.sh': '#!/bin/bash\necho "test"'
        }
        
        zip_file = self._create_test_zip(files)
        extra_info = {}
        
        try:
            result = captain.check_port('testport', zip_file, extra_info=extra_info)
            self.assertIsNotNone(result)
            # port_info_file should be moved to proper location
            self.assertIn('testport/', extra_info.get('port_info_file', ''))
        finally:
            os.unlink(zip_file)


if __name__ == '__main__':
    unittest.main()
