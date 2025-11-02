#!/bin/bash
# SPDX-License-Identifier: MIT
# Wrapper script for backward compatibility

echo "Using Python setuptools runtime downloader..."
python3 -m portmaster.build.runtimes --arch "${RUNTIME_ARCH:-aarch64}"
exit $?
