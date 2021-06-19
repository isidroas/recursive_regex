import re
import os
import yaml
import argparse
from typing import List



class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Parameters:
    def __init__(
        self,
        pattern,
        substitution,
        case_insensitive=False,
        exclude_dirs=[],
        exclude_files=[],
        ask_before=False,
    ):
        self.pattern: str = pattern
        self.substitution: str = substitution
        self.case_insensitive: bool = case_insensitive
        self.exclude_dirs: List[str] = exclude_dirs
        self.exclude_files: List[str] = exclude_files
        self.ask_before: bool = ask_before


SUB = "adios"
ASK_BEFORE = False
DRY_RUN = True
#TARGET = "./tests/"


def get_preceding(start: int, text_str: str):
    preceding = ""
    while start >= 0 and text_str[start] != "\n":
        preceding = text_str[start] + preceding
        start = start - 1
    return preceding


def get_successor(end: int, text_str: str):
    successor = ""
    while end < len(text_str) and text_str[end] != "\n":
        successor = successor + text_str[end]
        end = end + 1
    return successor


def getNumberOfLines(str_):
    return len(str_.split("\n"))


def sub_func(i):
    pre = get_preceding(i.start() - 1, i.string)
    suc = get_successor(i.end(), i.string)
    res = pre + bcolors.WARNING + i[0] + bcolors.ENDC + suc

    line = str(getNumberOfLines(i.string[: i.start()])) + ": "
    line_str = bcolors.FAIL + bcolors.BOLD + line + bcolors.ENDC

    print(line_str + res)
    print(" " * len(line + pre) + bcolors.OKBLUE + i.expand(SUB) + bcolors.ENDC)
    if ASK_BEFORE:
        skip = input("Do this substitution? [Y/n]") == "n"
        if skip:
            return i.group(0)

    return i.expand(SUB)


def process_file(path, pattern):
    print(
        "\n" + bcolors.UNDERLINE + bcolors.BOLD + bcolors.OKGREEN + path + bcolors.ENDC
    )
    with open(path, "rt") as file:
        file_str = file.read()
        res_sub, n_sub = re.subn(pattern, sub_func, file_str)

    if not n_sub:
        # delete last printed line (name of file)
        print("\033[F" + "\033[K")
    if not DRY_RUN and n_sub:
        with open(path, "wt") as file:
            file.write(res_sub)

def parse_arguments():
    parser = argparse.ArgumentParser(description = 'Recursive REGEX')
    parser.add_argument('target', help='path of the file or directory to search')
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_arguments()
    print(args.__dict__)
    with open('rere_parameters.yaml') as file:
        param_dict = yaml.load(file)

    params = Parameters(**param_dict)
    if params.case_insensitive:
        pattern = re.compile(params.pattern, flags=re.IGNORECASE)
    else:
        pattern = re.compile(params.pattern)

    if os.path.isdir(args.target):
        for root, subdirs, files in os.walk(args.target):
            if any([e in root for e in params.exclude_dirs]):
                continue
            for f in files:
                if any([e in f for e in params.exclude_files]):
                    continue
                path = os.path.join(root, f)
                process_file(path, pattern)
    else:
        process_file(args.target, pattern)
