#!/bin/python3
'''v0.2.0
Run main.py with the path to a python file as the only argument. 
Support for dirs will be added in the future. 

Minimum supported python version is 3.8.x (subject to change'''

import string
import sys

from dataclasses import dataclass
from functools import reduce
from math import gcd
from os import walk
from os.path import isdir, isfile
from typing import Dict, List, Tuple, Set

DictStrSet = Dict[str, set]


@dataclass
class States():
    '''This is a bit of a catchall class it handles global state bools, as well
    as namespace scoping tools.'''

    errors: bool = False
    indent: int = 0
    old_indent: int = -1
    multiline_status: int = 0         ### NEW

    def __post_init__(self) -> None:
        '''Dataclasses can't have lists as properties so this post_init is required.'''
        self.names_in_scope: List[Tuple] = [('root', 0)]
        self.loops_in_scope: List[Tuple] = [('root', 0)]


    def update_indent(self, indent: int) -> None:
        '''This method updates the indent level and when the indent level
        goes down it leaves the current scope.'''

        self.old_indent = self.indent
        self.indent = indent

        # These checks take the scope up one layer at the correct time.
        if self.indent < self.names_in_scope[-1][1]:
            self.names_in_scope.pop()

        if self.indent < self.loops_in_scope[-1][1]:
            self.loops_in_scope.pop()


def dir_or_file(path: str) -> None:
    '''Takes an input string and if it's a dir recursively lints it,
    and if it's a file lints it, and otherwise prints an error message.'''

    if isdir(path):
        exit_codes: List[int] = []

        for fullpath, subdirs, files in walk(path):         # pylint: disable=unused-variable
            for file in files:

                if file.endswith(".py") is True:
                    # This print makes the dir mode output easier to read
                    print(f'Linting results for {file}:')
                    code = icebrakes(f"{fullpath}/{file}", dir_mode=True)
                    exit_codes.append(code)
        print(exit_codes)

    elif isfile(path):
        icebrakes(path)

    else:
        print(f'{path.split("/")[-1]} is not a file or directory. No linting possible.')


def icebrakes(filepath: str, dir_mode: bool= False) -> int:
    '''This function takes a python file and lints it.'''

    states = States()

    with open(filepath, 'r', encoding='utf-8') as filehandler:
        file: List[str] = filehandler.readlines()

    constants, all_vars = get_names_from_file(file, states=states)

    if not constants and not states.errors:
        print('No constants declared, use #$ at then end of a line with a declaration.')
        states.errors = True

    exit_code: int = cross_reference(constants, all_vars, states=states)

    if not dir_mode:
        sys.exit(exit_code)
    return exit_code


def get_names_from_file(file: List[str], states: States) -> Tuple[dict, dict]:
    '''This function parses a python file for any names declared and builds two dictionaries.
    One dict is for all_vars in the file and one dict is only for constants. Constants are 
    defined as vars declared on a line ending in #$.'''

    def get_name_from_line(line: str, indent: int) -> str:
        '''This function takes a line of a file and runs all the name parse funcs
        over the line. Once a nonempty string is found a name is returned. When paren_parse() 
        returns a nonempty string get_names_from_line() updates the scope.'''

        line = line.lstrip()
        name: str = paren_parse(line)

        if name:
            states.names_in_scope.append((name, indent +1))
            return name

        return equal_sign_parse(line)

    base_indent: int = white_space_parse(file)

    all_vars: DictStrSet = {}
    constants: DictStrSet = {}

    for index, line in enumerate(file):
        line_lstrip: str = line.lstrip()
        len_line_lstrip: int = len(line_lstrip)

        # This check can still go at the top because it doesn't change the logic.
        if len_line_lstrip == 0:                 ### CHANGED
            continue

        multiline_comment_parse(line, states)    ### NEW

        # These two if statements can be combined but I think it will be confusing
        if states.multiline_status != 0:         ### NEW
            continue                             ### NEW

        if line_lstrip[0] == '#':                ### MOVED
            continue

        loop_parse(line, states)

        const_declared: bool = False
        spaces: int = len(line) - len_line_lstrip
        indent: int = spaces // base_indent
        states.update_indent(indent)

        if line.rstrip().endswith('#$'):
            const_declared = True

        name: str = get_name_from_line(line, indent)
        if name:
            name = name_gen(name, states)
            all_vars.setdefault(name, set()).add(index + 1)

            if const_declared:
                if len(states.loops_in_scope) == 1:
                    constants.setdefault(name, set()).add(index + 1)

                else:
                    loop_name = states.loops_in_scope[-1][0]
                    print(f'Bad usage was ignored inside {loop_name}loop on line {index +1}.')

        elif const_declared:
            print(f'Immutable var declared on line number {index + 1}, but no names found.')
            states.errors=True

    return constants, all_vars


