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
'''
