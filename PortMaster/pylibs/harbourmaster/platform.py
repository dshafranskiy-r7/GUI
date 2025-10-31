
# SPDX-License-Identifier: MIT

# System imports
import contextlib
import datetime
import json
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile

from gettext import gettext as _
from pathlib import Path

# Included imports

from loguru import logger
from utility import cprint, cstrip

# Module imports
from .config import *
from .hardware import *
from .util import *

SPECIAL_GAMELIST_CODE = object()

class PlatformBase():
    WANT_XBOX_FIX = False
    WANT_SWAP_BUTTONS = False

    MOVE_PM_BASH = False
    MOVE_PM_BASH_DIR = None
    ES_NAME = None
    ROMS_REFRESH_TEXT = ""

    XML_ELEMENT_MAP = {
        'path': 'path',
        'name': 'name',
        'image': 'image',
        'desc': 'desc',
        'releasedate': 'releasedate',
        'developer': 'developer',
        'publisher': 'publisher',
        'players': 'players',
        'genre': 'genre',
        }

    XML_ELEMENT_CALLBACK = {
        }

    XML_PATH_FIX = [
        'image',
        ]

    BLANK_GAMELIST_XML = """<?xml version='1.0' encoding='utf-8'?>\n<gameList />\n"""

    def __init__(self, hm):
        self.hm = hm
        self.added_ports = set()
        self.removed_ports = set()

    def loaded(self):
        ...

    def do_move_ports(self):
        ...

    def gamelist_file(self):
        return None

    @contextlib.contextmanager
    def gamelist_backup(self):
        if not hasattr(self, '_GAMELIST_BACKUP'):
            self._GAMELIST_BACKUP = 0

        gamelist_xml = self.gamelist_file()

        if gamelist_xml in (None, SPECIAL_GAMELIST_CODE):
            try:
                yield gamelist_xml

            finally:
                return

        gamelist_xml = self.gamelist_file()
        gamelist_bak = gamelist_xml.with_name(gamelist_xml.name + '.bak')

        broken = False
        if not gamelist_xml.is_file():
            if gamelist_bak.is_file():
                logger.debug(f"Restore {gamelist_bak} to {gamelist_xml}")
                shutil.copy(gamelist_bak, gamelist_xml)

            else:
                broken = True

        elif gamelist_xml.is_file() and gamelist_xml.stat().st_size == 0:
            if gamelist_bak.is_file():
                logger.debug(f"Restore {gamelist_bak} to {gamelist_xml}")
                shutil.copy(gamelist_bak, gamelist_xml)

            else:
                broken = True

        if broken:
            logger.debug(f"Creating empty {gamelist_xml}")
            with open(gamelist_xml, 'w') as fh:
                print(self.BLANK_GAMELIST_XML, file=fh)

        try:
            if self._GAMELIST_BACKUP == 0:
                logger.debug(f"Backing up {gamelist_xml} to {gamelist_bak}")
                shutil.copy(gamelist_xml, gamelist_bak)

            self._GAMELIST_BACKUP += 1

            yield gamelist_xml

        except:
            if self._GAMELIST_BACKUP == 1:
                logger.debug(f"Restoring {gamelist_bak} to {gamelist_xml}")
                shutil.copy(gamelist_bak, gamelist_xml)

            raise

        finally:
            self._GAMELIST_BACKUP -= 1
            return

    def gamelist_add(self, gameinfo_file):
        if not gameinfo_file.is_file():
            return

        FIX_PATH = self.hm.ports_dir != self.hm.scripts_dir

        with self.gamelist_backup() as gamelist_xml:
            if gamelist_xml is None:
                return

            gamelist_tree = ET.parse(gamelist_xml)
            gamelist_root = gamelist_tree.getroot()

            gameinfo_tree = ET.parse(gameinfo_file)
            gameinfo_root = gameinfo_tree.getroot()

            for gameinfo_element in gameinfo_tree.findall('game'):
                path_merge = gameinfo_element.find('path').text

                gamelist_update = gamelist_root.find(f'.//game[path="{path_merge}"]')
                if gamelist_update is None:
                    # Create a new game element
                    gamelist_update = ET.SubElement(gamelist_root, 'game')

                logger.info(f'{path_merge}: ')

                for child in gameinfo_element:
                    # Check if the child element is in the predefined list
                    if child.tag in self.XML_ELEMENT_MAP:
                        gamelist_element = gamelist_update.find(self.XML_ELEMENT_MAP[child.tag])

                        if gamelist_element is None:
                            gamelist_element = ET.SubElement(gamelist_update, self.XML_ELEMENT_MAP[child.tag])

                        if FIX_PATH and child.tag in self.XML_PATH_FIX:
                            new_path = child.text.strip()
                            if new_path.startswith('./'):
                                new_path = new_path[2:]

                            gamelist_element.text = str(self.hm.ports_dir / new_path)

                        else:
                            gamelist_element.text = child.text

                for child in gameinfo_element:
                    if child.tag in self.XML_ELEMENT_CALLBACK:
                        if FIX_PATH and child.tag in self.XML_PATH_FIX:
                            new_path = child.text.strip()
                            if new_path.startswith('./'):
                                new_path = new_path[2:]

                            child.text = str(self.hm.ports_dir / new_path)

                        self.XML_ELEMENT_CALLBACK[child.tag](path_merge, gamelist_update, child)

            if hasattr(ET, 'indent'):
                ET.indent(gamelist_root, space="  ", level=0)

            with open(gamelist_xml, 'w') as fh:
                print("<?xml version='1.0' encoding='utf-8'?>", file=fh)
                print("", file=fh)
                print(ET.tostring(gamelist_root, encoding='unicode'), file=fh)

            self.added_ports.add('GAMELIST UPDATER')

    def ports_changed(self):
        return (len(self.added_ports) > 0 or len(self.removed_ports) > 0)

    def first_run(self):
        """
        Called on first run, this can be used to add custom sources for your platform.
        """
        logger.debug(f"{self.__class__.__name__}: First Run")

    def port_install(self, port_name, port_info, port_files):
        """
        Called on after a port is installed, this can be used to check permissions, possibly augment the bash scripts.
        """
        logger.debug(f"{self.__class__.__name__}: Port Install {port_name}")

        if port_name in self.removed_ports:
            self.removed_ports.remove(port_name)
        else:
            self.added_ports.add(port_name)

    def runtime_install(self, runtime_name, runtime_files):
        """
        Called on after a port is installed, this can be used to check permissions, possibly augment the bash scripts.
        """
        logger.debug(f"{self.__class__.__name__}: Runtime Install {runtime_name}")

    def port_uninstall(self, port_name, port_info, port_files):
        """
        Called on after a port is uninstalled, this can be used clean up special files.
        """
        logger.debug(f"{self.__class__.__name__}: Port Uninstall {port_name}")

        if port_name in self.added_ports:
            self.added_ports.remove(port_name)
        else:
            self.removed_ports.add(port_name)

    def portmaster_install(self):
        """
        Called on after portmaster is updated, this can be used clean up special files.
        """
        logger.debug(f"{self.__class__.__name__}: PortMaster Install")

    def set_gcd_mode(self, mode=None):
        logger.info(f"{self.__class__.__name__}: Set GCD Mode {mode}")

    def get_gcd_modes(self):
        return tuple()

    def get_gcd_mode(self):
        logger.debug(f"{self.__class__.__name__}: Get GCD Mode")
        return None


class PlatformTesting(PlatformBase):
    WANT_XBOX_FIX = False
    WANT_SWAP_BUTTONS = False

    def gamelist_file(self):
        return self.hm.scripts_dir / 'gamelist.xml'



HM_PLATFORMS = {
    'darwin':    PlatformTesting,
    'default':   PlatformBase,
    }


__all__ = (
    'PlatformBase',
    'HM_PLATFORMS',
    )
