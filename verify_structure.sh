#!/bin/bash
#
# SPDX-License-Identifier: MIT
#
# Verification script for repository restructuring
# This script checks that all symlinks are correctly set up
# and the new structure is working properly.

echo "================================================"
echo "PortMaster Repository Structure Verification"
echo "================================================"
echo ""

ERRORS=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a path exists
check_path() {
    local path=$1
    local description=$2
    
    if [ -e "$path" ]; then
        echo -e "${GREEN}✓${NC} $description: $path"
        return 0
    else
        echo -e "${RED}✗${NC} $description: $path (NOT FOUND)"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Function to check if a symlink points to the correct target
check_symlink() {
    local link=$1
    local expected_target=$2
    local description=$3
    
    if [ -L "$link" ]; then
        local actual_target=$(readlink "$link")
        if [ "$actual_target" = "$expected_target" ]; then
            echo -e "${GREEN}✓${NC} $description: $link → $actual_target"
            return 0
        else
            echo -e "${YELLOW}⚠${NC} $description: $link → $actual_target (expected: $expected_target)"
            ERRORS=$((ERRORS + 1))
            return 1
        fi
    else
        echo -e "${RED}✗${NC} $description: $link (NOT A SYMLINK)"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

echo "Checking directory structure..."
echo "-------------------------------"
check_path "build" "Build directory"
check_path "build/scripts" "Build scripts directory"
check_path "build/tools" "Build tools directory"
check_path "dependencies" "Dependencies directory"
check_path "dependencies/exlibs" "External libraries"
check_path "resources" "Resources directory"
check_path "resources/binaries" "Binaries directory"
check_path "resources/binaries/aarch64" "ARM64 binaries"
check_path "resources/binaries/armhf" "ARM32 binaries"
check_path "resources/binaries/x86_64" "x86_64 binaries"
check_path "resources/platforms" "Platforms directory"
check_path "resources/platforms/config" "Platform configs"
echo ""

echo "Checking build scripts..."
echo "------------------------"
check_path "build/scripts/do_release.sh" "Main release script"
check_path "build/scripts/do_muos_release.sh" "muOS release script"
check_path "build/scripts/do_trimui_release.sh" "TrimUI release script"
check_path "build/scripts/do_x86_64_release.sh" "x86_64 release script"
echo ""

echo "Checking key symlinks..."
echo "-----------------------"
check_symlink "PortMaster/exlibs" "../dependencies/exlibs" "External libraries symlink"
check_symlink "PortMaster/gptokeyb" "../resources/binaries/aarch64/gptokeyb" "gptokeyb symlink"
check_symlink "PortMaster/miyoo" "../resources/platforms/miyoo" "Miyoo platform symlink"
check_symlink "PortMaster/muos" "../resources/platforms/muos" "muOS platform symlink"
check_symlink "PortMaster/mod_muOS.txt" "../resources/platforms/config/mod_muOS.txt" "Config file symlink"
echo ""

echo "Checking platform directories..."
echo "-------------------------------"
for platform in miyoo muos trimui batocera knulli retrodeck; do
    check_path "resources/platforms/$platform" "$platform directory"
done
echo ""

echo "Checking binary files..."
echo "-----------------------"
for arch in aarch64 armhf x86_64; do
    if [ "$arch" = "aarch64" ] || [ "$arch" = "armhf" ]; then
        check_path "resources/binaries/$arch/7zzs.$arch" "7zzs binary for $arch"
    fi
    
    if [ "$arch" != "aarch64" ]; then
        check_path "resources/binaries/$arch/gptokeyb.$arch" "gptokeyb binary for $arch"
        check_path "resources/binaries/$arch/xdelta3.$arch" "xdelta3 binary for $arch"
    else
        check_path "resources/binaries/$arch/gptokeyb" "gptokeyb binary for $arch"
        check_path "resources/binaries/$arch/xdelta3" "xdelta3 binary for $arch"
    fi
done
echo ""

echo "Checking documentation..."
echo "------------------------"
check_path "STRUCTURE.md" "Structure documentation"
check_path "MIGRATION_GUIDE.md" "Migration guide"
echo ""

echo "Testing Python imports..."
echo "------------------------"
cd PortMaster
if python3 -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('exlibs'))); sys.path.insert(0, str(Path('pylibs'))); import harbourmaster" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Python imports work correctly"
else
    echo -e "${RED}✗${NC} Python imports failed"
    ERRORS=$((ERRORS + 1))
fi
cd ..
echo ""

echo "================================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo "The repository structure is correctly set up."
    exit 0
else
    echo -e "${RED}✗ Found $ERRORS error(s)${NC}"
    echo "Please review the errors above and fix any issues."
    exit 1
fi
