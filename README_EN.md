# RSS Anime Collection

This repository contains scripts for managing and automating your anime downloads and organization.

## Setup

1. **Clone the repository**:
    ```
    git clone https://github.com/Cheolhwi/RSS-Anime-collection.git
    ```

2. **Configure qBittorrent**:
    - For `run_after_done.sh`:
      Need to change the path in the shell script:
      ```
      output=$(python3 /path_of_your_folder/rename_anime.py --name="$file_name" --root="$directory")
      ```
      Then configure the qBittorent in Setting -> downloads, scroll down find **Run on torrent finished** add the prompt
      ```
      /path_of_your_folder/run_after_done.sh "%F" "%D"
      ```

3. **Set up cron job for `update_folder.sh`**:
    ```
    crontab -e
    ```
    Need to change the path in the shell script and Add the following line:
    ```
    0 0 1 */6 * /path_of_your_folder/update_folder.sh
    ```
4. **Subscribe the RSS link in qBittorrent**
   for me I use the nyaa RSS feed link for chinese traditional language: https://nyaa.si/?page=rss&q=CHT&c=0_0&f=0