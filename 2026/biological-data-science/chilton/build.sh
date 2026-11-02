#!/usr/bin/env bash
# Rebuild poster.pdf and poster.svg from poster.typ (Typst 0.15.0 via uv).
set -euo pipefail
cd "$(dirname "$0")"
uvx --from typst==0.15.0 python render.py
