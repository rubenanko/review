import argparse
import os
import sys
from typing import List
from pathlib import Path

from rv.core.tui.colors import blue, green, yellow
from rv.core.tui.components import LOG, LOG_WARNING
from rv.core.Files import File


def entrypoint(argv: List[str]) -> None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='rv show',
                        description='shows the content of a file',
                        epilog="See 'rv --help' to get further help")

    # add arguments
    parser.add_argument(
        "file_alias", help="", type=str
    )

    parser.add_argument(
        "fuzzy_expression", help="", nargs="*", type=str
    )

    # parse argv
    args = parser.parse_args(argv)

    # fetch repositories data

    if len(args.fuzzy_expression):
        fuzzy_expression = " ".join(args.fuzzy_expression)
    else:
        fuzzy_expression = None

    file = File(args.file_alias)

    # print(file.highlighted_buffer)
    if fuzzy_expression:
        fragment = file.find_fragment(fuzzy_expression.lower())
        if fragment != None:
            print(fragment.highlighted_buffer)
    else:
        print(file.highlighted_buffer)
    print(f"\n{file.filename}")