#!/bin/python3
'''This is just the first part in a long series of steps required for scope awareness.
Eventually the methods of this file may get pulled into icebrakes.py, but first I want to
build my algorithms without breaking any of the unit tests.

I was kind of surprised I couldn't find a package or tool to do this since python is all about
indentation levels but i turned out to be a really easy solve. '''

from math import gcd
from functools import reduce
from typing import Set


def white_space_parse(file: str) -> int:
    '''Takes a file, calculates the indentation level using magic.
    For now we parse the first 100 lines of the file as that should be more than enough,
    but that number can probably be reduced a bit. It doesn't start counting until white
    space is found to ignore files will hundreds of lines of imports/doc strings.

    Also we are considering tabs as whitespace but there will be more work to process them
    later (aka you are a monster if your file has tabs in it), and also it's gonna be a mess 
    if you mix whitespace/tabs. So IceBrakes is going to assume some level of responsibility 
    belongs with the dev.'''

    levels: Set = set()
    with open(file, encoding="UTF-8") as tempfile:
        # DON'T DO READ LINES.
        num: int = 0
        for line in tempfile:
            if num == 100000:
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

out = white_space_parse('icebrakes.py')
print(out)
