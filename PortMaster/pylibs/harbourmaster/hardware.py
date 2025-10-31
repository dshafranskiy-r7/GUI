
# SPDX-License-Identifier: MIT

# System imports
import copy
import datetime
import fnmatch
import json
import math
import os
import pathlib
import platform
import re
import subprocess
import zipfile

from pathlib import Path

# Included imports

from loguru import logger

# Module imports
from .config import *
from .info import *
from .util import *


# This maps device name to HW_INFO, also includes manufacturer and compatible cfw.
DEVICES = {
    # Valve
    "SteamDeck":  {"device": "steamdeck", "manufacturer": "Valve", "cfw": ["RetroDECK", "Batocera"]},
    }


HW_INFO = {
    # Computer/Testing
    "pc":        {"resolution": (640, 480), "analogsticks": 2, "cpu": "x86_64", "capabilities": ["opengl", "power"]},

    # x86_64 devices
    "retrodeck": {"resolution": (1280, 800), "analogsticks": 2, "cpu": "x86_64", "capabilities": ["opengl", "power", "ultra"], "ram": 16384},
    "steamdeck": {"resolution": (1280, 800), "analogsticks": 2, "cpu": "x86_64", "capabilities": ["opengl", "power", "ultra"], "ram": 16384},

    # Default
    "default":   {"resolution": (640, 480), "analogsticks": 2, "cpu": "x86_64", "capabilities": ["opengl", "power"]},
    }


CFW_INFO = {
    }


## OBSOLETE
CPU_INFO = {
    "x86_64":        {"capabilities": ["x86_64"],           "primary_arch": "x86_64"},
    }


GLIBC_INFO = {
    "default":     "2.30",
    }


def cpu_info_v2(info):
    if Path('/lib/ld-linux.so.2').exists():
        info["capabilities"].append("x86")
        info['primary_arch'] = "x86"

    if (
            Path('/lib/ld-linux-x86-64.so.2').exists() or
            Path('/lib64/ld-linux-x86-64.so.2').exists() or
            Path('/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2').exists()):
        info["capabilities"].append("x86_64")
        info['primary_arch'] = "x86_64"

    if HM_TESTING or 'primary_arch' not in info:
        info["capabilities"].append("x86_64")
        info['primary_arch'] = "x86_64"


_GLIBC_VER=None
def get_glibc_version():
    global _GLIBC_VER

    lib_paths = [
        '/lib64/',
        '/lib/',
        '/usr/lib64/',
        '/usr/lib/',
        '/usr/lib/x86_64-linux-gnu/',
        ]

    if _GLIBC_VER is None:
        for lib_path in lib_paths:
            libc_path = Path(lib_path) / 'libc.so.6'

            if not libc_path.is_file():
                continue
    
            try:
                result = subprocess.run(
                    [str(libc_path), "--version"],
                    capture_output=True, text=True, check=True)

                # The first line contains the glibc version
                _GLIBC_VER = result.stdout.splitlines()[0].strip().split(' ')[-1].rstrip('.')

            except Exception as e:
                logger.error(f"Error retrieving glibc version: {e}")
                # Failsafe
                _GLIBC_VER = GLIBC_INFO['default']

            break

        else:
            _GLIBC_VER = GLIBC_INFO['default']

    return _GLIBC_VER


def safe_cat(file_name):
    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    elif not isinstance(file_name, pathlib.PurePath):
        raise ValueError(file_name)

    if str(file_name).startswith('~/'):
        file_name = file_name.expanduser()

    if not file_name.is_file():
        return ''

    return file_name.read_text()


def file_exists(file_name):
    return Path(file_name).exists()


def nice_device_to_device(raw_device):
    raw_device = raw_device.split('\0', 1)[0].lower()

    # For x86_64, we only support a few known patterns
    pattern_to_device = (
        ('valve jupiter*', 'steamdeck'),
        ('steamdeck*', 'steamdeck'),
        )

    for pattern, device in pattern_to_device:
        if fnmatch.fnmatch(raw_device, pattern):
            raw_device = device
            break
    else:
        raw_device = raw_device.lower()

    if raw_device not in HW_INFO:
        logger.debug(f"nice_device_to_device -->> {raw_device!r} <<--")
        raw_device = 'default'

    return raw_device.lower()


