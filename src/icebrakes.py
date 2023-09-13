#!/bin/python3
'''Run main.py with the path to a python file as the only argument. 
Support for dirs will be added in the future. 

Minimum supported python version is 3.8.x (subject to change'''
from os.path import isfile
import sys
from typing import Dict, List
from dataclasses import dataclass

# It's still really really really ugly to pass this everywhere
# But at least I'm not using any globals anymore
@dataclass
class States():
    '''I had to many global states vars so now this dataclass keeps them all tidy.'''
    all_mode: bool = False
    errors: bool = False

DictIntStr = Dict[int, str]


def icebrakes(filepath: str) -> None:
    '''takes a single argument filepath is a string that points to
    a file, then IceBrakes begins linting the file by collecting all 
    named assignments and any references to const variables (#$) '''
    states = States()

    if isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as filehandler:
            file: List[str] = filehandler.readlines()

        constants: DictIntStr = get_names_from_file(file, states=states, target='#$')

        if not constants and not states.errors:      # When errors is True then #$ must be somewhere
            print('No constants declared, use #$ at then end of a line with a declaration.')
            sys.exit(2)
        states.all_mode=True
        all_vars: DictIntStr = get_names_from_file(file, states=states)
        cross_reference(constants, all_vars, states=states)
    else:
        print(f'{filepath} is not a file. No linting possible.')


def get_names_from_file(file: List[str], states: States, target: str='') -> dict:
    '''This function checks every line of a file and grabs the names
    from those lines. If a target is declared this function checks
    the last chars of the file for the target.'''

    def get_name_from_line(line: str) -> str:
        '''This function takes a line of a file and runs all the name parse funcs
        over the line. Once a nonempty string is found a name is returned.'''

        line = line.lstrip()
        name: str = paren_parse(line)
        if name:
            return name
        return equal_sign_parse(line, states=states)


    names: DictIntStr = {}
    for index, line in enumerate(file):
        #This is neat because the default value of target always returns True on 'in' checks.
        if target in line.rstrip()[-len(target):]:
            name: str = get_name_from_line(line)
            if name:
                names[index +1] = name
            elif target:
                print(f'Immutable var declared on line number {index + 1}, but no names found.')
                states.errors=True
    return names


# These parse methods for the basis on the whole project and
# are subject to the most new code being written


def paren_parse(line: str) -> str:
    '''paren_parse searches a line for one of these openers ['async def', 'def', 'class'] 
    and if an opener is found then the string between the opener and "(" is returned.'''
    name: str = ''
    for opener in ['async def', 'def', 'class']:
        if opener in line:
            idx: int = line.index(opener)
            for char in line[idx + len(opener):]:
                if char == '(':
                    return name
                name += char
    return name


def equal_sign_parse(line: str, states: States) -> str:
    '''This method parses a string for any single equal sign.
    Once an equal sign is found it gets the first name before the 
    equal sign. See DOCS/icebrakes.txt for more info.'''
    name: str = ''
    idx:int = 0
    def name_assembler(name: str='', idx: int=0) -> str:
        for char in line[:idx]:
            if char in ' :':
                break
            name += char
        return name

    if states.all_mode:
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


def cross_reference(constants: DictIntStr, all_vars: DictIntStr, states: States) -> None:
    '''Once you have the constants and all_vars for a given python file you 
    can cross reference them to see if any constants are overwritten illegally 
    and inform the users.'''

    for c_key, c_val in constants.items():
        for v_key, v_val in all_vars.items():
            if c_val == v_val and v_key != c_key:
                mes=f'Bad use {c_val} was made static on line {c_key}, and mutated on line {v_key}'
                print(mes)
                states.errors = True

    if not states.errors:
        print('Congrats you passed the IceBrakes lint with a perfect 300/300 score!')

    # This could be a return statement if we won't want to sys.exit on every call
    sys.exit(int(states.errors))     # I was gonna use two bools but this is damn clever.


if __name__ == '__main__':
    if len(sys.argv) == 2:
        icebrakes(sys.argv[1])
    else:
        print('This project takes exactly 1 command line arg, a python file path.')


# Copyright © 2023 Lars S.
