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

# Parsing something like this will require an engine.
# ''' """ ''' """ ''' """
