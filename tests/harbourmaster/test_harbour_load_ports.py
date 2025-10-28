"""
Unit tests for harbour.py load_ports method phases.
Tests for Phase 1 and Phase 2 of the load_ports refactoring.
"""
import unittest
import tempfile
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

# Add the PortMaster directories to the path
portmaster_base = Path(__file__).parent.parent.parent / 'PortMaster'
portmaster_pylibs = portmaster_base / 'pylibs'
portmaster_exlibs = portmaster_base / 'exlibs'

sys.path.insert(0, str(portmaster_pylibs))
sys.path.insert(0, str(portmaster_exlibs))

# Import after adding to path
import harbourmaster.harbour
import harbourmaster.util
from harbourmaster.harbour import HarbourMaster
from harbourmaster.util import add_dict_list_unique, get_dict_list


class TestLoadPortsPhase1(unittest.TestCase):
    """Test cases for Phase 1: Load all *.port.json files"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.ports_dir = Path(self.temp_dir) / "ports"
        self.ports_dir.mkdir()
        
        # Create a mock HarbourMaster instance
        self.hm = MagicMock(spec=HarbourMaster)
        self.hm.ports_dir = self.ports_dir
        
        # Bind the actual method to the mock
        self.hm._load_ports_phase1 = HarbourMaster._load_ports_phase1.__get__(self.hm, HarbourMaster)
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_phase1_empty_port_files(self):
        """Test Phase 1 with no port files"""
        port_files = []
        ports_info = {'portsmd_fix': {}}
        
        all_ports, ports_files_result, all_items = self.hm._load_ports_phase1(port_files, ports_info)
        
        self.assertEqual(all_ports, {})
        self.assertEqual(ports_files_result, {})
        self.assertEqual(all_items, {})
    
    def test_phase1_single_valid_port(self):
        """Test Phase 1 with a single valid port"""
        # Create a test port directory and file
        port_dir = self.ports_dir / "testport"
        port_dir.mkdir()
        port_file = port_dir / "port.json"
        
        port_data = {
            'name': 'testport',
            'items': ['testport.sh'],
            'attr': {
                'title': 'Test Port',
                'porter': 'TestPorter'
            }
        }
        
        with open(port_file, 'w') as f:
            json.dump(port_data, f)
        
        # Mock the helper methods
        self.hm._load_port_info = MagicMock(return_value={
            'name': 'testport',
            'items': ['testport.sh'],
            'attr': {'title': 'Test Port', 'porter': 'TestPorter'}
        })
        self.hm._ports_dir_relative_to = MagicMock(return_value=Path('testport/port.json'))
        self.hm._ports_dir_exists = MagicMock(return_value=True)
        
        port_files = [port_file]
        ports_info = {'portsmd_fix': {}}
        
        all_ports, ports_files_result, all_items = self.hm._load_ports_phase1(port_files, ports_info)
        
        # Verify results
        self.assertIn('testport', all_ports)
        self.assertIn('testport', ports_files_result)
        self.assertIn('testport.sh', all_items)
    
    def test_phase1_port_with_none_porter(self):
        """Test Phase 1 handles None porter correctly"""
        port_dir = self.ports_dir / "testport2"
        port_dir.mkdir()
        port_file = port_dir / "port.json"
        
        # Mock the helper methods
        self.hm._load_port_info = MagicMock(return_value={
            'name': 'testport2',
            'items': ['testport2.sh'],
            'attr': {'title': 'Test Port 2', 'porter': None}
        })
        self.hm._ports_dir_relative_to = MagicMock(return_value=Path('testport2/port.json'))
        self.hm._ports_dir_exists = MagicMock(return_value=True)
        
        port_files = [port_file]
        ports_info = {'portsmd_fix': {}}
        
        all_ports, ports_files_result, all_items = self.hm._load_ports_phase1(port_files, ports_info)
        
        # Verify porter was set to ['Unknown']
        self.assertEqual(all_ports['testport2']['attr']['porter'], ['Unknown'])
        self.assertTrue(all_ports['testport2']['changed'])
    
    def test_phase1_port_with_string_porter(self):
        """Test Phase 1 handles string porter correctly"""
        port_dir = self.ports_dir / "testport3"
        port_dir.mkdir()
        port_file = port_dir / "port.json"
        
        # Mock the helper methods
        self.hm._load_port_info = MagicMock(return_value={
            'name': 'testport3',
            'items': ['testport3.sh'],
            'attr': {'title': 'Test Port 3', 'porter': 'OldPorter'}
        })
        self.hm._ports_dir_relative_to = MagicMock(return_value=Path('testport3/port.json'))
        self.hm._ports_dir_exists = MagicMock(return_value=True)
        
        port_files = [port_file]
        ports_info = {'portsmd_fix': {'oldporter': 'NewPorter'}}
        
        all_ports, ports_files_result, all_items = self.hm._load_ports_phase1(port_files, ports_info)
        
        # Verify porter was looked up in portsmd_fix
        self.assertEqual(all_ports['testport3']['attr']['porter'], 'NewPorter')
        self.assertTrue(all_ports['testport3']['changed'])
    
    def test_phase1_port_with_optional_items(self):
        """Test Phase 1 handles optional items correctly"""
        port_dir = self.ports_dir / "testport4"
        port_dir.mkdir()
        port_file = port_dir / "port.json"
        
        # Mock the helper methods
        self.hm._load_port_info = MagicMock(return_value={
            'name': 'testport4',
            'items': ['testport4.sh'],
            'items_opt': ['optional.sh'],
            'attr': {'title': 'Test Port 4', 'porter': ['Porter1']}
        })
        self.hm._ports_dir_relative_to = MagicMock(return_value=Path('testport4/port.json'))
        self.hm._ports_dir_exists = MagicMock(return_value=True)
        
        port_files = [port_file]
        ports_info = {'portsmd_fix': {}}
        
        all_ports, ports_files_result, all_items = self.hm._load_ports_phase1(port_files, ports_info)
        
        # Verify optional items are in all_items
        self.assertIn('optional.sh', all_items)
        self.assertIn('testport4.sh', all_items)


class TestLoadPortsPhase2(unittest.TestCase):
    """Test cases for Phase 2: Check all files/dirs in ports_dir"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.ports_dir = Path(self.temp_dir) / "ports"
        self.ports_dir.mkdir()
        
        # Create a mock HarbourMaster instance
        self.hm = MagicMock(spec=HarbourMaster)
        self.hm.ports_dir = self.ports_dir
        
        # Bind the actual method to the mock
        self.hm._load_ports_phase2 = HarbourMaster._load_ports_phase2.__get__(self.hm, HarbourMaster)
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_phase2_empty_ports_dir(self):
        """Test Phase 2 with empty ports directory"""
        all_ports = {}
        all_items = {}
        
        # Mock _iter_ports_dir to return empty list
        self.hm._iter_ports_dir = MagicMock(return_value=[])
        
        unknown_files, file_renames = self.hm._load_ports_phase2(all_ports, all_items)
        
        self.assertEqual(unknown_files, [])
        self.assertEqual(file_renames, {})
    
    def test_phase2_skips_excluded_files(self):
        """Test Phase 2 skips excluded files like gamelist.xml"""
        all_ports = {}
        all_items = {}
        
        # Create mock file items
        excluded_file = MagicMock()
        excluded_file.name = 'gamelist.xml'
        excluded_file.is_dir.return_value = False
        excluded_file.suffix.casefold.return_value = '.xml'
        
        self.hm._iter_ports_dir = MagicMock(return_value=[excluded_file])
        
        unknown_files, file_renames = self.hm._load_ports_phase2(all_ports, all_items)
        
        # Should be empty since gamelist.xml is excluded
        self.assertEqual(unknown_files, [])
    
    def test_phase2_skips_no_touchy_files(self):
        """Test Phase 2 skips files with PORTMASTER NO TOUCHY marker"""
        all_ports = {}
        all_items = {}
        
        # Create mock file item
        no_touchy_file = MagicMock()
        no_touchy_file.name = 'special.sh'
        no_touchy_file.is_dir.return_value = False
        no_touchy_file.is_file.return_value = True
        no_touchy_file.suffix.casefold.return_value = '.sh'
        
        self.hm._iter_ports_dir = MagicMock(return_value=[no_touchy_file])
        
        # Mock open to return file with NO TOUCHY marker
        with patch('builtins.open', mock_open(read_data=b'PORTMASTER NO TOUCHY')):
            unknown_files, file_renames = self.hm._load_ports_phase2(all_ports, all_items)
        
        # Should be empty since file has NO TOUCHY marker
        self.assertEqual(unknown_files, [])
    
    def test_phase2_handles_known_port_files(self):
        """Test Phase 2 handles files belonging to known ports"""
        all_ports = {'testport': {
            'name': 'testport',
            'files': {}
        }}
        all_items = {'testport.sh': ['testport']}
        
        # Create mock file item
        known_file = MagicMock()
        known_file.name = 'testport.sh'
        known_file.is_dir.return_value = False
        known_file.is_file.return_value = True
        known_file.suffix.casefold.return_value = '.sh'
        
        self.hm._iter_ports_dir = MagicMock(return_value=[known_file])
        
        # Mock load_pm_signature to return None (needs signature)
        with patch('harbourmaster.harbour.load_pm_signature', return_value=None):
            with patch('harbourmaster.harbour.add_pm_signature') as mock_add_sig:
                with patch('builtins.open', mock_open(read_data=b'#!/bin/bash')):
                    unknown_files, file_renames = self.hm._load_ports_phase2(all_ports, all_items)
                
                # Should have called add_pm_signature
                mock_add_sig.assert_called_once()
        
        # File should not be in unknown_files
        self.assertNotIn('testport.sh', unknown_files)
    
    def test_phase2_tracks_unknown_files(self):
        """Test Phase 2 tracks unknown files"""
        all_ports = {}
        all_items = {}
        
        # Create mock file item
        unknown_file = MagicMock()
        unknown_file.name = 'unknown.sh'
        unknown_file.is_dir.return_value = False
        unknown_file.is_file.return_value = True
        unknown_file.suffix.casefold.return_value = '.sh'
        
        self.hm._iter_ports_dir = MagicMock(return_value=[unknown_file])
        self.hm._get_pm_signature = MagicMock(return_value=None)
        
        with patch('builtins.open', mock_open(read_data=b'#!/bin/bash')):
            unknown_files, file_renames = self.hm._load_ports_phase2(all_ports, all_items)
        
        # Should track unknown file
        self.assertIn('unknown.sh', unknown_files)
    
    def test_phase2_tracks_file_renames(self):
        """Test Phase 2 tracks renamed files"""
        all_ports = {}
        all_items = {}
        
        # Create mock file item
        renamed_file = MagicMock()
        renamed_file.name = 'newname.sh'
        renamed_file.is_dir.return_value = False
        renamed_file.is_file.return_value = True
        renamed_file.suffix.casefold.return_value = '.sh'
        
        self.hm._iter_ports_dir = MagicMock(return_value=[renamed_file])
        # Mock signature showing file was renamed: (current_name, original_name, port_name)
        self.hm._get_pm_signature = MagicMock(return_value=('newname.sh', 'oldname.sh', None))
        
        with patch('builtins.open', mock_open(read_data=b'#!/bin/bash')):
            unknown_files, file_renames = self.hm._load_ports_phase2(all_ports, all_items)
        
        # Should track file rename
        self.assertIn('oldname.sh', file_renames)
        self.assertEqual(file_renames['oldname.sh'], 'newname.sh')


