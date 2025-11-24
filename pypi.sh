#!/bin/sh
# Build and upload using uv and Twine
set -euo pipefail

rm -rf dist
uv build
uv run --with twine twine upload dist/*
