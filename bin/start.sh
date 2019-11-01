#!/bin/bash

rm -f stop_running

CUDA_VISIBLE_DEVICES=0 nohup ./leader.sh > /dev/null &
CUDA_VISIBLE_DEVICES=0 nohup ./worker.sh > /dev/null &
CUDA_VISIBLE_DEVICES=0 nohup ./worker.sh > /dev/null &
CUDA_VISIBLE_DEVICES=0 nohup ./worker.sh > /dev/null &

CUDA_VISIBLE_DEVICES=1 nohup ./worker.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./worker.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./worker.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./worker.sh > /dev/null &