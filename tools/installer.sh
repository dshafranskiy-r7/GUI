#!/bin/bash
#
# SPDX-License-Identifier: MIT
#
# Wrapper script for backward compatibility

echo "Using Python setuptools installer..."
python3 -m portmaster.build.installer "$@"

exit $?
