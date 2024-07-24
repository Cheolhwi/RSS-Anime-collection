#!/bin/bash

# 获取传递的参数
file_name="$1"
directory="$2"

# 记录传递的参数
echo "File name: $file_name" > /tmp/qbittorrent_log.txt
echo "Directory: $directory" >> /tmp/qbittorrent_log.txt

# 运行Python脚本，并获取重命名后的信息
output=$(python3 /Volumes/media/anime/rename_anime.py --name="$file_name" --root="$directory")
anime_name=$(echo $output | cut -d',' -f1)
new_name=$(echo $output | cut -d',' -f2)
new_path=$(echo $output | cut -d',' -f3)

# 记录Python脚本输出
echo "Python script output: $output" >> /tmp/qbittorrent_log.txt

# 如果重命名成功并且新路径不为空
if [ -n "$anime_name" ] && [ -n "$new_name" ] && [ -n "$new_path" ]; then
    echo "Moved $new_name to $new_path" >> /tmp/qbittorrent_log.txt
else
    echo "Renaming or moving failed." >> /tmp/qbittorrent_log.txt
fi
