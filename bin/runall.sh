#!/bin/bash
# run_simulator

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

CUDA_VISIBLE_DEVICES=0 nohup ./leader.sh > /dev/null &
CUDA_VISIBLE_DEVICES=0 nohup ./worker.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./worker.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./worker.sh > /dev/null &