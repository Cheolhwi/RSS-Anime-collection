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
        print(f"Looking for items containing: {unwanted}")
        for item in Path(root).iterdir():  # 仅检查根目录中的文件和文件夹
            if unwanted in item.name:
                print(f"Found item: {item}")
                try:
                    if item.is_file():
                        print(f"Deleting file: {item}")
                        os.chmod(item, 0o777)  # 修改权限以确保可以删除
                        item.unlink()
                        print(f"Deleted file: {item}")
                    elif item.is_dir():
                        print(f"Deleting directory: {item}")
                        for sub_item in item.rglob('*'):
                            if sub_item.is_file():
                                print(f"Deleting file in directory: {sub_item}")
                                os.chmod(sub_item, 0o777)  # 修改权限以确保可以删除
                                sub_item.unlink()
                                print(f"Deleted file in directory: {sub_item}")
                            elif sub_item.is_dir():
                                print(f"Deleting sub-directory: {sub_item}")
                                os.chmod(sub_item, 0o777)  # 修改权限以确保可以删除
                                sub_item.rmdir()
                                print(f"Deleted sub-directory: {sub_item}")
                        os.chmod(item, 0o777)  # 修改权限以确保可以删除
                        item.rmdir()
                        print(f"Deleted directory: {item}")
                except Exception as e:
                    print(f"Error deleting {item}: {e}")

if __name__ == "__main__":
    unwanted_list = load_unwanted_list()
    if unwanted_list:  # 检查列表是否为空
        print(f"Unwanted list: {unwanted_list}")
        print(f"Contents of root directory: {list(Path(root_directory).iterdir())}")
        delete_unwanted_files(root_directory, unwanted_list)
    else:
        print("Unwanted list is empty. No files to delete.")
