#!/bin/bash

touch stop_running
kill $(pgrep python)
sleep 5
rm -f stop_running