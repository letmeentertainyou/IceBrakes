#!/bin/python3
'''Eventually the functions of this file may get pulled into icebrakes.py, but first I want to
build my algorithms without breaking any of the unit tests.

My original thought process was naive and I assumed I needed to track every white space
change but since I only care about namespaces it's actually a much simpler problem, and
the main engines are already written.

Below I lay out how I will use white_space_parse() from this file along with get_names_from_file()
and paren_parse() from icebrakes.py to solve for namespaces.

Here's the deal with scopes, only the keywords 'def', 'class', 'async def' can
trigger a change in namespace. We don't need to track any other keywords. Words like
'for' and 'if' won't effect this is any way. My original line of thinking considered ternary 
if statements as an edge case but they are not even on my radar anymore.

So what do we really need? A different set of name dicts (constants/all_vars) for each sub 
namespace which will be determined by one of the above keywords and a corresponding white 
space change. We track when the white space goes back to it's original level, and that kills 
the sub namespace.

The good news is we don't need to parse lines more than once, but we need to juggle a lot
more dictionaries. So I need to figure out an api or tool or recursion that allows us to
sub name space for a while and then return out. 

We also either need to parse each set of sub dicts as we are leaving the scope or we need a
dict of all total dicts where the keys are related to the scope that we parse once after reading 
the file. The keys can't be indentation level because two different functions can have the same 
indent level and not be in each other's scopes.

So the name of each function can kind of work as a key but they would need to be sub keyed to their
outer scope, and then everything at the top would be named 'root'.

Here is a python code example.

def foo():
    def bar():
        pass

def bar():
    def foo():
        pass
        
We want to parse than into an object that looks like this.

root.foo
root.foo.bar
root.bar
root.bar.foo

I imagine that is a solved problem in python but it's one I will have to research.

It might be worth implementing some OO for the name dicts. Some struct that contains two
dicts. It will make passing things around a bit easier.

Because I already have paren_parse, I can actually use it to set a flag whenever a new
scope is found, then we unset the flag later by tracking white space. This would basically
mean checking for the sub scope flag (or int?) every pass and then carefully tracking white
space when it is set. This will have a huge time deficit but I always knew that.

The reason I think we need an int instead of a bool for a flag is to track how many sub scopes
deep we are. So 0 means root and 1 means one function def in, etc. Then every time we leave a scope,
we subtract one, and once the number is 0 we're not in a scope anymore. This will work with a nice
'if flag:' check because 0 is already falsey.

In get_names_from_file() is where I should track white space and check flags. I need to count 
the whitespace before stripping it, and move left/right accordingly. 

Things are structured and functional enough now that I think I can achieve this change with
only one or two additional functions. My next step will be to write out what those functions
might look like, and then I will try building that engine. When this step is complete most of 
the rest of the unit tests can be turned on because a large amount of them relate to white space.

I will also need a new major feature to work towards (loops) but I'm sure something will come up.

***************

Upon further thinking I have realized that by creating unique keys I won't actually need the
nested dict design pattern. Instead I will make a Naming() class that takes a name, and a
States() object and builds unique name keys. Then anytime two keys match exactly we have
a scope problem at the earliest place in the keys that match. I'm going to build the changes
to both classes, and then build a name parsing engine and then I barely have to change any
of the rest of the code.
'''

import sys

from dataclasses import dataclass
from functools import reduce
from math import gcd
from os.path import isfile
from typing import Dict, List, Tuple, Set


def white_space_parse(file: str) -> int:
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
    with open(file, encoding="UTF-8") as tempfile:
        num: int = 0
        for line in tempfile:
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
        # tnt here is also for mypy
        return int(reduce(gcd, levels))

    # This is just for mypy/pylint
    return 1
    #out = white_space_parse('icebrakes.py')
    #print(out)



# I added in the API for states.indent now I need to build the multilayer dict
# And then rework parsing for a multilayer dict. This could get really ugly with
# The indentation levels.
@dataclass
class States():
    '''I had to many global states vars so now this dataclass keeps them all tidy.'''
    errors: bool = False
    indent: int = 0

DictStrSet = Dict[str, set]


def icebrakes(filepath: str) -> None:
    '''takes a single argument filepath is a string that points to
    a file, then IceBrakes begins linting the file by collecting all 
    named assignments and any references to const variables (#$) '''

    # I tried to get rid of states now that it's a single value but it
    # Either needs to be an object, a global or returned from every function
    # In order for the state to change. So the dataclass stays for now. Yay OO.
    states = States()

    if isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as filehandler:
            file: List[str] = filehandler.readlines()

        constants, all_vars = get_names_from_file(file, states=states)

        # This speed up has been removed in favor of never scraping the file twice.
        # But we still need the custom exit code.

        # I tried to to remove that states.errors check and broke everything.
        if not constants and not states.errors:
            print('No constants declared, use #$ at then end of a line with a declaration.')
            sys.exit(2)

        cross_reference(constants, all_vars, states=states)
    else:
        print(f'{filepath.rsplit("/")[-1]} is not a file. No linting possible.')

def get_names_from_file(file: List[str], states: States) -> Tuple[dict, dict]:
    '''This function checks every line of a file and grabs names from those lines.'''

    def get_name_from_line(line: str) -> str:
        '''This function takes a line of a file and runs all the name parse funcs
        over the line. Once a nonempty string is found a name is returned.'''

        line = line.lstrip()
        name: str = paren_parse(line)
        if name:
            states.indent += 1       # Is this all I need?
            return name
        return equal_sign_parse(line)

    # Find room for an if states.indent path, and then get ready for all the dict stuff.
    all_vars: DictStrSet = {}
    constants: DictStrSet = {}
    for index, line in enumerate(file):
        # I could do this with one less if statement but the boolean helps
        # Raise the edge case at the bottom of the function and I like that.
        const_declared: bool = False

        if '#$' in line.rstrip()[-2:]:
            const_declared = True

        name: str = get_name_from_line(line)

        if name:
            all_vars.setdefault(name, set()).add(index + 1)
            if const_declared:
                constants.setdefault(name, set()).add(index + 1)

        elif const_declared:
            print(f'Immutable var declared on line number {index + 1}, but no names found.')
            states.errors=True
    return constants, all_vars


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


def equal_sign_parse(line: str) -> str:
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

    for name, values in constants.items():
        for val in values:
                                    # I tried default=set() but that broke my tests
                                    # mypy is being dumb here because None seems to work
            set_of_line_numbers = all_vars.get(name)
            for num in set_of_line_numbers:          # type: ignore
                if num == val:
                    continue
                mes=f'Bad use {name} was made static on line {val}, and mutated on line {num}'
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
