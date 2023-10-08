import re
import argparse
from typing import List
import sys


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


# TODO: inherit to
#  - avoid boilerplate redirect
#  - avoid inventing
# problem: the re.sub only passes re.Match
class Match:
    def __init__(self, match: re.Match):
        self.init_pos: int = match.start()
        self.end_pos: int = match.end()

        # The full file
        self.string: str = match.string

        # The regex groups
        self.groups: List[str] = match.groups()

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

        line = str(self._number_of_lines(self.string[: self.init_pos])) + ": "
        line_str = bcolors.FAIL + bcolors.BOLD + line + bcolors.ENDC

        print(line_str + res)
        print(
            " " * len(line + pre)
            + bcolors.OKBLUE
            + substitution_processed
            + bcolors.ENDC
            + "\n",
            end="",
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
    def _number_of_lines(str_):
        return len(str_.split("\n"))


class Substitutor:
    def __init__(
        self,
        pattern,
        substitution: str,
        ask_before: bool = False,
        case_insensitive=False,
        dry_run=False,
    ):
        self.substitution = substitution
        self.ask_before = ask_before
        self.dry_run = dry_run
        if case_insensitive:
            self.pattern = re.compile(pattern, flags=re.IGNORECASE)
        else:
            self.pattern = re.compile(pattern)
        self._first_sub = True
        self._path = None

    def process_file(self, path):
        self._first_sub = True
        self._path = path
        with open(path, "rt") as file:
            contents_sub, n_sub = re.subn(self.pattern, self._sub, file.read())

        if n_sub:
            # this produces a blank line, even in the last file
            print("\n", end="")

        if not self.dry_run and n_sub:
            with open(path, "wt") as file:
                file.write(contents_sub)

    def _sub(self, match):
        match = Match(match)

        substitution_processed = match.regex_substitute(self.substitution)

        if self._first_sub:
            print(
                bcolors.UNDERLINE
                + bcolors.BOLD
                + bcolors.OKGREEN
                + self._path
                + bcolors.ENDC
                + "\n",
                end="",
            )
            self._first_sub = False

        # TODO: handle when substitution is equal.
        #       For example, by skipping the print.
        #       or by priting "(equal)"
        match.print_context_and_substitution(substitution_processed)

        if self.ask_before:
            skip = input("Do this substitution? [Y/n]") == "n"
            if skip:
                return match.original_capture

        return substitution_processed


def get_arguments():
    parser = argparse.ArgumentParser(description="Recursive REGEX")
    parser.add_argument("pattern")
    parser.add_argument("substitution")
    parser.add_argument(
        "target", help="path of the file or directory to search", nargs="*"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--case-insensitive", "-i", action="store_true")
    args = parser.parse_args()
    return vars(args)


def main(pattern, substitution, target, **kwargs):
    if not target:
        target = (p.rstrip() for p in sys.stdin.readlines())

    substitutor = Substitutor(pattern, substitution, **kwargs)
    for path in target:
        substitutor.process_file(path)


def run():
    """
    Run from command line
    """
    main(**get_arguments())


if __name__ == "__main__":
    run()
