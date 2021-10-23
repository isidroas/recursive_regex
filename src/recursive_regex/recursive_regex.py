import re
import os
import yaml
import argparse
from typing import List


# def custom_postfilter(match_obj: re.Match) -> bool:
#    unchanged_string = match_obj.group(0)
#
#    return True

# TODO: remove it? this is only useful
# when you want aditionaly, a regex_substitution
# CUSTOM_POSTFILTER = custom_postfilter
# CUSTOM_POSTFILTER = None

# name it ADITIONAL_FILTER ?

# Sometimes is useful to not convert when it fails.
# but in thas case, the 'original_capture' attribute could be used


# CUSTOM_CONVERSION = custom_conversion
CUSTOM_CONVERSION = None
# name it ADVANCED_SUBSTITUTION?


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


class Match:
    def __init__(self, match: re.Match):

        self.init_pos: int = match.start()
        self.end_pos: int = match.end()

        # The full file
        self.string: str = match.string

        # The regex groups
        # self.groups: List[str]

        # Unaltered caputured string
        self.original_capture: str = match.group(0)

        self._match = match

    def regex_substitute(self, substitution: str) -> str:
        return self._match.expand(substitution)

    def print_context_and_substitution(self, substitution_processed):
        pre = self._get_preceding(self.init_pos - 1, self.string)
        suc = self._get_successor(self.end_pos, self.string)
        res = (
            pre + bcolors.WARNING + self.original_capture + bcolors.ENDC + suc
        )

        line = str(self._getNumberOfLines(self.string[: self.init_pos])) + ": "
        line_str = bcolors.FAIL + bcolors.BOLD + line + bcolors.ENDC

        print(line_str + res)
        print(
            " " * len(line + pre)
            + bcolors.OKBLUE
            + substitution_processed
            + bcolors.ENDC
        )

    @staticmethod
    def _get_preceding(start: int, text_str: str):
        """
        Given a position on a string, it returns all of the characters between
        that position and the previous line break.

        >>> _get_preceding(10, 'hola\\nadios que pasa\\n otra linea')
        'adios '
        """

        preceding = ""
        while start >= 0 and text_str[start] != "\n":
            preceding = text_str[start] + preceding
            start = start - 1
        return preceding

    @staticmethod
    def _get_successor(end: int, text_str: str):
        """
        Given a position on a string, it returns all of the characters between
        that position and the next line break.

        >>> _get_successor(10, 'hola\\nadios que pasa\\n otra linea')
        'ue pasa'
        """
        successor = ""
        while end < len(text_str) and text_str[end] != "\n":
            successor = successor + text_str[end]
            end = end + 1
        return successor

    @staticmethod
    def _getNumberOfLines(str_):
        return len(str_.split("\n"))


def sub_func(i: Match, substitution, ask_before, custom_conversion):

    # if CUSTOM_POSTFILTER:
    #    if not CUSTOM_POSTFILTER(i):
    #        return i.original_capture

    if custom_conversion:
        substitution_processed = custom_conversion(i)
    else:
        substitution_processed = i.regex_substitute(substitution)

    i.print_context_and_substitution(substitution_processed)

    if ask_before:
        skip = input("Do this substitution? [Y/n]") == "n"
        if skip:
            return i.original_capture

    return substitution_processed


def process_file(path, pattern, dry_run, sub_func1):
    print(
        "\n"
        + bcolors.UNDERLINE
        + bcolors.BOLD
        + bcolors.OKGREEN
        + path
        + bcolors.ENDC
    )
    with open(path, "rt") as file:
        file_str = file.read()
        res_sub, n_sub = re.subn(pattern, sub_func1, file_str)

    if not n_sub:
        # delete last printed line (name of file)
        print("\033[F" + "\033[K")
    if not dry_run and n_sub:
        with open(path, "wt") as file:
            file.write(res_sub)


def get_arguments():
    parser = argparse.ArgumentParser(description="Recursive REGEX")
    parser.add_argument(
        "target", help="path of the file or directory to search"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--config-file", "-c", help="yaml file where config is stored"
    )
    args = parser.parse_args()
    return args.target, args.dry_run, args.config_file


def main(target, dry_run, config_file, custom_conversion=None):
    if config_file:
        with open(config_file) as file:
            param_dict = yaml.safe_load(file)

    params = Parameters(**param_dict)
    if params.case_insensitive:
        pattern = re.compile(params.pattern, flags=re.IGNORECASE)
    else:
        pattern = re.compile(params.pattern)

    def sub_func_wrap(i):
        return sub_func(
            Match(i), params.substitution, params.ask_before, custom_conversion
        )

    if os.path.isdir(target):
        for root, subdirs, files in os.walk(target):
            if any([e in root for e in params.exclude_dirs]):
                continue
            for f in files:
                if any([e in f for e in params.exclude_files]):
                    continue
                process_file(
                    os.path.join(root, f), pattern, dry_run, sub_func_wrap
                )
    else:
        process_file(target, pattern, dry_run, sub_func_wrap)


def run():
    """
    Run from command line
    """
    main(*get_arguments())


if __name__ == "__main__":
    run()