def name_gen(name: str, states: States) -> str:
    '''Create unique keys for the all_vars/constants dicts using names_in_scope to create a key.'''
    temp: List = [name[0] for name in states.names_in_scope] + [name]
    return '.'.join(temp)


def name_split(name: str) -> str:
    '''Gets all chars to the right of the last period in a string.'''
    return name.rsplit('.')[-1]


def loop_parse(line: str, states: States) -> None:
    '''Finds a loop in a given line and updates states. This function
    will need string awareness when that is implemented.'''
    for opener in ['for ', 'while ']:
        if opener in line[0:len(opener)]:
            states.loops_in_scope.append((opener, states.indent))


def paren_parse(line: str) -> str:
    '''Searches a line for one of these openers ['async def', 'def', 'class'] 
    and if an opener is found then the string between the opener and "(" is returned.'''
    name: str = ''
    for opener in ['async def ', 'def ', 'class ']:
        if opener in line[0:len(opener)]:
            idx: int = line.index(opener)
            for char in line[idx + len(opener):]:
                if char == '(':
                    return name
                name += char
    return name


def equal_sign_parse(line: str) -> str:
    '''This method parses a string for any single equal sign
    and gets the first name before the equal sign.'''

    def name_assembler(line_to_idx: str='') -> str:
        '''Parses all chars that can be in a name and stops when an invalid char is found.'''
        name: str = ''
        for symbol in "(\"'":
            if symbol in line_to_idx:
                return name

        for char in line_to_idx:
            name_chars=list(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_')
            if char not in name_chars:
                break
            name += char
        return name

    name: str = ''
    idx: int = 0

    for symbol in ['-=', '+=', '*=', '%=', ':=', '/=', '//=']:
        if symbol in line:
            idx = line.index(symbol)
            break

    if not idx:
        if '=' in line:
            idx = line.index('=')
            if len(line) == idx or line[idx + 1] == '=':
                return name

    name = name_assembler(line_to_idx=line[:idx])
    return name


def white_space_parse(file: List[str]) -> int:
    '''Takes a file and calculates how many spaces that file uses to indent by parsing
    the first 100 indented lines of the file.'''

    levels: Set = set()
    num: int = 0

    for line in file:
        if num == 100:
            break

        if line[0] in "\t ":
            len_line_lstrip = len(line.lstrip())

            # This removes any lines that only have whitespace on them
            if len_line_lstrip > 0:
                num += 1
                size = len(line) - len_line_lstrip
                levels.add(size)

    if levels:
        return int(reduce(gcd, levels)) # int() here is for mypy.

    return 1    # This explicit return is just for mypy/pylint


def multiline_comment_parse(line: str, states: States) -> int:  ### NEW
    '''See IceBrakes API.txt for more detailed explanation, this function tracks
    whether a multiline comment is opened or closed on any given line.'''

    def find_first_index(tag: str, line: str) -> Tuple:
        '''Grabs the index of the first occurrence of a given string.'''
        try:
            return line.index(tag), tag
        except ValueError:
            return None, None

    single: str = "'''"
    double: str = '"""'
    tags: List[str] = []

    if single in line and states.multiline_status >=0:
        tags.append(single)

    if double in line and states.multiline_status <=0:
        tags.append(double)

    if tags:
        all_tags: List[Tuple] = [find_first_index(tag, line) for tag in tags]
        smallest = min(all_tags)

        if smallest[1] == single:
            states.multiline_status = 1 if states.multiline_status == 0 else 0

        if smallest[1] == double:
            states.multiline_status = -1 if states.multiline_status == 0 else 0

        idx = smallest[0]
        multiline_comment_parse(line=line[idx+3:], states=states)

    return states.multiline_status


def cross_reference(constants: DictStrSet, all_vars: DictStrSet, states: States) -> int:
    '''Once you have the constants and all_vars for a given python file you 
    can cross reference them to see if any constants are overwritten illegally 
    and inform the users. The exit status is returned as an int.'''

    for key, values in constants.items():
        for val in values:

            set_of_line_numbers: Set = all_vars.get(key, set())
            if set_of_line_numbers is not None:

                for num in set_of_line_numbers:
                    if num == val:
                        continue

                    name = name_split(key)
                    mes=f'Bad use {name} was made static on line {val}, and mutated on line {num}'
                    print(mes)
                    states.errors = True

    if not states.errors:
        print('Congrats you passed the IceBrakes lint with a perfect 300/300 score!')

    return int(states.errors)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        dir_or_file(sys.argv[1])

    else:
        print('This project takes exactly 1 command line arg, a python file path.')


#Copyright © 2023 Lars S.
