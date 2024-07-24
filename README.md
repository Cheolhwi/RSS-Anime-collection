# RSS Anime Collection

用于管理和自动化动漫下载和整理的脚本。

## 设置

1. **克隆仓库**：
    ```
    git clone https://github.com/Cheolhwi/RSS-Anime-collection.git
    ```

2. **配置qBittorrent**：
    - 对于 `run_after_done.sh`：
      需要更改脚本中的路径：
      ```
      output=$(python3 /path_of_your_folder/rename_anime.py --name="$file_name" --root="$directory")
      ```
      然后在qBittorrent设置中，进入 **设置** -> **下载**，向下滚动找到 **完成后运行程序**，添加以下命令：
      ```
      /path_of_your_folder/run_after_done.sh "%F" "%D"
      ```

3. **设置`update_folder.sh`的定时任务**：
    ```
    crontab -e
    ```
    需要更改脚本中的路径，并添加以下行：
    ```
    0 0 1 */6 * /path_of_your_folder/update_folder.sh
    ```

4. **在qBittorrent中订阅RSS链接**：
    我使用的是nyaa的繁体中文RSS订阅链接： https://nyaa.si/?page=rss&q=CHT&c=0_0&f=0

5. **修改unwanted_list.txt**：
    对于不想追或者不想再看的番剧可以根据之前运行过生成的animelist.txt列表中添加至unwanted_list.txt,这样做就不会保留该番剧的文件和文件夹。

## 英文版README

[English Version README](README_EN.md)
