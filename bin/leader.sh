#!/bin/bash
# run_simulator

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

export PYTHONPATH=.

# Worker just runs self play
while true; do
  python simulator/run.py
  if [ -e stop_running ]; then
    exit
  fi

  python lib/ml/run.py >> training.log
  if [ -e stop_running ]; then
    exit
  fi
done