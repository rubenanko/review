import argparse
import os
import sys
from difflib import SequenceMatcher
from typing import List

from rv.core.Files import File
from rv.core.tui.colors import blue, green, yellow
from rv.core.tui.components import LOG, LOG_WARNING


def entrypoint(argv: List[str]) -> None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='rv functions',
                        description='rv list allows you to list all functions in a file',
                        epilog="See 'rv --help' to get further help")

    # add arguments
    parser.add_argument(
        "file_alias", help="", type=str
    )
    parser.add_argument(
        "filter_pattern", 
        nargs='?',
        help="Filter functions by fuzzy name matching (optional)", 
        type=str, 
        default=None
    )

    # parse argv
    args = parser.parse_args(argv)

    file = File(args.file_alias)

    functions = file.get_functions()
    functions_names = [name for name,_ in functions]
    functions_lines_index = [index for _,index in functions]

    # Apply fuzzy filter if provided
    if args.filter_pattern:
        filtered_indices = []
        for i, name in enumerate(functions_names):
            similarity = SequenceMatcher(None, args.filter_pattern.lower(), name.lower()).ratio()
            if similarity > 0.3:  # Threshold for fuzzy matching
                filtered_indices.append(i)
        functions_names = [functions_names[i] for i in filtered_indices]
        functions_lines_index = [functions_lines_index[i] for i in filtered_indices]

    buffer = ""
    # format output -> ls style

    for index in functions_lines_index:
        print(file.highlighted_lines[index])
    
    # if len(functions_names):
    #     terminal_width, _ = os.get_terminal_size()
    #     max_len = max([len(function_name) for function_name in functions_names])
    #     formatted_functions_names = [
    #         (function_name + " " + " " * (3 + max_len - len(function_name)))
    #         for function_name in functions_names
    #     ]

    #     number_of_records_per_line = terminal_width // (max_len+4)
    #     number_of_lines = 1 + len(formatted_functions_names)//number_of_records_per_line
    #     for i in range(1,number_of_lines):
    #         formatted_functions_names[i*number_of_records_per_line-1]+= "\n"
    #     buffer = "".join(formatted_functions_names)

    # print(buffer + "\n")
    print(f"\nDisplaying {len(functions_names)} functions")
