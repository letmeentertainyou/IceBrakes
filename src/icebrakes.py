#!/bin/python3
'''Run main.py with the path to a python file as the only argument. 
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
    names_in_scope = [('root', 0)]


    def update_indent(self, indent: int) -> None:
        '''This method updates the indent level and when the indent level
        goes to the left we attempt to leave the current scope.'''
        self.old_indent = self.indent
        self.indent = indent
        if self.indent < self.old_indent:
            self.leave_scope()


    def leave_scope(self) -> None:
        '''This method pops the last name from names_in_scope when then
        indent level is less than it was when that name was added to the scope.'''
        if self.indent < self.names_in_scope[-1][1]:
            self.names_in_scope.pop()


def icebrakes(filepath: str) -> None:
    '''takes a single argument filepath is a string that points to
    a file, then IceBrakes begins linting the file by collecting all 
    named assignments and any references to const variables (#$) '''

    states = States()

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
    '''This function checks every line of a file and grabs names from those lines.'''

    def get_name_from_line(line: str, indent: int) -> str:
        '''This function takes a line of a file and runs all the name parse funcs
        over the line. Once a nonempty string is found a name is returned.'''

        line = line.lstrip()
        name: str = paren_parse(line)
        if name:                         # This is a tuple
            states.names_in_scope.append((name, indent +1))   ### NEW
            return name


        return equal_sign_parse(line)

    base_indent: int = white_space_parse(file)         ### NEW

    # Find room for an if states.indent path, and then get ready for all the dict stuff.
    all_vars: DictStrSet = {}
    constants: DictStrSet = {}

    for index, line in enumerate(file):
        if line == '\n':                                  ### NEW
            continue                                      ### NEW

        spaces: int = len(line) - len(line.lstrip())      ### NEW
        indent: int = spaces // base_indent               ### NEW
        states.update_indent(indent)                      ### NEW

        const_declared: bool = False

        if '#$' in line.rstrip()[-2:]:
            const_declared = True

        name: str = get_name_from_line(line, indent)

        if name:
            name = name_gen(name, states)                     ### NEW
            all_vars.setdefault(name, set()).add(index + 1)
            if const_declared:
                constants.setdefault(name, set()).add(index + 1)

        elif const_declared:
            print(f'Immutable var declared on line number {index + 1}, but no names found.')
            states.errors=True

    return constants, all_vars


def name_gen(name: str, states: States) -> str:
    '''Create unique keys for the name dicts using names_in_scope to create a path.'''
    temp: List = [name[0] for name in states.names_in_scope] + [name]
    return '.'.join(temp)


def name_split(name: str) -> str:
    '''Returns only the name from a scope string for communicating with users.'''
    return name.rsplit('.')[-1]


def paren_parse(line: str) -> str:
    '''paren_parse searches a line for one of these openers ['async def', 'def', 'class'] 
    and if an opener is found then the string between the opener and "(" is returned.'''
    name: str = ''
    for opener in ['async def ', 'def ', 'class ']:
        if opener in line[0:len(opener)]:
            idx: int = line.index(opener)
            for char in line[idx + len(opener):]:        ### FIXED A BUG HERE
                if char == '(':
                    return name
                name += char
    return name


def equal_sign_parse(line: str) -> str:
    '''This method parses a string for any single equal sign.
    Once an equal sign is found it gets the first name before the 
    equal sign. See DOCS/icebrakes.txt for more info.'''
    name: str = ''
    idx:int = 0
    def name_assembler(name: str='', idx: int=0) -> str:
        for char in line[:idx]:

            # Massive BUG fix here.                   ### NEW
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

            set_of_line_numbers = all_vars.get(key)

            if set_of_line_numbers is not None:
                for num in set_of_line_numbers:
                    if num == val:
                        continue

                    name = name_split(key)              ### NEW
                    mes=f'Bad use {name} was made static on line {val}, and mutated on line {num}'
                    print(mes)
                    states.errors = True

    if not states.errors:
        print('Congrats you passed the IceBrakes lint with a perfect 300/300 score!')

    # This could be a return statement if we won't want to sys.exit on every call
    sys.exit(int(states.errors))


def white_space_parse(file: List[str]) -> int:
    '''Takes a file, calculates the indentation level using magic.
    For now we parse the first 100 lines of the file as that should be more than enough,
    but that number can probably be reduced a bit. It doesn't start counting until white
    space is found which ignores imports/doc strings in the line count.

    Also we are considering tabs as whitespace but there will be more work to process them
    later (aka you are a monster if your file has tabs in it), and also it's gonna be a mess 
    if you mix whitespace/tabs. So IceBrakes is going to assume some level of responsibility 
    belongs with the dev.
    
    I was kind of surprised I couldn't find a package or tool to do this since python is all about
    indentation levels but it turned out to be a really easy solve. 
    '''

    levels: Set = set()
    num: int = 0
    for line in file:
        if num == 100:
            break
        if line[0] in "\t ":
            len_line_lstrip = len(line.lstrip())

            # This removes any lines that only have whitespace on them
            # Of course so should your other linter but you know.
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