def new_device_info():
    if HM_TESTING:
        return {
            'name': platform.system(),
            'version': platform.release(),
            'device': 'default',
            }

    info = {}

    # Works on RetroDECK if flatpack deployed to $HOME folder.
    retrodeck_version = safe_cat('/var/config/retrodeck/retrodeck.cfg')
    if retrodeck_version == '':
        retrodeck_version = safe_cat('~/.var/app/net.retrodeck.retrodeck/config/retrodeck/retrodeck.cfg')

    if retrodeck_version != '':
        info['name'] = 'RetroDECK'
        info['version'] = ' '.join(re.findall(r'version=(.*)', retrodeck_version))
        info['device'] = 'retrodeck'

    # Works on Batocera
    batocera_version = safe_cat('/usr/share/batocera/batocera.version')
    if batocera_version != '':
        info.setdefault('name', 'Batocera')
        info['version'] = subprocess.getoutput('batocera-version').strip().split(' ', 1)[0]
        info['device'] = 'steamdeck'

    # Check /etc/os-release for generic Linux systems
    os_release = safe_cat('/etc/os-release')
    for result in re.findall(r'^([a-z0-9_]+)="([^"]+)"$', os_release, re.I | re.M):
        if result[0] in ('NAME', 'VERSION'):
            key = result[0].lower()
            value = result[1].strip()
            info.setdefault(key, value)

    if 'device' not in info:
        info['device'] = 'pc'

    info.setdefault('name', platform.system())
    info.setdefault('version', platform.release())

    logger.info(info)

    return info


def old_device_info():
    # Abandon all hope, ye who enter. 

    # From PortMaster/control.txt
    if file_exists('/dev/input/by-path/platform-ff300000.usb-usb-0:1.2:1.0-event-joystick'):
        if file_exists('/boot/rk3326-rg351v-linux.dtb') or safe_cat("/storage/.config/.OS_ARCH").strip().casefold() == "rg351v":
            # RG351V
            return "rg351v"

        # RG351P/M
        return "rg351p"

    elif file_exists('/dev/input/by-path/platform-odroidgo2-joypad-event-joystick'):
        if "190000004b4800000010000001010000" in safe_cat('/etc/emulationstation/es_input.cfg'):
            return "oga"
        else:
            return "rk2020"

        return "rgb10s"

    elif file_exists('/dev/input/by-path/platform-odroidgo3-joypad-event-joystick'):
        if ("rgb10max" in safe_cat('/etc/emulationstation/es_input.cfg').strip().casefold()):
            return "rgb10max"

        if file_exists('/opt/.retrooz/device'):
            device = safe_cat("/opt/.retrooz/device").strip().casefold()
            if "rgb10max2native" in device:
                return "rgb10max"

            if "rgb10max2top" in device:
                return "rgb10max"

        return "ogs"

    elif file_exists('/dev/input/by-path/platform-gameforce-gamepad-event-joystick'):
        return "chi"

    return 'unknown'


def _merge_info(info, new_info):
    for key, value in new_info.items():
        if key not in info:
            if isinstance(value, (list, tuple)):
                value = value[:]

            elif isinstance(value, dict):
                value = dict(value)

            info[key] = value
            continue

        if isinstance(value, list):
            info[key] = list(set(info[key]) | set(value))

        elif isinstance(value, (str, tuple, int)):
            info[key] = value

    return info


