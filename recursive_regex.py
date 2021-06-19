import re
import os


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


PATTERN = r"Total Active Export"
SUB = "Active Energy Export (-A)"
ASK_BEFORE = False
DRY_RUN = False
EXCLUDE = [".git", ".swp", "__pycache__", ".bin", "zigbee_certification"]
TARGET = "/home/isidro-trabajo/WSLW/robot_tests"


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


def sub_func(i):
    pre = get_preceding(i.start() - 1, i.string)
    suc = get_successor(i.end(), i.string)
    res = pre + bcolors.WARNING + i[0] + bcolors.ENDC + suc
    print(res)
    print(" " * len(pre) + bcolors.OKBLUE + i.expand(SUB) + bcolors.ENDC)
    if ASK_BEFORE:
        skip = input("Do this substitution? [Y/n]") == "n"
        if skip:
            return i.group(0)

    return i.expand(SUB)


def process_file(path, pattern):
    with open(path, "rt") as file:
        file_str = file.read()
        res_sub = re.sub(PATTERN, sub_func, file_str, flags=re.IGNORECASE)
        # print(res_sub)
    if not DRY_RUN:
        with open(path, "wt") as file:
            file.write(res_sub)


if __name__ == "__main__":
    pattern = re.compile(PATTERN)
    if os.path.isdir(TARGET):
        for root, subdirs, files in os.walk(TARGET):
            if any([e in root for e in EXCLUDE]):
                continue
            for file in files:
                if any([e in file for e in EXCLUDE]):
                    continue
                path = os.path.join(root, file)
                # print(path)
                process_file(path, pattern)
    else:
        process_file(path, pattern)
