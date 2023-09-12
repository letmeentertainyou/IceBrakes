*** Addendum ***
    Most of the these tools only apply to tests starting in 0 now.
    test_0000.py to test_0999.py, this gives us 1000 tests following
    the format and gives us room for any tests that will not be linting themselves.

    We need tests for various other interfaces in the main package, as well as
    tests for the testing tools and neither of these will use the template methodology
    laid out. 

################### TESTING ######################

Going from 0.0.1 onward features will be defined in a test before development. 
See DOCS/test_maninfest.txt for a detailed list of the tests and what they check.

All tests need to be backwards and forewards compatable so I am not writing tests
to prove that features don't exist. If for example I wrote a test to prove that 
scopes aren't implemented, then I would need to delete that test when scopes are added.

Instead I will focus on core features and add additional 'completeness' testing as I go.

There are two main python files in src/tests
    template.py (a sample test)
    tools.py (the testing api)
 

*** bellow is the fulltext of template.py for reference

BEGINE TEMPLATE
'''The test_###.py file is also the file we are linting.'''
from src.tests.tools import static_checker

##################################################
############### BEGIN TEST CODE ##################
##################################################
FOO = 0
BAR = 0 #$
GOO = 0
CAR = 0 #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('###')


END TEMPLATE

In the template you write code between the two huge blocks of #s, and then
you specify the number of the test in the pytest_runner call at the bottom
of the template. 

Because IceBrakes.py only looks for lines ending in #$ as long as those characters 
aren't in the rest of the file and no names are duplicated between the test 
block and the rest of the file, we are essentially only linting the test block.

As for formatting the vars FOO and BAR will be used in all tests with different
forms of capitalization to appease pylint. 
    Foo and anything that rhymes with foo will be mutable. 
    Bar and it's rhymes will be immutable.

    FOO is mutable, BAR is not.
    GOO is mutable, CAR is not.

It's worth noting that I could have a single dir full of sample python files and
I could have a single test that runs the linter on every file in that dir. The side
effect of that method would be that pytest considers that a singe test. Which means
it will be really hard to track down failures. With my current method pytest reports
the name of the failed test.


*** tools.py

While you can just copy and paste the testing template as you'd like, I did automate that.
tools.py contains helpers for running tests, generating test data, and generating tests themselves.

This module contains all the tools used by the testing methodoloy, I'll break it downside
by function below.

pytest is my testing tool of choice so you will need to pip install it into
your python3 enviroment to do any testing.

Below is a list of functions provided in tools.py.


*** parse_argv(args: List[str]) -> None
    This is the CLI implementation of tools.py. The current use cases are:

    ./tools.py ###
    Call tools.py with a single integer arg to generate output data 
    for the given test number.
    
    ./tools.py -a
    -a to genererate data for all tests

    ./tools.py -n ###
    -n to copy the template to a new test file numbered after the second arg.
    The template will be named _test_###.py which means it will not be run
    by pytest until the leading underscore is removed.

    Also there is a sed command that replaces "test_number" in the template with the real number of the test being created.

*** cleanup() -> None
    Deletes the tempory .txt files created during the tests.
    This leaves the .gitignore file which is important for
    git to recognize empty dirs which I've decided I want

*** filecmp(path_1: str, path_2: str) -> bool
    This is named after the python builtin filecmp.cmp but my 
    version only checks if the lines of the two files are the 
    same and not the metadata.


*** int_to_filepath(num: str) -> str
    The first testing API had you give the full name of the test file.
    pytest_runner('test_999.py') or pytest_runner(__name__) from inside
    a python file testing itself.

    I simplified it so that all interactions with tools.py take a single
    integer as input, so this function does the conversion. Thus '000' becomes
    'test_000.py'

    One downside to this is that the entire api relies on the same filename
    which means any new format of test may require additional API features.

    I may find a better method as testing develops further.


*** pytest_runner(num: str) -> None
    This function runs a IceBrakes.py lint on the given input file,
    and sends the given output to a tmp file. A test should never be written
    with an invalid input file because the test_###.py files are 
    the test input themselves. 
    
    However I should add some code in IceBrakes.py to validate that a given input file is a valid python file. And then I should write tests for an invalid input use case.
    

*** gen_output_for_all_test_0()-> None
    This function gets called when you run 
    ./tools.py -a

    Output data will be generated for every test with a number starting
    with 0 using the current version of IceBrakes.py. This could overwrite 
    valid data with invalid data so make sure to only use this function when
    every test is passing!

    'Every test' is defined as files in src/tests/tests that start with 
    the four characters 'test' this means any '_test' file is 
    ignored until the file's name is changed. 

    As a side effect no file/folder is src/tests/tests can have less than four chars 
    in it's name.


Copyright © 2023 Lars S.
