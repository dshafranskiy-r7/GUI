# SPDX-License-Identifier: MIT

"""
Tests for PortMaster/mapper.py
"""

import os
import sys
import unittest
from pathlib import Path

# Add PortMaster to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PortMaster'))

import mapper


class TestMapperConstants(unittest.TestCase):
    """Test mapper constants"""

    def test_tr_map_exists(self):
        """Test that TR_MAP is defined"""
        self.assertIsInstance(mapper.TR_MAP, dict)
        self.assertGreater(len(mapper.TR_MAP), 0)

    def test_tr_map_button_mappings(self):
        """Test specific button mappings"""
        self.assertEqual(mapper.TR_MAP["b"], "a")
        self.assertEqual(mapper.TR_MAP["a"], "b")
        self.assertEqual(mapper.TR_MAP["x"], "y")
        self.assertEqual(mapper.TR_MAP["y"], "x")

    def test_tr_map_dpad_mappings(self):
        """Test dpad mappings"""
        self.assertEqual(mapper.TR_MAP["up"], "dpup")
        self.assertEqual(mapper.TR_MAP["down"], "dpdown")
        self.assertEqual(mapper.TR_MAP["left"], "dpleft")
        self.assertEqual(mapper.TR_MAP["right"], "dpright")

    def test_tr_map_analog_mappings(self):
        """Test analog stick mappings"""
        self.assertEqual(mapper.TR_MAP["leftanalogup"], "-lefty")
        self.assertEqual(mapper.TR_MAP["leftanalogdown"], "+lefty")
        self.assertEqual(mapper.TR_MAP["leftanalogleft"], "-leftx")
        self.assertEqual(mapper.TR_MAP["leftanalogright"], "+leftx")

    def test_map_suffix(self):
        """Test MAP_SUFFIX constant"""
        self.assertEqual(mapper.MAP_SUFFIX, "platform:Linux,")


class TestMapInputFunction(unittest.TestCase):
    """Test map_input function"""

    def test_map_button_input(self):
        """Test button mapping"""
        result = mapper.map_input("a", "button", "0", "1")
        self.assertEqual(result, "b:b0,")

    def test_map_axis_negative(self):
        """Test axis mapping with negative value"""
        result = mapper.map_input("leftanalogup", "axis", "1", "-1")
        self.assertEqual(result, "-lefty:-a1,")

    def test_map_axis_positive(self):
        """Test axis mapping with positive value"""
        result = mapper.map_input("leftanalogdown", "axis", "1", "1")
        self.assertEqual(result, "+lefty:+a1,")

    def test_map_trigger(self):
        """Test trigger mapping"""
        result = mapper.map_input("lefttrigger", "axis", "2", "1")
        self.assertEqual(result, "lefttrigger:a2,")

    def test_map_hat_input(self):
        """Test hat mapping"""
        result = mapper.map_input("up", "hat", "0", "1")
        self.assertEqual(result, "dpup:h0.1,")

    def test_map_invalid_input_name(self):
        """Test mapping with invalid input name"""
        result = mapper.map_input("invalid_button", "button", "0", "1")
        self.assertEqual(result, "")

    def test_map_invalid_input_type(self):
        """Test mapping with invalid input type"""
        result = mapper.map_input("a", "invalid_type", "0", "1")
        self.assertEqual(result, "")


class TestPremapInputFunction(unittest.TestCase):
    """Test premap_input function"""

    def test_premap_joystick1left(self):
        """Test premapping joystick1left"""
        input_entry = {
            "name": "joystick1left",
            "type": "axis",
            "id": "0",
            "value": "-1"
        }
        result = mapper.premap_input(input_entry)
        self.assertIn("-leftx", result)
        self.assertIn("+leftx", result)

    def test_premap_joystick1up(self):
        """Test premapping joystick1up"""
        input_entry = {
            "name": "joystick1up",
            "type": "axis",
            "id": "1",
            "value": "-1"
        }
        result = mapper.premap_input(input_entry)
        self.assertIn("-lefty", result)
        self.assertIn("+lefty", result)

    def test_premap_joystick2left(self):
        """Test premapping joystick2left"""
        input_entry = {
            "name": "joystick2left",
            "type": "axis",
            "id": "2",
            "value": "-1"
        }
        result = mapper.premap_input(input_entry)
        self.assertIn("-rightx", result)
        self.assertIn("+rightx", result)

    def test_premap_joystick2up(self):
        """Test premapping joystick2up"""
        input_entry = {
            "name": "joystick2up",
            "type": "axis",
            "id": "3",
            "value": "-1"
        }
        result = mapper.premap_input(input_entry)
        self.assertIn("-righty", result)
        self.assertIn("+righty", result)

    def test_premap_button(self):
        """Test premapping regular button"""
        input_entry = {
            "name": "a",
            "type": "button",
            "id": "0",
            "value": "1"
        }
        result = mapper.premap_input(input_entry)
        self.assertEqual(result, "b:b0,")

    def test_premap_value_inversion(self):
        """Test that value inversion works correctly"""
        input_entry = {
            "name": "joystick1left",
            "type": "axis",
            "id": "0",
            "value": "1"
        }
        result = mapper.premap_input(input_entry)
        # When value is "1", invert should be "-1"
        self.assertIn("+a0", result)
        self.assertIn("-a0", result)


if __name__ == '__main__':
    unittest.main()
