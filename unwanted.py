import os
from pathlib import Path

unwanted_list_path = "/Volumes/media/anime/unwanted_list.txt"
root_directory = "/Volumes/media/anime/new_update"  # 更新这个路径为你的根目录

def load_unwanted_list():
    if os.path.exists(unwanted_list_path):
        with open(unwanted_list_path, 'r', encoding='utf-8') as f:
            unwanted_list = [line.strip() for line in f.readlines()]
            return unwanted_list
    return []

def delete_unwanted_files(root, unwanted_list):
    for unwanted in unwanted_list:
        for item in Path(root).rglob(f'*{unwanted}*'):
            if item.is_file() or item.is_dir():
                print(f"Deleting {item}")
                if item.is_dir():
                    for sub_item in item.rglob('*'):
                        if sub_item.is_file():
                            sub_item.unlink()
                        else:
                            delete_unwanted_files(sub_item, unwanted_list)
                    item.rmdir()
                else:
                    item.unlink()

if __name__ == "__main__":
    unwanted_list = load_unwanted_list()
    if unwanted_list:  # 检查列表是否为空
        delete_unwanted_files(root_directory, unwanted_list)