class TestUtilFunctions(unittest.TestCase):
    """Test utility functions used by load_ports phases"""
    
    def test_add_dict_list_unique_new_key(self):
        """Test add_dict_list_unique with a new key"""
        base_dict = {}
        add_dict_list_unique(base_dict, 'key1', 'value1')
        self.assertEqual(base_dict['key1'], 'value1')
    
    def test_add_dict_list_unique_existing_string(self):
        """Test add_dict_list_unique with existing string value"""
        base_dict = {'key1': 'value1'}
        add_dict_list_unique(base_dict, 'key1', 'value2')
        self.assertEqual(base_dict['key1'], ['value1', 'value2'])
    
    def test_add_dict_list_unique_existing_list(self):
        """Test add_dict_list_unique with existing list value"""
        base_dict = {'key1': ['value1']}
        add_dict_list_unique(base_dict, 'key1', 'value2')
        self.assertEqual(base_dict['key1'], ['value1', 'value2'])
    
    def test_add_dict_list_unique_duplicate(self):
        """Test add_dict_list_unique with duplicate value"""
        base_dict = {'key1': ['value1']}
        add_dict_list_unique(base_dict, 'key1', 'value1')
        self.assertEqual(base_dict['key1'], ['value1'])
    
    def test_get_dict_list_missing_key(self):
        """Test get_dict_list with missing key"""
        base_dict = {}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, [])
    
    def test_get_dict_list_string_value(self):
        """Test get_dict_list with string value"""
        base_dict = {'key1': 'value1'}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, ['value1'])
    
    def test_get_dict_list_list_value(self):
        """Test get_dict_list with list value"""
        base_dict = {'key1': ['value1', 'value2']}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, ['value1', 'value2'])
    
    def test_get_dict_list_none_value(self):
        """Test get_dict_list with None value"""
        base_dict = {'key1': None}
        result = get_dict_list(base_dict, 'key1')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
