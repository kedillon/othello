#!/bin/bash

export PYTHONPATH=.

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
