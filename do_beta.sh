#!/bin/bash
#
# SPDX-License-Identifier: MIT
#
# Wrapper script for backward compatibility

echo "Using Python setuptools build system..."
python3 -m portmaster.build.release beta "$@"

git add PortMaster/

git commit
