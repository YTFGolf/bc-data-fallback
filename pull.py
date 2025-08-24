import re
import sys
import os
from typing import TypedDict, NewType
import shutil

def are_files_different(file_1, file_2):
    if os.stat(file_1).st_size != os.stat(file_2).st_size:
        return True

    return False
    # # makes this much faster

    # cur_cont = open(cur_file, encoding="utf-8").read()
    # prev_cont = open(prev_file, encoding="utf-8").read()
    # return cur_cont != prev_cont

class Folder(TypedDict):
    path: str
    patterns: list[str]

# Usage:
# python pull.py "~/Downloads/Version 14.5.0 JP"
def newfiles(args):
    pull_from = os.path.expanduser(args[1])

    folders: list[Folder] = [
        {
            'path': 'ImageDataLocal',
            'patterns': [
                r'\d{3}.*'
            ]
        },
        {
            'path': 'DataLocal',
            'patterns': [
                # r'unitbuy.csv',
                r'stage.*\d\d\.csv'
            ]
        }
    ]

    Desc = NewType('Desc', tuple[str, str])
    new: Desc = []
    changed: Desc = []
    for folder in folders:
        def folder_matches(name: str) -> bool:
            for pattern in folder['patterns']:
                if re.match(pattern, name):
                    return True
            return False

        here = f"./{folder['path']}"
        here_files = [file for file in os.listdir(here) if folder_matches(file)]

        there = f"{pull_from}/{folder['path']}"
        there_files = [file for file in os.listdir(there) if folder_matches(file)]

        here_files = set(here_files)
        for file in there_files:
            dst_file = os.path.join(here, file)
            src_file = os.path.join(there, file)
            if not os.path.exists(dst_file):
                new.append((src_file, dst_file))
            else:
                if are_files_different(src_file, dst_file):
                    changed.append((src_file, dst_file))

    def copyfile(files: Desc):
        src = files[0]
        dst = files[1]
        shutil.copyfile(src, dst)

    for files in new: copyfile(files)
    # for files in changed: copyfile(files)

newfiles(sys.argv)
