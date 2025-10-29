#!/bin/bash
#
# SPDX-License-Identifier: MIT
#
# Wrapper script for backward compatibility

./do_i18n.sh

echo "Using Python setuptools build system..."
python3 -m portmaster.build.release stable "$@"

git add PortMaster/

git commit
