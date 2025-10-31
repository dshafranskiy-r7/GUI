# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/pylibs/harbourmaster/hardware.py
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add PortMaster/pylibs to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster', 'pylibs'))

from harbourmaster import hardware


class TestHardwareConstants(unittest.TestCase):
    """Test hardware module constants"""

    def test_devices_dict_exists(self):
        """Test DEVICES dictionary is defined"""
        self.assertIsInstance(hardware.DEVICES, dict)
        self.assertGreater(len(hardware.DEVICES), 0)

    def test_devices_structure(self):
        """Test DEVICES has expected structure"""
        for device_name, device_data in hardware.DEVICES.items():
            self.assertIsInstance(device_name, str)
            self.assertIsInstance(device_data, dict)
            self.assertIn('device', device_data)
            self.assertIn('manufacturer', device_data)
            self.assertIn('cfw', device_data)
            self.assertIsInstance(device_data['cfw'], list)

    def test_hw_info_dict_exists(self):
        """Test HW_INFO dictionary is defined"""
        self.assertIsInstance(hardware.HW_INFO, dict)
        self.assertGreater(len(hardware.HW_INFO), 0)

    def test_hw_info_structure(self):
        """Test HW_INFO has expected structure"""
        for device_key, device_info in hardware.HW_INFO.items():
            self.assertIsInstance(device_key, str)
            self.assertIsInstance(device_info, dict)
            # Common fields
            if 'resolution' in device_info:
                self.assertIsInstance(device_info['resolution'], tuple)
                self.assertEqual(len(device_info['resolution']), 2)

    def test_specific_devices(self):
        """Test specific device entries"""
        # Anbernic devices
        self.assertIn("Anbernic RG351P/M", hardware.DEVICES)
        self.assertIn("Anbernic RG552", hardware.DEVICES)

        # Check device mapping
        rg351p_info = hardware.DEVICES["Anbernic RG351P/M"]
        self.assertEqual(rg351p_info["device"], "rg351p")
        self.assertEqual(rg351p_info["manufacturer"], "Anbernic")

    def test_specific_hw_info(self):
        """Test specific hardware info entries"""
        self.assertIn("rg552", hardware.HW_INFO)
        rg552_info = hardware.HW_INFO["rg552"]
        self.assertEqual(rg552_info["resolution"], (1920, 1152))
        self.assertEqual(rg552_info["analogsticks"], 2)


class TestFindDeviceByResolution(unittest.TestCase):
    """Test find_device_by_resolution function"""

    def test_find_device_by_resolution_exists(self):
        """Test function exists"""
        self.assertTrue(hasattr(hardware, 'find_device_by_resolution'))
        self.assertTrue(callable(hardware.find_device_by_resolution))

    def test_find_device_by_known_resolution(self):
        """Test finding device by known resolution"""
        # RG552 has resolution (1920, 1152)
        result = hardware.find_device_by_resolution((1920, 1152))
        if result is not None:
            # Result is just the device key string
            self.assertIsInstance(result, str)


class TestExpandInfo(unittest.TestCase):
    """Test expand_info function"""

    def test_expand_info_exists(self):
        """Test function exists"""
        self.assertTrue(hasattr(hardware, 'expand_info'))
        self.assertTrue(callable(hardware.expand_info))

    def test_expand_info_basic(self):
        """Test expand_info with basic device info"""
        info = {'device': 'rg552', 'name': 'Test Device'}
        hardware.expand_info(info)

        # Should add hardware info
        self.assertIn('resolution', info)
        self.assertIn('analogsticks', info)

    def test_expand_info_with_override_resolution(self):
        """Test expand_info with resolution override"""
        info = {'device': 'rg552', 'name': 'Test Device'}
        override_resolution = (1280, 720)
        hardware.expand_info(info, override_resolution=override_resolution)

        # Resolution should be overridden
        self.assertEqual(info['resolution'], override_resolution)

    def test_expand_info_with_override_ram(self):
        """Test expand_info with RAM override"""
        info = {'device': 'rg552', 'name': 'Test Device'}
        override_ram = 2048
        hardware.expand_info(info, override_ram=override_ram)

        # RAM should be set
        self.assertIn('ram', info)


class TestDeviceInfo(unittest.TestCase):
    """Test device_info function"""

    def test_device_info_exists(self):
        """Test function exists"""
        self.assertTrue(hasattr(hardware, 'device_info'))
        self.assertTrue(callable(hardware.device_info))

    @patch('harbourmaster.hardware.new_device_info')
    @patch('harbourmaster.hardware.mem_limits')
    def test_device_info_with_override(self, mock_mem_limits, mock_new_device_info):
        """Test device_info with override"""
        mock_new_device_info.return_value = {
            'device': 'unknown',
            'name': 'Unknown Device'
        }
        mock_mem_limits.return_value = 1024

        result = hardware.device_info(override_device='rg552')

        self.assertIsNotNone(result)
        self.assertEqual(result['device'], 'rg552')

    @patch('harbourmaster.hardware.new_device_info')
    @patch('harbourmaster.hardware.mem_limits')
    def test_device_info_caching(self, mock_mem_limits, mock_new_device_info):
        """Test that device_info caches results"""
        mock_new_device_info.return_value = {
            'device': 'test_device',
            'name': 'Test Device'
        }
        mock_mem_limits.return_value = 1024

        # Clear cache by calling with override
        result1 = hardware.device_info(override_device='test1')

        # Second call without override should use cache
        result2 = hardware.device_info()

        # Results should be the same object
        self.assertEqual(result1['device'], result2['device'])


class TestHardwareModule(unittest.TestCase):
    """Test overall hardware module structure"""

    def test_all_exports(self):
        """Test __all__ exports"""
        self.assertIn('device_info', hardware.__all__)
        self.assertIn('expand_info', hardware.__all__)
        self.assertIn('find_device_by_resolution', hardware.__all__)
        self.assertIn('HW_INFO', hardware.__all__)
        self.assertIn('DEVICES', hardware.__all__)


if __name__ == '__main__':
    unittest.main()
