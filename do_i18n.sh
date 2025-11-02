#!/bin/bash
# SPDX-License-Identifier: MIT
# Wrapper script for backward compatibility

echo "Using Python setuptools i18n system..."
python3 -m portmaster.build.i18n full
exit $?
