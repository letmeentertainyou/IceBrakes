#!/bin/python3
'''
At the top of the get_names_from_file() loop for every line of the file we
will check for triple quotes to either enter or exit a multiline comment. If
an entrance is found we have to check the rest of the line for an exit. So
this will require a separate function. We'll have a bool in States() that
allows us to skip the rest of the line checks until the multi line string
is exited.

This is going to be a nice performance boost because it allows us to ignore
many lines we checked before.

There can only be one multiline string at a time so we only need to track
whether it was single or double quotes that entered the string and once
a string is exited we need to continue tracking.

It might be best to use regex to get every occurrence of """ from the line
and then do some logic based on the tree of """s. We need to track groups
of three quotes at a time, and track the index of the third quote. So that
a pattern line """" doesn't appear as an entrance and an exit. 

Also """" "" is not a valid exit either. It needs to be another group of
three quotes like """""" or """ """

If there are characters before the string starts then we do need to parse
the line. So this is mostly for tracking when entire sections of a file
are not to be parsed.


    1. If string is declared set flag
    2. Parse the rest of the string to possibly unset the flag too
    3. If index of string is zero continue.
'''
from typing import List, Tuple

def find_first_index(tag: str, line: str) -> Tuple:
    '''Grabs the index of the first occurrence of a given string.'''
    try:
        return line.index(tag), tag
    except ValueError:
        return None, None


# LATER open_comment will be States.open_comment
#  open_comment
# -1 = """
#  0 = False
#  1 = '''
def parse_line(line: str, open_comment: int = 0) -> None:
    '''A basic multiline comment parser. Still needs a bit of recursion.'''
    single: str = "'''"
    double: str = '"""'

    tags: List[str] = []

    # Both of these proc on zero. Chef's kiss!
    if single in line and open_comment >=0:
        tags.append(single)

    if double in line and open_comment <=0:
        tags.append(double)

    if tags:
        all_tags: List[Tuple] = [find_first_index(tag, line) for tag in tags]
        smallest = min(all_tags)

        if smallest[1] == single:
            open_comment = 1

        if smallest[1] == double:
            open_comment = -1

        print(smallest)

        # Pop off line
        # use the index we just got

        # Recurse
        # send the truncated string back through.
        # It will stop looping when no more tags are found in the line.

    # if tags is empty then the line is done being parsed.


# This is a demo of how this would be implemented,
# We'll need to sneak a continue in there somewhere too.

if __name__ == '__main__':
    with open('multiline_trainer.txt', 'r', encoding='UTF-8') as tempfile:
        file: List[str] = tempfile.readlines()

    # pylint didn't line 'line' here
    for item in file:
        parse_line(item)
