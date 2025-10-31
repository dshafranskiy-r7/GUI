#!/usr/bin/env python3
"""
Runtime downloader module for PortMaster
Replaces the tools/download_runtimes.sh script
"""

import argparse
import hashlib
import json
import requests
import sys
from pathlib import Path


def download_file(url, filename):
    """Download a file using requests"""
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except requests.RequestException as e:
        print(f"Error downloading {filename}: {e}")
        return False


def verify_md5(filename, expected_md5):
    """Verify MD5 checksum of a file"""
    md5_obj = hashlib.md5()

    with open(filename, 'rb') as fh:
        for data in iter(lambda: fh.read(4096), b''):
            md5_obj.update(data)

    actual_md5 = md5_obj.hexdigest()

    if actual_md5 != expected_md5:
        print(f"MD5 mismatch for {filename}! Expected {expected_md5}, got {actual_md5}")
        return False

    print(f"MD5 OK for {filename}")
    return True


def download_runtimes(runtime_arch="aarch64"):
    """Download runtime files for specified architecture"""

    print(f"Downloading runtimes for {runtime_arch}...")

    # Download ports.json
    ports_json = Path("ports.json")
    if not ports_json.exists():
        print("Downloading ports.json...")

        # Get latest release URL
        try:
            response = requests.get("https://api.github.com/repos/PortsMaster/PortMaster-New/releases/latest")
            response.raise_for_status()

            release_data = response.json()
            ports_json_url = None

            for asset in release_data.get("assets", []):
                if asset.get("name") == "ports.json":
                    ports_json_url = asset.get("browser_download_url")
                    break

            if not ports_json_url:
                print("Error: Could not find ports.json in latest release")
                return False

            if not download_file(ports_json_url, "ports.json"):
                print("Error: Failed to download ports.json")
                return False

        except requests.RequestException as e:
            print(f"Error: Failed to get latest release info: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse release data: {e}")
            return False

    # Parse ports.json and download runtimes
    try:
        with open("ports.json", "r") as f:
            ports_data = json.load(f)

        utils = ports_data.get("utils", {})
        downloaded_count = 0

        for key, value in utils.items():
            # Skip images and gameinfo
            if "images" in key.lower() or "gameinfo" in key.lower():
                continue

            # Check runtime_arch
            if value.get("runtime_arch") != runtime_arch:
                continue

            url = value.get("url")
            runtime_name = value.get("runtime_name")
            md5 = value.get("md5")

            if not url or not runtime_name:
                continue

            # Download the file
            if download_file(url, runtime_name):
                # Verify MD5 if provided
                if md5:
                    if not verify_md5(runtime_name, md5):
                        Path(runtime_name).unlink()
                        continue

                downloaded_count += 1

        print(f"\nDownloaded {downloaded_count} runtime files")

    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse ports.json: {e}")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        # Clean up ports.json
        if ports_json.exists():
            ports_json.unlink()

    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Download PortMaster runtime files")
    parser.add_argument(
        '--arch',
        default='aarch64',
        choices=['aarch64', 'x86_64', 'armhf'],
        help='Runtime architecture (default: aarch64)'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory (default: current directory)'
    )

    args = parser.parse_args()

    # Change to output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    import os
    os.chdir(output_dir)

    # Download runtimes
    success = download_runtimes(args.arch)

    if success:
        print("\nRuntime download complete!")
        sys.exit(0)
    else:
        print("\nRuntime download failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
