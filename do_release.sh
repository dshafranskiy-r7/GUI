#!/bin/bash
#
# SPDX-License-Identifier: MIT
#
# Wrapper script for backward compatibility
# Calls the new Python-based setuptools build system

# Parse arguments
RELEASE_TYPE="alpha"
MAKE_INSTALL=""

if [[ "$1" == "stable" ]] || [ "$MAKE_INSTALL" = "Y" ]; then
    MAKE_INSTALL="--make-install"
fi

if [[ -n "$1" ]]; then
    RELEASE_TYPE="$1"
fi

# Call the Python build system
echo "Using Python setuptools build system..."
python3 -m portmaster.build.release "$RELEASE_TYPE" $MAKE_INSTALL

# Exit with the same code
exit $?
