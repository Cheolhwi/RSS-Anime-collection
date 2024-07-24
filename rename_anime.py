import re
import os
import io
import sys
import os.path as op
import argparse
import codecs
from pathlib import Path

# 设置日志文件路径
log_name = op.join(op.dirname(op.realpath(__file__)), 'log.txt')
# 设置不需要的番剧列表路径
unwanted_list_path = "/Volumes/media/anime/unwanted_list.txt"

# 定义匹配规则
episode_rules = [
    r'(.*)\[(\d{1,3}|\d{1,3}\.\d{1,2})(?:v\d{1,2})?(?:END)?\](.*)',
    r'(.*)\[E(\d{1,3}|\d{1,3}\.\d{1,2})(?:v\d{1,2})?(?:END)?\](.*)',
    r'(.*)\[第(\d*\.*\d*)话(?:END)?\](.*)',
    r'(.*)\[第(\d*\.*\d*)話(?:END)?\](.*)',
    r'(.*)第(\d*\.*\d*)话(?:END)?(.*)',
    r'(.*)第(\d*\.*\d*)話(?:END)?(.*)',
    r'(.*)- (\d{1,3}|\d{1,3}\.\d{1,2})(?:v\d{1,2})?(?:END)? (.*)'
]

# 支持的文件后缀
suffixs = ['mp4', 'mkv', 'avi', 'mov', 'flv', 'rmvb', 'ass', 'idx']

# 设置输出编码
sys.stdout = io.TextIOWrapper(buffer=sys.stdout.buffer, encoding='utf8')

# 解析输入参数
parser = argparse.ArgumentParser(description='Regular Expression Match')
parser.add_argument('--root', default='',
                    help='The root directory of the input file.')
parser.add_argument('--name', default='',
                    help='The file name of the input file.')
parser.add_argument('--path', default='',
                    help='The file full path of the input file.')

def load_unwanted_list():
    if os.path.exists(unwanted_list_path):
        with open(unwanted_list_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    return []

def check_file_size(root, name):
    file_path = root / name
    file_size = file_path.stat().st_size
    file_size_gb = file_size / (1024 ** 3)  # 转换为GB
    if file_size_gb > 1:
        print(f"File {name} is larger than 1GB, deleting it.")
        os.remove(file_path)
        sys.exit()

def rename_and_move(root, name, unwanted_list):
    root = Path(root)
    check_file_size(root, name)  # 检查文件大小
    for rule in episode_rules:
        matchObj = re.match(rule, name, re.I)
        if matchObj is not None:
            anime_name = matchObj.group(1).strip()
            if anime_name in unwanted_list:
                print(f"Anime {anime_name} is in unwanted list, deleting {name}.")
                os.remove(root / name)
                return None, None, None
            episode_number = matchObj.group(2).strip()
            new_name = f'{anime_name} E{episode_number}{Path(name).suffix}'
            print(f'Renaming: {name} -> {new_name}')
            with codecs.open(log_name, 'a+', 'utf-8') as f:
                print(f'Renaming: {name} -> {new_name}', file=f)
            new_path = root / new_name
            os.rename(str(root/name), str(new_path))
            create_and_move(root, anime_name, new_path)
            update_animelist(anime_name)
            return anime_name, new_name, new_path
    return general_check(root, name, unwanted_list)

def general_check(root, name, unwanted_list):
    new_name = ' '.join(name.split())
    if new_name != name:
        print(f'General Check Renaming: {name} -> {new_name}')
        with codecs.open(log_name, 'a+', 'utf-8') as f:
            print(f'General Check Renaming: {name} -> {new_name}', file=f)
        new_path = root / new_name
        os.rename(str(root/name), str(new_path))
        anime_name = Path(new_name).stem
        if anime_name in unwanted_list:
            print(f"Anime {anime_name} is in unwanted list, deleting {new_name}.")
            os.remove(new_path)
            return None, None, None
        update_animelist(anime_name)
        create_and_move(root, anime_name, new_path)
        return anime_name, new_name, new_path
    return None, None, None

def create_and_move(root, anime_name, new_path):
    anime_folder = root / anime_name
    if not anime_folder.exists():
        print(f'Creating folder: {anime_folder}')
        anime_folder.mkdir()
    final_path = anime_folder / new_path.name
    print(f'Moving: {new_path} to {final_path}')
    os.rename(new_path, final_path)
    with codecs.open(log_name, 'a+', 'utf-8') as f:
        print(f'Moving: {new_path} to {final_path}', file=f)
    return final_path

def update_animelist(anime_name):
    animelist_path = "/Volumes/media/anime/animelist.txt"
    anime_name = anime_name.split('/')[-1]  # 提取番剧名称
    if not os.path.exists(animelist_path):
        with open(animelist_path, 'w', encoding='utf-8') as f:
            f.write(f'{anime_name}\n')
    else:
        with open(animelist_path, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            if anime_name + '\n' not in lines:
                f.write(f'{anime_name}\n')

if __name__ == "__main__":
    args = parser.parse_args()
    if op.isdir(args.path):
        args.root = args.path
        args.path = ''

    unwanted_list = load_unwanted_list()

    anime_name, new_name, new_path = None, None, None
    if args.name != '' and args.root != '':
        temp = str(Path(args.root) / args.name)
        if op.isdir(temp):
            args.root = temp
            args.name = ''

    if args.path != '':
        root, name = op.split(args.path)
        anime_name, new_name, new_path = rename_and_move(root, name, unwanted_list)
    elif args.name != '' and args.root != '':
        anime_name, new_name, new_path = rename_and_move(args.root, args.name, unwanted_list)
    elif args.root != '':
        files = []
        for suffix in suffixs:
            files.extend(Path(args.root).rglob('*.' + suffix))
            files.extend(Path(args.root).rglob('*.' + suffix.upper()))
        print(f'Total Files Number: {len(files)}')
        for path in files:
            root, name = op.split(path)
            anime_name, new_name, new_path = rename_and_move(root, name, unwanted_list)
    else:
        print('Please input whether only root, or only path, or both root and name')
    
    if anime_name and new_name and new_path:
        print(f'{anime_name},{new_name},{new_path}')
