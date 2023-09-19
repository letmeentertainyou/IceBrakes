#!/bin/python3
'''
# TESTING
# Lint every file in src/tests/tests/ >> output file.txt (append mode)
# Writing the test first means locking in the API, and that's good.

# CODING
# check if argv[1] is a dir or a file, for the dir loop through python files
# This gives us a chance to reject non python files wholesale for dirs, 
# Our output message should contain some formatting to address each file linted. 
# This can be achieved with a single new function, and an if statement in 
parse_file_by_name() 

Here is the code writeup from TODO.txt

    *Directory support

        IceBrakes should run with either a file or a dir of files as input. I will add
        a bool to get_names_from_file() that tracks when a dir is being parsed. When
        in dir_more we return an exit code instead of exiting with that code. Here is an
        example of the code.

        def get_names_from_file(file: str, dir_mode: bool=False) -> int:
            exit_code: int = 0
            if dir_mode:
                return exit_code
            else:
                exit(exit_code)

        Then the dir function just collects all the exit codes and prints them all
        for now. This won't break a single unit test or the API.


The above writeup assumes only one directory but of course projects can have recursive directories.
So we need some level of recursion to get all files, in all dirs, and then parse them. I suspect
this tool already exists in python. I am gonna write the single dir parse first regardless. 

When the file_or_dir function is written then the is_file() check in icebrakes will be redundant. So
remove it. '''
