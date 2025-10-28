#!/bin/bash
#
# SPDX-License-Identifier: MIT
#

# Directory where .pot file is located
POT_DIR="PortMaster/pylibs/locales"
POT_FILES=("messages" "themes")

cp PortMaster/pugwash{,.bak}

python3 tools/pm_release.py $*

awk -F"'" '/PORTMASTER_VERSION = / {print $2}' PortMaster/pugwash > PortMaster/version
cp PortMaster/version version

rm -vf PortMaster.zip

find . -iname '.DS_Store' -or -iname '._*' -delete -print

# for name in $(find . -iname '__pycache__');
# do
#     rm -fRv "$name"
# done

for lang_dir in $POT_DIR/* ; do
    LANG_CODE=$(basename "$lang_dir")
    if [[ "${LANG_CODE}" != "." ]] && [[ "${LANG_CODE}" != ".." ]] && [ -d "$lang_dir" ]; then
        # echo "${LANG_CODE}:"

        for POT_FILE in "${POT_FILES[@]}"; do

            LANG_POT_FILE="$lang_dir/LC_MESSAGES/${POT_FILE}.pot"
            LANG_PO_FILE="$lang_dir/LC_MESSAGES/${POT_FILE}.po"
            LANG_MO_FILE="$lang_dir/LC_MESSAGES/${POT_FILE}.mo"

            if [ -f "$LANG_POT_FILE" ]; then
                mv -fv "$LANG_POT_FILE" "$LANG_PO_FILE"
            fi

            # Compile .po file into .mo file
            # printf "msgfmt: "
            msgfmt -v -o "${LANG_MO_FILE}" "${LANG_PO_FILE}"

            # echo ""
        done
    fi
done

echo "Exporting dependencies with Poetry"
# Create a temporary directory for dependencies
DEPS_DIR="PortMaster/deps"
rm -rf "$DEPS_DIR"
mkdir -p "$DEPS_DIR"

# Generate requirements.txt from pyproject.toml using Python's tomllib
python3 << 'PYTHON_SCRIPT'
import tomllib
import os

# Read pyproject.toml
with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)

# Extract dependencies
deps = data['tool']['poetry']['dependencies']
reqs = []
for pkg, version in deps.items():
    if pkg == 'python':
        continue
    # Convert version format
    if isinstance(version, str):
        if version.startswith('^'):
            reqs.append(f"{pkg}>={version[1:]}")
        else:
            reqs.append(f"{pkg}=={version}")
    else:
        reqs.append(pkg)

# Write to requirements file
os.makedirs('PortMaster/deps', exist_ok=True)
with open('PortMaster/deps/requirements.txt', 'w') as f:
    f.write('\n'.join(reqs))

print("Generated requirements.txt")
PYTHON_SCRIPT

# Install dependencies to the deps directory
pip install -r "$DEPS_DIR/requirements.txt" -t "$DEPS_DIR" --no-deps --quiet

# Clean up unnecessary files from dependencies
find "$DEPS_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$DEPS_DIR" -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find "$DEPS_DIR" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find "$DEPS_DIR" -name "*.pyc" -delete
find "$DEPS_DIR" -name "*.pyo" -delete
rm -f "$DEPS_DIR/requirements.txt"

echo "Creating pylibs.zip"
cd PortMaster

rm -f pylibs.zip
zip -9r pylibs.zip pylibs/ deps/ \
    -x \*__pycache__\*/\* \
    -x \*.DS_Store \
    -x ._\* \
    -x \*NotoSans\*.ttf

cd ..

echo "Creating PortMaster.zip"
zip -9r PortMaster.zip PortMaster/ \
    -x PortMaster/pylibs/\* \
    -x PortMaster/deps/\* \
    -x PortMaster/config/\* \
    -x PortMaster/themes/\* \
    -x PortMaster/libs/\*.squashfs \
    -x PortMaster/libs/\*.squashfs.md5 \
    -x PortMaster/pugwash.bak \
    -x PortMaster/log.txt \
    -x PortMaster/pugwash.txt \
    -x PortMaster/harbourmaster.txt \
    -x '*.DS_Store'

if [[ "$1" == "stable" ]] || [ "$MAKE_INSTALL" = "Y" ]; then
    echo "Creating Installers"

    for arch in "aarch64" "x86_64"; do
        export RUNTIME_ARCH="$arch"

        if [ ! -f "runtimes.${RUNTIME_ARCH}.zip" ]; then
            echo "Downloading Runtimes for $RUNTIME_ARCH."
            mkdir -p runtimes
            cd runtimes
            ../tools/download_runtimes.sh
            zip -9 "../runtimes.${RUNTIME_ARCH}.zip" *
            cd ..
            rm -fRv runtimes
        fi
    done

    if [ ! -d "makeself-2.5.0" ]; then
        echo "Downloading makeself"
        wget "https://github.com/megastep/makeself/releases/download/release-2.5.0/makeself-2.5.0.run"
        chmod +x makeself-2.5.0.run
        ./makeself-2.5.0.run
    fi

    echo "Building Release"
    mkdir -p pm_release
    cd pm_release
    cp ../PortMaster.zip .
    cp ../tools/installer.sh .
    cd ..

    # Remove old installers
    rm -f Install*PortMaster.sh

    makeself-2.5.0/makeself.sh --header "tools/makeself-header.sh" pm_release "Install.PortMaster.sh" "PortMaster Installer" ./installer.sh

    if [ -z "$NO_FULL_INSTALL" ]; then
        for arch in "aarch64" "x86_64"; do
            export RUNTIME_ARCH="$arch"

            if [ "$RUNTIME_ARCH" = "aarch64" ]; then
                SCRIPT_NAME=""
            else
                SCRIPT_NAME=".${RUNTIME_ARCH}"
            fi

            cd pm_release
            cp "../runtimes.${RUNTIME_ARCH}.zip" runtimes.zip
            cd ..

            makeself-2.5.0/makeself.sh --header "tools/makeself-header.sh" pm_release "Install.Full${SCRIPT_NAME}.PortMaster.sh" "PortMaster Full Installer" ./installer.sh
        done
    fi

    rm -fRv pm_release
fi

if [[ ! -f "version.json" ]]; then
    wget "https://github.com/PortsMaster/PortMaster-GUI/releases/latest/download/version.json"
fi

python3 tools/pm_version.py $*

# Restore this file
mv PortMaster/pugwash{.bak,}