def mem_limits():
    # Lets not go crazy, who gives a fuck over 16gb
    MAX_RAM = 16

    if not hasattr(os, 'sysconf_names'):
        memory = 2

    elif 'SC_PAGE_SIZE' not in os.sysconf_names:
        memory = 2

    elif 'SC_PHYS_PAGES' not in os.sysconf_names:
        memory = 2

    else:
        memory = min(MAX_RAM, math.ceil((os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')) / (1024**3)))

    return memory * 1024


def find_device_by_resolution(resolution):
    for device, information in HW_INFO.items():
        if resolution == information['resolution']:
            return device

    return 'default'


def expand_info(info, override_resolution=None, override_ram=None, use_old_cpu_info=False):
    """
    This turns fetches device info and expands out the capabilities based on that device/cfw.
    """

    _merge_info(info, HW_INFO.get(info['device'], HW_INFO['default']))

    if not use_old_cpu_info:
        cpu_info_v2(info)

    else:
        if f"{info['cpu']}-{info['device']}" in CPU_INFO:
            _merge_info(info, CPU_INFO[f"{info['cpu']}-{info['device']}"])

        elif info['cpu'] in CPU_INFO:
            _merge_info(info, CPU_INFO[info['cpu']])

    if f"{info['name'].lower()}-{info['device']}" in CFW_INFO:
        _merge_info(info, CFW_INFO[f"{info['name'].lower()}-{info['device']}"])

    elif info['name'].lower() in CFW_INFO:
        _merge_info(info, CFW_INFO[info['name'].lower()])

    if override_resolution is not None:
        info['resolution'] = override_resolution

    if override_ram is not None:
        info['ram'] = override_ram

    if use_old_cpu_info:
        _name, _device = info['name'].lower(), info['device'].lower()
        if f"{_name}-{_device}" in GLIBC_INFO:
            info['glibc'] = GLIBC_INFO[f"{_name}-{_device}"]

        elif f"{_name}-*" in GLIBC_INFO:
            info['glibc'] = GLIBC_INFO[f"{_name}-*"]

        elif f"*-{_device}" in GLIBC_INFO:
            info['glibc'] = GLIBC_INFO[f"*-{_device}"]

        else:
            info['glibc'] = GLIBC_INFO['default']

    else:
        info['glibc'] = get_glibc_version()

    display_gcd = math.gcd(info['resolution'][0], info['resolution'][1])
    display_ratio = f"{info['resolution'][0] // display_gcd}:{info['resolution'][1] // display_gcd}"

    if display_ratio == "8:5":
        ## HACK
        info['capabilities'].append("16:9")
        display_ratio = "16:10"

    info['capabilities'].append('restore')

    info['capabilities'].append(display_ratio)
    info['capabilities'].append(f"{info['resolution'][0]}x{info['resolution'][1]}")

    info['capabilities'].append(info['name'])
    info['capabilities'].append(info['device'])

    for i in range(info['analogsticks']+1):
        info['capabilities'].append(f"analog_{i}")

    if info['resolution'][1] < 480:
        info['capabilities'].append("lowres")

    elif info['resolution'][1] > 480:
        info['capabilities'].append("hires")

    if info['resolution'][0] > 640:
        if "hires" not in info['capabilities']:
            info['capabilities'].append("hires")

        if info['resolution'][0] > info['resolution'][1]:
            info['capabilities'].append("wide")

    results = []
    max_memory = info.get('ram', 1024)
    memory = 1024
    while memory <= max_memory:
        info['capabilities'].append(f"{memory // 1024}gb")
        memory *= 2

    return info


__root_info = None
def device_info(override_device=None, override_resolution=None):
    global __root_info
    if override_device is None and override_resolution is None and __root_info is not None:
        return __root_info

    # Best guess at what device we are running on, and what it is capable of.
    info = new_device_info()

    if override_device is not None:
        info['device'] = override_device

    override_ram = mem_limits()

    if info['device'] in ('rg353v', 'rg353p') and override_ram == 1024:
        info['device'] += 's'

    if info['device'] == 'rg-arc-d' and override_ram == 1024:
        info['device'] = 'rg-arc-s'

    expand_info(info, override_resolution, override_ram)

    logger.info(f"DEVICE INFO: {info}")
    __root_info = info
    return info


__all__ = (
    'device_info',
    'expand_info',
    'find_device_by_resolution',
    'HW_INFO',
    'DEVICES',
    )
