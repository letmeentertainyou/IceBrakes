'''Test what happens when #$ is declared on a line but no
vars are assigned on that line. This gives a unique output message.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
def foobar(foo: int, goo: int) -> int:
    '''This test declares immutability on a line with no assignment.'''
    return foo ** goo #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('4')


#Copyright © 2023 Lars S.
