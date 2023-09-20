#!/bin/python3
'''v0.1.3
Run main.py with the path to a python file as the only argument. 
Support for dirs will be added in the future. 

Minimum supported python version is 3.8.x (subject to change'''

import string
import sys

from dataclasses import dataclass
from functools import reduce
from math import gcd
from os.path import isfile
from typing import Dict, List, Tuple, Set

DictStrSet = Dict[str, set]


@dataclass
class States():
    '''This is a bit of a catchall class it handles global state bools, as well
    as namespace scoping tools.'''
    errors: bool = False
    indent: int = 0
    old_indent: int = -999

    def __post_init__(self) -> None:
        '''Dataclasses can't have lists as properties so this post_init is required.'''
        self.names_in_scope: List[Tuple] = [('root', 0)]

    def update_indent(self, indent: int) -> None:
        '''This method updates the indent level and when the indent level
        goes down it leaves the current scope.'''
        self.old_indent = self.indent
        self.indent = indent

        if self.indent < self.names_in_scope[-1][1]:
            # This takes us up one level of scope
            self.names_in_scope.pop()


def icebrakes(filepath: str) -> None:
    '''This function takes a python file and lints it.'''

    states = States()

    # These file checks/messages will be removed from this function soon.
    if isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as filehandler:
            file: List[str] = filehandler.readlines()

        constants, all_vars = get_names_from_file(file, states=states)

        # I tried to to remove that states.errors check and broke everything.
        if not constants and not states.errors:
            print('No constants declared, use #$ at then end of a line with a declaration.')
            sys.exit(2)

        cross_reference(constants, all_vars, states=states)
    else:
        print(f'{filepath.rsplit("/")[-1]} is not a file. No linting possible.')


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
        if name:                         # This is a tuple
            states.names_in_scope.append((name, indent +1))
            return name

        return equal_sign_parse(line)

    base_indent: int = white_space_parse(file)

    all_vars: DictStrSet = {}
    constants: DictStrSet = {}

    for index, line in enumerate(file):
        line_lstrip: str = line.lstrip()
        len_line_lstrip: int = len(line_lstrip)

        #BUG FIX 2000
        if len_line_lstrip == 0 or line_lstrip[0] == '#':
            continue

        spaces: int = len(line) - len_line_lstrip
        indent: int = spaces // base_indent
        states.update_indent(indent)

        const_declared: bool = False

        if '#$' in line.rstrip()[-2:]:
            const_declared = True

        name: str = get_name_from_line(line, indent)

        if name:
            name = name_gen(name, states)
            all_vars.setdefault(name, set()).add(index + 1)
            if const_declared:
                constants.setdefault(name, set()).add(index + 1)

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
    name: str = ''
    idx:int = 0
    def name_assembler(name: str='', idx: int=0) -> str:
        for char in line[:idx]:
            name_chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_')
            if char not in name_chars:
                break
            name += char
        return name


    # FOUND A BUG WHEN LINTING THIS FILE, THESE EQUAL SIGNS ARE NOT
    # BEING IGNORED EVEN THOUGH THEY ARE STRINGS. STRING AWARENESS NEEDED.
    for symbol in ['-=', '+=', '*=', '%=', ':=', '/=', '//=']:
        if symbol in line:
            idx = line.index(symbol)
            break

    if not idx:
        if '=' in line:
            idx = line.index('=')
            if len(line) == idx or line[idx + 1] == '=':
                return name

    name = name_assembler(idx=idx)
    return name


def cross_reference(constants: DictStrSet, all_vars: DictStrSet, states: States) -> None:
    '''Once you have the constants and all_vars for a given python file you 
    can cross reference them to see if any constants are overwritten illegally 
    and inform the users.'''

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

    # This will be a return statement for dirs
    sys.exit(int(states.errors))


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
        # int here is also for mypy
        return int(reduce(gcd, levels))

    # This is just for mypy/pylint
    return 1


if __name__ == '__main__':
    if len(sys.argv) == 2:
        icebrakes(sys.argv[1])
    else:
        print('This project takes exactly 1 command line arg, a python file path.')
