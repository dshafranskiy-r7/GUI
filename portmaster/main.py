#!/usr/bin/env python3
"""
Main entry point for PortMaster GUI
Wraps the existing pugwash script
"""

import sys
import os
from pathlib import Path


def main():
    """Run the PortMaster GUI"""
    # Get the PortMaster directory
    portmaster_dir = Path(__file__).parent.parent / "PortMaster"
    
    # Change to PortMaster directory
    os.chdir(portmaster_dir)
    
    # Add to path
    sys.path.insert(0, str(portmaster_dir))
    
    # Import and run pugwash
    import runpy
    runpy.run_path(str(portmaster_dir / "pugwash"), run_name="__main__")


if __name__ == "__main__":
    main()
