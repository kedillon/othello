#!/bin/bash
# run_simulator

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

# Worker just runs self play
while true; do
  python simulator/run.py
done