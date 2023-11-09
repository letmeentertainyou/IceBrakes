BUG FIXES

This is a new addition to the methodology. Now any bug fixes need
to be manually tested so that they will be caught easier in the future.

I understand now why bugs are assigned numbers and documented. While it is
often easy to patch the bugs I as I discover them, I am not really documenting them
and that leaves me exposed to doing the exact same work over and over again.

Bug tests will be numbered 2000-2999.


TESTING

Going from 0.0.1 onward features will be defined in a test before development. 
See DOCS/test_manifest.txt for a detailed list of the tests and what they check.

All tests need to be backwards and forwards compatible so I am not writing tests
to prove that features don't exist. If for example I wrote a test to prove that 
scopes aren't implemented, then I would need to delete that test when scopes are added.

Most of the these tools only apply to test numbers begging with 0. (test_0000.py - test_0999.py).

This testing methodology only tests IceBrakes linter ability. I realize that I should
write tests outside of the scope of linting as well. Those tests will not use the method
laid out below.

There are two main python files in src/tests
    template.py (a sample test)
    tools.py (the testing api)


*** bellow is the full text of template.py for reference

BEGIN TEMPLATE
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

When you write a test following this template then the test will uce IceBrakes
to lint itself and record the output. You have to provide at least one sample of
an expected output for the given test in order to know if you have passed or failed.
Generating test output data is detailed below.

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

This module contains all the tools used by the testing methodology, I'll break it down
by function below.

pytest is my testing tool of choice so you will need to pip install it into
your python3 environment to do any testing.

Below is a list of functions provided in tools.py.


*** parse_argv(args: List[str]) -> None
    This is the CLI implementation of tools.py. The current use cases are:

    ./tools.py ####
    Call tools.py with a single integer arg to generate output data 
    for the given test number.
    
    ./tools.py -a
    -a to generate data for all tests

    ./tools.py -n ####
    -n to copy the template to a new test file numbered after the second arg.
    The template will be named _test_####.py which means it will not be run
    by pytest until the leading underscore is removed.

    Also there is a sed command that replaces "test_number" in the template with the real number of the test being created.


*** cleanup() -> None
    Deletes the temporary .txt files created during the tests.


*** filecmp(path_1: str, path_2: str) -> bool
    This is named after the python builtin filecmp.cmp but my 
    version only checks if the lines of the two files are the 
    same and not the metadata.


*** int_to_filepath(num: str) -> str
    The first testing API had you give the full name of the test file.
    pytest_runner('test_999.py') or pytest_runner(__name__) from inside
    a python file testing itself.

    I simplified it so that all interactions with tools.py take a single
    integer as input, so this function does the conversion. Thus '0000' or '0' becomes
    'test_0000.py'

    One downside to this is that the entire api relies on the same filename
    which means any new format of test may require additional API features.


*** pytest_runner(num: str, get_code: bool=False) -> int
    This function runs a IceBrakes.py lint on the given input file,
    and sends the given output to a tmp file. A test should never be written
    with an invalid input file because the test_####.py files are 
    the test input themselves. 
    
    When you call pytest_runner with get_code=True, then pytest_runner returns the exit code
    of icebrakes.py. This is useful for testing the exit codes in test_1001.

    pytest_runner now returns 9999 by default, this is to please pylint which wants all paths
    to either explicitly return something or have no returns at all.


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


Copyright © 2023 Lars S.
