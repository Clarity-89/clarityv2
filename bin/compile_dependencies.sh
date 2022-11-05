#!/bin/bash

#
# Compile the dependencies for production, CI and development.
#
# Usage, in the root of the project:
#
#     ./bin/compile_dependencies.sh
#
# Any extra flags/arguments passed to this wrapper script are passed down to pip-compile.
# E.g. to update a package:
#
#     ./bin/compile_dependencies.sh --upgrade-package django

set -ex

toplevel=$(git rev-parse --show-toplevel)

cd $toplevel

export CUSTOM_COMPILE_COMMAND="./bin/compile_dependencies.sh"

# Base (& prod) deps
pip-compile \
    --no-emit-index-url \
    --allow-unsafe \
    "$@" \
    requirements/base.in

# Dependencies for testing
pip-compile \
    --no-emit-index-url \
    --allow-unsafe \
    --output-file requirements/test.txt \
    "$@" \
    requirements/base.txt \
    requirements/test-tools.in

# Dev dependencies
pip-compile \
    --no-emit-index-url \
    --allow-unsafe \
    --output-file requirements/dev.txt \
    "$@" \
    requirements/base.txt \
    requirements/dev.in