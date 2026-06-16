#!/bin/bash

# 解决输出缓冲问题
export PYTHONUNBUFFERED=1
# 可选：设置 UTF-8 编码
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

LOG_DIR="./logs"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$LOG_DIR/scan_$DATE.log"

mkdir -p "$LOG_DIR"

python3 client_run.py 2>&1 | tee -a "$LOG_FILE"