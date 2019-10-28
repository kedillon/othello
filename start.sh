#!/bin/bash

rm -f stop_running

CUDA_VISIBLE_DEVICES=0 nohup ./lead.sh > /dev/null &
CUDA_VISIBLE_DEVICES=0 nohup ./work.sh > /dev/null &
CUDA_VISIBLE_DEVICES=0 nohup ./work.sh > /dev/null &
CUDA_VISIBLE_DEVICES=0 nohup ./work.sh > /dev/null &

CUDA_VISIBLE_DEVICES=1 nohup ./work.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./work.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./work.sh > /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup ./work.sh > /dev/null &
