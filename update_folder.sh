#!/bin/bash

# 定义源目录和目标目录
src_dir="/Volumes/media/anime/new_update"
dest_dir="/Volumes/media/anime/history"

# 获取当前日期和上次移动的日期
current_date=$(date +%s)
last_move_date_file="/tmp/last_move_date.txt"

# 如果上次移动日期文件不存在，则创建它并设置初始日期为当前日期
if [ ! -f "$last_move_date_file" ]; then
    echo "$current_date" > "$last_move_date_file"
    echo "Initialized last move date to current date."
    exit 0
fi

# 读取上次移动的日期
last_move_date=$(cat "$last_move_date_file")

# 计算时间差（秒）
time_diff=$((current_date - last_move_date))

# 6个月的秒数
six_months_seconds=$((6 * 30 * 24 * 60 * 60))

# 如果时间差大于或等于6个月，则移动文件
if [ "$time_diff" -ge "$six_months_seconds" ]; then
    echo "Moving files from $src_dir to $dest_dir"

    # 如果目标目录不存在，则创建它
    if [ ! -d "$dest_dir" ]; then
        mkdir -p "$dest_dir"
        echo "Created directory $dest_dir"
    fi

    # 移动文件
    mv "$src_dir"/* "$dest_dir"/

    # 更新上次移动的日期
    echo "$current_date" > "$last_move_date_file"
    echo "Files moved and last move date updated."
else
    echo "Less than 6 months since last move. No files moved."
fi
